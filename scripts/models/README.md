# YuNet face detector

Official model: https://github.com/opencv/opencv_zoo/tree/main/models/face_detection_yunet

`face_detection_yunet_2023mar.onnx` uses the OpenCV 4.x FaceDetectorYN interface.
Downloaded from the official OpenCV Zoo repository. Its MIT license is included in `YUNET-LICENSE`.

The network detects faces, not identity. We select the largest detected face unless YAML selects another,
then apply a configurable 4:5 composition with headroom and shoulder/background context.
This is face-aware framing, not a learned aesthetic-quality model. No images are uploaded to a service.
