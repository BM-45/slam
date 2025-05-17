import numpy as np
import math


# Smart keyframe selector for SLAM systems.
# Used ORB-SLAM2's logic:
#      1) Don’t insert if mapping is busy or initialization isn’t done
#      2) If map is tiny, force a keyframe every few frames
#      3) Check translation/rotation thresholds
#      4) Check tracking quality (number of inliers)

class KeyframeSelector:
    def __init__(self, map_manager, local_mapper, init_done_flag, trans_thresh=0.1, rot_thresh_deg=5.0,quality_ratio=0.9):

        self.map_mgr = map_manager
        self.local_mapper = local_mapper
        self.init_done_flag = init_done_flag
        self.trans_thresh = trans_thresh
        self.rot_thresh = math.radians(rot_thresh_deg)
        self.quality_ratio = quality_ratio

    def need_new_keyframe(self,
                          last_kf_pose,       # 4×4 matrix of last KF
                          curr_pose,         # 4×4 matrix of current frame
                          n_inliers,         # number of tracked inliers this frame
                          last_kf_tracked):  # number of map points tracked in last KF
        # 1) Don’t insert if mapping is busy or initialization isn’t done
        if not self.init_done_flag():
            return False
        if self.local_mapper.is_stopped() or self.local_mapper.stop_requested():
            return False

        # 2) If map is tiny, force keyframe every few frames
        if self.map_mgr.KeyFramesInMap() <= 2:
            return True

        # 3) Check translation/rotation thresholds
        # translation delta
        delta_t = np.linalg.norm(curr_pose[:3,3] - last_kf_pose[:3,3])
        # rotation delta (angle between rotations)
        R_rel = last_kf_pose[:3,:3].T @ curr_pose[:3,:3]
        trace = np.trace(R_rel)
        # clamp numerical errors
        cos_angle = min(1.0, max(-1.0, (trace - 1)/2))
        delta_r = math.acos(cos_angle)

        if delta_t > self.trans_thresh or delta_r > self.rot_thresh:
            return True

        # 4) Check tracking quality (number of inliers)
        if last_kf_tracked > 0 and n_inliers < self.quality_ratio * last_kf_tracked:
            return True

        return False
