import cv2

class EssentialMatrixEstimator:
    def __init__(self, focal: float, pp: tuple):
        self.focal = focal
        self.pp = pp

    def compute(self, pts1, pts2):
        E, mask = cv2.findEssentialMat(
            pts1, pts2,
            focal=self.focal,
            pp=self.pp,
            method=cv2.RANSAC,
            prob=0.999,
            threshold=1.0
        )
        return E, mask
