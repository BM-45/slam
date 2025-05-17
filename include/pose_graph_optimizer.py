class PoseGraphOptimizer:

    def __init__(self):
        self.constraints = []
        self.poses = {}

    def add_loop_constraint(self, src_id, dst_id, pose_src, pose_dst):
        self.constraints.append((src_id, dst_id, pose_src.copy(), pose_dst.copy()))
        self.poses[src_id] = pose_src.copy()
        self.poses[dst_id] = pose_dst.copy()

    def optimize(self, max_iter=10):
        pass

    def get_poses(self):
        return self.poses