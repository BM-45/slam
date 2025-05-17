import cv2
import numpy as np
from pykitti import raw

class FrameData:

    def __init__(self, base_path: str, date: str, drive: str, frames=None):
        
        
        self.dataset = raw(base_path, date, drive, frames=frames)
        self.cam0_files = self.dataset.cam0_files  
        P = self.dataset.calib.P_rect_00  
        self.K = P[:3, :3]  

    def __len__(self) -> int:
        return len(self.cam0_files)

    def get_frame(self, idx: int) -> np.ndarray:
        img = cv2.imread(self.cam0_files[idx], cv2.IMREAD_GRAYSCALE)
        if img is None:
            raise IOError(f"Could not read frame at {self.cam0_files[idx]}")
        return img
