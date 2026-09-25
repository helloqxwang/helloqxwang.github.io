import importlib.util
import json
from pathlib import Path
import unittest
import tempfile
import subprocess
from imageio_ffmpeg import read_frames
from PIL import Image
ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('media', ROOT / 'scripts/prepare-media.py')
media = importlib.util.module_from_spec(spec)
spec.loader.exec_module(media)

class MediaTests(unittest.TestCase):
    def test_live_photo_companion_and_browser_video(self):
        with tempfile.TemporaryDirectory() as folder:
            folder = Path(folder)
            still, video = folder/'Live.HEIC', folder/'Live.MOV'
            still.touch()
            self.assertIsNone(media.live_companion(still, {}))
            with self.assertRaises(ValueError): media.live_companion(still, {'live':'missing.MOV'})
            subprocess.run([media.get_ffmpeg_exe(), '-v', 'error', '-f', 'lavfi', '-i',
                'testsrc2=size=640x480:rate=10:duration=0.4', '-an', '-c:v', 'libx264', str(video)], check=True)
            self.assertEqual(media.live_companion(still, {}), video)
            output = folder/'web.mp4'
            media.prepare_live(video, output, [.2,.1,.4,2/3])
            frames = read_frames(str(output))
            metadata = next(frames)
            self.assertEqual(metadata['size'], (800,1000))
            first, second = next(frames), next(frames)
            self.assertNotEqual(first, second)
            frames.close()
            full = folder/'full.mp4'
            media.prepare_live(video, full)
            full_frames = read_frames(str(full))
            full_metadata = next(full_frames)
            width, height = full_metadata['size']
            self.assertAlmostEqual(width/height, 640/480)
            self.assertLessEqual(width, 1440)
            self.assertLessEqual(height, 1920)
            self.assertNotEqual(next(full_frames), next(full_frames))
            full_frames.close()

    def test_missing_metadata_is_not_invented(self):
        data = media.metadata_from_exif({271:'SONY', 272:'ILCE-7CM2', 42036:'----', 33434:1/4000})
        self.assertEqual(data['lens'], '')
        self.assertEqual(data['focal_length'], '')
        self.assertEqual(data['aperture'], '')
        self.assertEqual(data['shutter'], '1/4000 s')

    def test_manual_crop_is_validated(self):
        image = Image.new('RGB', (1000,1000))
        with self.assertRaises(ValueError): media.face_crop(image, {'crop':[.9,0,.4,.5]})
        with self.assertRaises(ValueError): media.face_crop(image, {'crop':[0,0,.5,.5]})
        crop, info = media.face_crop(image, {'crop':[.2,.1,.4,.5]})
        self.assertEqual(info['method'], 'manual override')
        self.assertEqual(crop, [.2,.1,.4,.5])

    def test_current_portraits_have_faces_and_valid_context_crops(self):
        manifest = json.loads((ROOT / 'src/data/media.json').read_text())
        self.assertEqual(len(manifest['portraits']), 6)
        for photo in manifest['portraits']:
            x,y,w,h = photo['crop']
            self.assertTrue(x >= 0 and y >= 0 and x+w <= 1.00001 and y+h <= 1.00001)
            self.assertAlmostEqual(w*photo['width']/(h*photo['height']), .8, places=4)
            self.assertGreater(photo['detection']['confidence'], .65)
            fx,fy,fw,fh = photo['detection']['faceBox']
            self.assertTrue(x <= fx and y <= fy and x+w >= fx+fw and y+h >= fy+fh)
            self.assertGreater(h, fh*2)

    def test_photo_priority_and_real_exif(self):
        photos = json.loads((ROOT / 'src/data/media.json').read_text())['photos']
        self.assertEqual([p['id'] for p in photos if p['priority']==1], ['DSC06320'])
        self.assertEqual(photos[0]['metadata']['shutter'], '1/2500 s')
        self.assertEqual(photos[0]['metadata']['aperture'], 'f/1.4')
        self.assertEqual(photos[0]['metadata']['focal_length'], '85 mm')

if __name__ == '__main__': unittest.main()
