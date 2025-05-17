import cv2
# used ORB or superpoint(deep learning based feature extractor got to know from paper) for feature extraction

class FeatureExtractor:
    def __init__(self, method='ORB', **kwargs):
        if method == 'ORB':
            self.det = cv2.ORB_create(**kwargs)
        else:
            from superpoint import SuperPoint
            self.det = SuperPoint(**kwargs)

    def extract(self, img_gray):
        if hasattr(self.det, 'detectAndCompute'):
            return self.det.detectAndCompute(img_gray, None)
        else:
            return self.det.run(img_gray)
