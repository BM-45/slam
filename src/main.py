#!/usr/bin/env python3
import os
import argparse
import cv2
import numpy as np
import imageio

from data_module.frame_data      import FrameData
from data_module.config          import Config
from include.feature_extractor   import FeatureExtractor
from include.matcher             import FlannMatcher
from include.essential_matrix    import EssentialMatrixEstimator
from include.pose_estimator      import PoseEstimator
from include.optimizer           import PoseOptimizer
from utils.trajectory_visualizer import TrajectoryVisualizer
from utils.video_visualizer    import VideoVisualizer

def run_slam(base_path, date, drive, kf_dist, ba_window=5):
    # --- OUTPUT FILES (always overwrite) ---
    for fn in ('trajectory.png', 'slam_live.gif', 'est_traj.txt'):
        if os.path.exists(fn):
            os.remove(fn)
            print(f"Removed old {fn}")

    print(f"▶ Starting SLAM on {date} / {drive}")

    # 1) Load data & intrinsics
    data = FrameData(base_path, date, drive)
    print(f"Loaded {len(data)} frames")
    config = Config(data.K)
    N = len(data)

    # 2) Modules (no mapping/keyframe logic)
    extractor = FeatureExtractor(nfeatures=1500)
    matcher   = FlannMatcher()
    ess_est   = EssentialMatrixEstimator(config.focal, config.pp)
    pose_est  = PoseEstimator(config.focal, config.pp)
    optimizer = PoseOptimizer(max_trans=1.0)

    # 3) Visualization
    vis     = VideoVisualizer(window_name='SLAM Live')
    gif_buf = []

    # 4) SLAM state
    curr_pose  = np.eye(4)
    trajectory = [curr_pose[:3,3].copy()]
    poses      = [curr_pose.copy()]

    # 5) First frame init
    prev_gray    = data.get_frame(0)
    prev_kp, prev_des = extractor.extract(prev_gray)
    frame0_vis = vis.update(prev_gray, trajectory)
    if frame0_vis is not None and frame0_vis.size:
        gif_buf.append(cv2.cvtColor(frame0_vis, cv2.COLOR_BGR2RGB))

    # 6) Main loop (no keyframe/map building)
    for idx in range(1, N):
        print(f"Frame {idx}/{N}")
        gray = data.get_frame(idx)
        kp, des = extractor.extract(gray)
        if prev_des is None or des is None:
            prev_kp, prev_des = kp, des
            continue

        matches = matcher.match(prev_des, des)
        if len(matches) < 8:
            prev_kp, prev_des = kp, des
            continue

        pts1 = np.float32([prev_kp[m.queryIdx].pt for m in matches])
        pts2 = np.float32([kp[m.trainIdx].pt      for m in matches])

        E, mask = ess_est.compute(pts1, pts2)
        if E is None:
            prev_kp, prev_des = kp, des
            continue

        R, t, mask = pose_est.recover(E, pts1, pts2)
        if not optimizer.filter(R, t):
            prev_kp, prev_des = kp, des
            continue

        # update pose
        T = np.eye(4)
        T[:3,:3], T[:3,3] = R, t.flatten()
        curr_pose = curr_pose @ T
        trajectory.append(curr_pose[:3,3].copy())
        poses.append(curr_pose.copy())

        # live view
        vis_frame = vis.update(gray, trajectory)
        if vis_frame is not None and vis_frame.size:
            gif_buf.append(cv2.cvtColor(vis_frame, cv2.COLOR_BGR2RGB))

        prev_kp, prev_des = kp, des

    # 7) Finish
    print("Finished processing all frames.")
    vis.close()
    cv2.destroyAllWindows()

    # Static trajectory plot
    TrajectoryVisualizer.plot(trajectory, save_path='trajectory.png')
    print("Saved trajectory plot to trajectory.png")

    # Animated GIF
    if gif_buf:
        imageio.mimsave('slam_live.gif', gif_buf, duration=0.05)
        print("Saved animated GIF to slam_live.gif")
    else:
        print("No frames to save for slam_live.gif")

    # KITTI‐style trajectory dump
    with open('est_traj.txt', 'w') as f:
        for T in poses:
            for row in T[:3,:4]:
                f.write(" ".join(f"{x:.6f}" for x in row) + " ")
            f.write("")
    print("Saved estimated trajectory to est_traj.txt")


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--base_path', required=True, help='KITTI raw data folder')
    p.add_argument('--date',      default='2011_09_26')
    p.add_argument('--drive',     default='2011_09_26_drive_0002_sync')
    p.add_argument('--kf_dist',   type=float, default=0.5)
    p.add_argument('--ba_window', type=int,   default=5)
    args = p.parse_args()

    run_slam(args.base_path,
             args.date,
             args.drive,
             args.kf_dist,
             args.ba_window)
