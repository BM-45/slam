import cv2

class PoseEstimator:

    def __init__(self, focal: float, pp: tuple):
        self.focal = focal
        self.pp = pp

    def recover(self, E, pts1, pts2):

        _, R, t, mask = cv2.recoverPose(
            E, pts1, pts2,
            focal=self.focal,
            pp=self.pp
        )
        return R, t, mask
