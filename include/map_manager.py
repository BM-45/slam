import numpy as np
import cv2

class MapManager:
    def __init__(self, K):
        self.K = K
        self.keyframes = {}
        self.landmarks = {}
        self.next_lm_id = 0
    def add_keyframe(self, kf_id, pose):
        self.keyframes[kf_id] = {'pose': pose, 'lm_ids': []}
    def triangulate(self, pose1, pose2, pts1, pts2):
        pts4 = cv2.triangulatePoints(pose1[:3], pose2[:3], pts1.T, pts2.T)
        pts3 = (pts4[:3] / pts4[3]).T
        ids = []
        for P in pts3:
            lm_id = self.next_lm_id
            self.landmarks[lm_id] = P
            ids.append(lm_id)
            self.next_lm_id += 1
        return ids
    def add_observation(self, lm_id, kf_id):
        self.keyframes[kf_id]['lm_ids'].append(lm_id)