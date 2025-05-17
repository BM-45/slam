from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.pyplot as plt

class TrajectoryVisualizer:
    @staticmethod
    def plot(trajectory, save_path=None):
        traj = np.array(trajectory) 
        fig = plt.figure(figsize=(8, 8))
        ax = fig.add_subplot(111, projection='3d')
        ax.plot(traj[:, 0], traj[:, 1], traj[:, 2], '-o', markersize=2)

        ax.set_xlabel('X [m]')
        ax.set_ylabel('Y [m]')
        ax.set_zlabel('Z [m]')
        ax.set_title('Estimated Vehicle Trajectory (3D)')
        ax.view_init(elev=30, azim=-60)

        x_min, x_max = traj[:,0].min(), traj[:,0].max()
        y_min, y_max = traj[:,1].min(), traj[:,1].max()
        z_min, z_max = traj[:,2].min(), traj[:,2].max()

        max_range = max(x_max - x_min, y_max - y_min, z_max - z_min) / 2.0

        x_mid = (x_max + x_min) * 0.5
        y_mid = (y_max + y_min) * 0.5
        z_mid = (z_max + z_min) * 0.5

    
        ax.set_xlim(x_mid - max_range, x_mid + max_range)
        ax.set_ylim(y_mid - max_range, y_mid + max_range)
        ax.set_zlim(z_mid - max_range, z_mid + max_range)

        if save_path:
            fig.savefig(save_path)
        plt.show()
