import numpy as np
import math

class PoseOptimizer:

    def __init__(self, max_trans=1.0, max_rot_deg=5.0):
        self.max_trans = max_trans
        self.max_rot   = math.radians(max_rot_deg)

    def filter(self, R, t):
      
        if np.linalg.norm(t) > self.max_trans:
            return False
  
        angle = math.acos(max(-1.0, min(1.0, (np.trace(R)-1)/2)))
        if angle > self.max_rot:
            return False
        return True
