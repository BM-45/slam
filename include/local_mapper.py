class LocalMapper:
    def __init__(self, K, window_size=5):
        self.K = K
        self.window = []
        self.window_size = window_size
    def add_keyframe(self, kf_id, pose, lm_ids, desc=None):
        self.window.append((kf_id, pose, lm_ids))
        if len(self.window) > self.window_size:
            self.window.pop(0)
    def optimize(self):
        pass