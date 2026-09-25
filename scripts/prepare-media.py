"""Local neural headshot crops and EXIF-aware web media. Originals are never modified."""
from pathlib import Path
import hashlib
import io
import json
import math
import re
import sys
import subprocess
import fcntl

import cv2
import numpy as np
import yaml
from PIL import Image, ImageCms, ImageOps
from pillow_heif import register_heif_opener, open_heif
from imageio_ffmpeg import get_ffmpeg_exe

ROOT = Path(__file__).resolve().parents[1]
MODEL = ROOT / "scripts/models/face_detection_yunet_2023mar.onnx"
VERSION = "headshot-color-live-3"
EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".avif", ".heic", ".heif"}
register_heif_opener()


def write_if_changed(path, content):
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists() or path.read_text() != content:
        temporary = path.with_suffix(path.suffix + ".tmp")
        temporary.write_text(content)
        temporary.replace(path)


def read_config(name, key, directory):
    config = yaml.safe_load((ROOT / "config" / name).read_text())
    entries = config.get(key, [])
    names = [row["file"] for row in entries]
    if len(set(names)) != len(names):
        raise ValueError(f"Duplicate filenames in {name}")
    # New images work without requiring a YAML edit; YAML is for order/overrides.
    for path in sorted((ROOT / directory).iterdir()):
        if path.suffix.lower() in EXTENSIONS and path.name not in names:
            entries.append({"file": path.name})
    for row in entries:
        if Path(row["file"]).name != row["file"]:
            raise ValueError("Image filenames must refer to files directly in their source folder")
        if not (ROOT / directory / row["file"]).is_file():
            raise ValueError(f"Missing source image: {directory}/{row['file']}")
    return config.get("defaults", {}), entries


def read_image(path):
    with Image.open(path) as source:
        exif = dict(source.getexif())
        exif.update(source.getexif().get_ifd(34665))
        profile = source.info.get("icc_profile")
        # Pillow's AVIF RGB conversion does not apply the file's CICP transfer
        # function or primaries. Decode the complete tile grid at 16-bit first.
        if path.suffix.lower() == ".avif" and not profile:
            heif = open_heif(path, convert_hdr_to_8bit=False)
            color = heif.info.get("nclx_profile", {})
            if color.get("color_primaries") == 9:
                transfer = color.get("transfer_characteristics")
                if transfer not in (1, 14, 15, 16):
                    raise ValueError(f"Unsupported AVIF transfer characteristic: {transfer}")
                filters = ["format=gbrp16le", f"zscale=pin=bt2020:tin={transfer}:min=gbr:rin=full:p=bt2020:t=linear:m=gbr:r=full:npl=203", "format=gbrpf32le", "zscale=p=bt709"]
                if transfer == 16:
                    filters.append("tonemap=mobius:desat=2")
                filters += ["zscale=t=iec61966-2-1", "format=rgb24"]
                pixel_format = "rgb48le" if heif.mode == "RGB;16" else "rgb24"
                result = subprocess.run([get_ffmpeg_exe(), "-v", "error", "-filter_threads", "2", "-f", "rawvideo", "-pix_fmt", pixel_format,
                    "-s", f"{heif.size[0]}x{heif.size[1]}", "-i", "pipe:0", "-vf", ",".join(filters), "-frames:v", "1", "-f", "rawvideo", "-pix_fmt", "rgb24", "pipe:1"],
                    input=bytes(heif.data), capture_output=True)
                if result.returncode:
                    raise ValueError(f"Color conversion failed: {result.stderr.decode()[-600:]}")
                return Image.frombytes("RGB", heif.size, result.stdout), exif
        image = ImageOps.exif_transpose(source).convert("RGB")
        if profile:
            try:
                image = ImageCms.profileToProfile(image, ImageCms.ImageCmsProfile(io.BytesIO(profile)),
                                                  ImageCms.createProfile("sRGB"), outputMode="RGB")
            except (OSError, ImageCms.PyCMSError):
                print(f"Warning: could not convert color profile for {path.name}", file=sys.stderr)
    return image, exif


def clean(value):
    text = str(value or "").strip().strip("\x00")
    return "" if text in {"", "----", "0", "Unknown"} else text


def number(value):
    try:
        result = float(value)
        return result if math.isfinite(result) and result > 0 else None
    except (TypeError, ValueError, ZeroDivisionError):
        return None


def metadata_from_exif(exif):
    make, model = clean(exif.get(271)), clean(exif.get(272))
    camera = model if model.lower().startswith(make.lower()) else f"{make} {model}".strip()
    exposure = number(exif.get(33434))
    focal, aperture, iso = number(exif.get(37386)), number(exif.get(33437)), number(exif.get(34855))
    return {
        "camera": camera,
        "lens": clean(exif.get(42036)),
        "shutter": (f"1/{round(1 / exposure)} s" if exposure < 1 else f"{exposure:g} s") if exposure else "",
        "focal_length": f"{focal:g} mm" if focal else "",
        "aperture": f"f/{aperture:g}" if aperture else "",
        "iso": f"ISO {iso:g}" if iso else "",
    }


def face_crop(image, settings):
    width, height = image.size
    if settings.get("crop") is not None:
        x, y, w, h = map(float, settings["crop"])
        if not (min(x, y) >= 0 and min(w, h) > 0 and x + w <= 1 and y + h <= 1):
            raise ValueError("crop must be normalized and inside the image")
        if abs((w * width) / (h * height) - .8) > .02:
            raise ValueError("Manual crop must have a 4:5 pixel aspect ratio")
        return [x, y, w, h], {"method": "manual override"}
    preview = image.copy()
    preview.thumbnail((1280, 1280))
    detector = cv2.FaceDetectorYN.create(str(MODEL), "", preview.size, .65, .3, 5000)
    faces = detector.detect(cv2.cvtColor(np.asarray(preview), cv2.COLOR_RGB2BGR))[1]
    if faces is None:
        raise ValueError("No face found. Add a normalized 4:5 crop override in config/portraits.yml")
    candidates = sorted(faces, key=lambda face: float(face[0]))
    if "face_index" in settings:
        face = candidates[int(settings["face_index"])]
    else:
        face = max(candidates, key=lambda item: float(item[2] * item[3]))
    sx, sy = width / preview.width, height / preview.height
    fx, fy, fw, fh = float(face[0]) * sx, float(face[1]) * sy, float(face[2]) * sx, float(face[3]) * sy
    context = float(settings.get("context", 3.8))
    position = float(settings.get("face_position", .36))
    if not 2 <= context <= 8 or not .2 <= position <= .6:
        raise ValueError("context must be 2–8; face_position must be 0.2–0.6")
    crop_height = min(max(fh * context, fw * 2.8 / .8), height, width / .8)
    crop_width = crop_height * .8
    x = max(0, min(width - crop_width, fx + fw / 2 - crop_width / 2))
    y = max(0, min(height - crop_height, fy + fh / 2 - crop_height * position))
    return [x / width, y / height, crop_width / width, crop_height / height], {
        "method": "YuNet + context crop", "confidence": round(float(face[-1]), 4),
        "facesDetected": len(faces), "faceBox": [fx / width, fy / height, fw / width, fh / height],
    }


def save_webp(image, target, size, quality):
    output = image.copy()
    output.thumbnail(size, Image.Resampling.LANCZOS)
    target.parent.mkdir(parents=True, exist_ok=True)
    output.save(target, "WEBP", quality=quality, method=5,
                icc_profile=ImageCms.ImageCmsProfile(ImageCms.createProfile("sRGB")).tobytes())


def live_companion(source, settings):
    if settings.get("live"):
        name = settings["live"]
        if Path(name).name != name or not (source.parent / name).is_file():
            raise ValueError(f"Missing Live Photo companion in headshots/: {name}")
        return source.parent / name
    return next((p for p in sorted(source.parent.iterdir())
                 if p.stem.lower() == source.stem.lower() and p.suffix.lower() in (".mov", ".mp4")), None)


def prepare_live(source, target, crop=None):
    target.parent.mkdir(parents=True, exist_ok=True)
    temporary = target.with_suffix(".building.mp4")
    info = subprocess.run([get_ffmpeg_exe(), "-hide_banner", "-i", str(source)], capture_output=True, text=True).stderr
    filters = ""
    if "smpte2084" in info or "arib-std-b67" in info:
        filters = "zscale=t=linear:npl=203,format=gbrpf32le,zscale=p=bt709,tonemap=mobius:desat=2,zscale=t=bt709:m=bt709:r=limited,format=yuv420p,"
    elif "smpte432" in info:
        # iPhone Display P3 footage needs an actual gamut conversion, not just
        # different output tags, to match the color-managed sRGB still.
        filters = "zscale=p=bt709:t=bt709:m=bt709:r=limited,"
    if crop is not None:
        x, y, w, h = crop
        filters += f"crop=iw*{w}:ih*{h}:iw*{x}:ih*{y},scale=800:1000:force_original_aspect_ratio=increase,crop=800:1000,setsar=1"
    else:
        filters += "scale=1440:1920:force_original_aspect_ratio=decrease:force_divisible_by=2,setsar=1"
    # Use the full sensor framing before applying the still's normalized crop;
    # applying Apple's clean-aperture inset first would zoom the face twice.
    result = subprocess.run([get_ffmpeg_exe(), "-v", "error", "-y", "-apply_cropping", "0", "-i", str(source), "-vf", filters,
        "-map", "0:v:0", "-an", "-map_metadata", "-1", "-c:v", "libx264", "-crf", "20", "-preset", "medium", "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(temporary)], capture_output=True)
    if result.returncode:
        temporary.unlink(missing_ok=True)
        raise ValueError(f"Live Photo conversion failed: {result.stderr.decode()[-600:]}")
    temporary.replace(target)


def prepare():
    cache_path = ROOT / ".media-cache.json"
    cache = json.loads(cache_path.read_text()) if cache_path.exists() else {}
    new_cache = {}
    manifest = {"portraits": [], "photos": []}
    generated = 0
    model_hash = hashlib.sha256(MODEL.read_bytes()).hexdigest()
    for kind, folder, config in [("portraits", "headshots", "portraits.yml"), ("photos", "Photos", "photos.yml")]:
        defaults, entries = read_config(config, kind, folder)
        ids = set()
        for row in entries:
            settings = {**defaults, **row}
            source = ROOT / folder / row["file"]
            stem = re.sub(r"[^a-zA-Z0-9_-]", "-", source.stem)
            if stem in ids:
                raise ValueError(f"Duplicate output stem: {stem}")
            ids.add(stem)
            key = f"{kind}/{source.name}"
            live = live_companion(source, settings) if kind == "portraits" else None
            signature = hashlib.sha256(source.read_bytes() + json.dumps(settings, sort_keys=True).encode()
                                       + (live.read_bytes() if live else b"")
                                       + (VERSION + model_hash).encode()).hexdigest()
            old = cache.get(key)
            if old and old["signature"] == signature and all((ROOT / "public" / p.lstrip("/")).exists() for p in old["outputs"]):
                data = old["data"]
                new_cache[key] = old
            else:
                image, exif = read_image(source)
                width, height = image.size
                if kind == "portraits":
                    crop, detection = face_crop(image, settings)
                    data = {"id": stem, "src": f"/portraits/{stem}.webp", "full": f"/portraits/{stem}-full.webp",
                            "width": width, "height": height, "crop": crop, "detection": detection,
                            "alt": settings.get("alt", "Portrait of Qianxu Wang"), "live": f"/portraits/{stem}-live.mp4" if live else None,
                            "liveFull": f"/portraits/{stem}-live-full.mp4" if live else None}
                    x, y, w, h = crop
                    thumbnail = image.crop((round(x * width), round(y * height), round((x + w) * width), round((y + h) * height)))
                    save_webp(thumbnail, ROOT / "public" / data["src"].lstrip("/"), (800, 1000), 88)
                    save_webp(image, ROOT / "public" / data["full"].lstrip("/"), (2200, 2200), 88)
                    if live:
                        prepare_live(live, ROOT / "public" / data["live"].lstrip("/"), crop)
                        prepare_live(live, ROOT / "public" / data["liveFull"].lstrip("/"))
                    print(f"{source.name}: {detection['method']}, crop {[round(v, 3) for v in crop]}")
                else:
                    priority = settings.get("priority", 0)
                    if type(priority) is not int or priority not in (0, 1):
                        raise ValueError(f"{source.name}: priority must be 0 or 1")
                    metadata = metadata_from_exif(exif)
                    overrides = settings.get("metadata", {})
                    for field, value in overrides.items():
                        if field not in metadata:
                            raise ValueError(f"Unknown metadata field {field}")
                        metadata[field] = clean(value)
                    data = {"id": stem, "src": f"/photography/{stem}.webp", "full": f"/photography/{stem}-large.webp",
                            "width": width, "height": height, "priority": priority, "metadata": metadata,
                            "caption": str(settings.get("caption", "exif")), "alt": settings.get("alt", f"Photograph {stem}")}
                    save_webp(image, ROOT / "public" / data["src"].lstrip("/"), (1500 if priority else 900, 2000), 85)
                    save_webp(image, ROOT / "public" / data["full"].lstrip("/"), (2200, 2400), 88)
                new_cache[key] = {"signature": signature, "data": data, "outputs": [data["src"], data["full"]] + ([data["live"], data["liveFull"]] if data.get("live") else [])}
                generated += 1
            manifest[kind].append(data)
    if not manifest["portraits"]:
        raise ValueError("Add at least one portrait to headshots/")
    write_if_changed(ROOT / "src/data/media.json", json.dumps(manifest, indent=2, ensure_ascii=False) + "\n")
    write_if_changed(cache_path, json.dumps(new_cache, indent=2, ensure_ascii=False) + "\n")
    print(f"Media ready: {len(manifest['portraits'])} portraits, {len(manifest['photos'])} photographs; {generated} updated.")


if __name__ == "__main__":
    try:
        # The preview watcher and a manual build may start together. Serialize
        # writers so neither the MP4 faststart pass nor the manifest is corrupted.
        with (ROOT / ".media-preparation.lock").open("w") as lock:
            fcntl.flock(lock, fcntl.LOCK_EX)
            prepare()
    except Exception as error:
        print(f"Media preparation failed: {error}", file=sys.stderr)
        sys.exit(1)
