export type Rect = { left: number; top: number; width: number; height: number };
type Photo = { crop: number[]; width: number; height: number };
const clamp = (n: number, min: number, max: number) => Math.max(min, Math.min(max, n));
/** Reveal context without changing the scale or screen position of the headshot. */
export function portraitGeometry(source: Rect, photo: Photo, viewport: { width: number; height: number }, fit = false) {
  const [x, y, w] = photo.crop;
  const width = source.width / w, height = width * photo.height / photo.width;
  const origin = { left: source.left - x * width, top: source.top - y * height };
  const margin = 24;
  // Intersect the original-scale image with the safe viewport. Moving the
  // whole image to fit would move the face away from its original position.
  const minX = Math.max(margin, origin.left), minY = Math.max(margin, origin.top);
  const maxX = Math.min(viewport.width - margin, origin.left + width);
  const maxY = Math.min(viewport.height - margin, origin.top + height);
  const frameW = Math.max(1, Math.min(maxX - minX, 1000));
  const frameH = Math.max(1, Math.min(maxY - minY, 680));
  const left = clamp(source.left + source.width / 2 - frameW / 2, minX, maxX - frameW);
  const top = clamp(source.top + source.height / 2 - frameH / 2, minY, maxY - frameH);
  const smallFrame = { ...source };
  const smallImage = { left: -x * width, top: -y * height, width, height };
  const frame = { left, top, width: frameW, height: frameH };
  const image = { left: origin.left - left, top: origin.top - top, width, height };
  if (fit) {
    const scale = Math.min(1, frameW / width, frameH / height);
    const fitW = width * scale, fitH = height * scale;
    frame.left += (frameW - fitW) / 2; frame.top += (frameH - fitH) / 2;
    frame.width = fitW; frame.height = fitH;
    Object.assign(image, { left: 0, top: 0, width: fitW, height: fitH });
  }
  return { smallFrame, smallImage, frame, image, pannable: !fit && (width > frameW + 1 || height > frameH + 1) };
}
