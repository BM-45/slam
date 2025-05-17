class BundleAdjuster:
    
    def __init__(self, max_iters=5):
        self.max_iters = max_iters

    def optimize(self, local_map):
        local_map.optimize()