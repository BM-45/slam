import cv2
import numpy as np

class VideoVisualizer:
    def __init__(self, window_name='SLAM View'):
        self.window_name = window_name
        cv2.namedWindow(self.window_name, cv2.WINDOW_NORMAL)

    def update(self, frame_gray: np.ndarray, trajectory: list):
        frame_bgr = cv2.cvtColor(frame_gray, cv2.COLOR_GRAY2BGR)
        h, w = frame_gray.shape

        canvas = np.zeros((h, h, 3), dtype=np.uint8)
        if len(trajectory) >= 2:
            xs = [p[0] for p in trajectory]
            zs = [p[2] for p in trajectory]
            min_x, max_x = min(xs), max(xs)
            min_z, max_z = min(zs), max(zs)
            dx = (max_x - min_x)*0.1 or 1.0
            dz = (max_z - min_z)*0.1 or 1.0
            min_x, max_x = min_x-dx, max_x+dx
            min_z, max_z = min_z-dz, max_z+dz
            sx = (h-20)/(max_x-min_x)
            sz = (h-20)/(max_z-min_z)

            pts = []
            for x, _, z in trajectory:
                px = int((x-min_x)*sx) + 10
                pz = int((z-min_z)*sz) + 10
                pz = h - pz
                pts.append((px, pz))

            for i in range(1, len(pts)):
                cv2.line(canvas, pts[i-1], pts[i], (0,255,0), 2)

        canvas_resized = cv2.resize(canvas, (w, h))
        combined = np.hstack((frame_bgr, canvas_resized))

        cv2.imshow(self.window_name, combined)
        cv2.waitKey(1)
        return combined

    def close(self):
        cv2.destroyWindow(self.window_name)
