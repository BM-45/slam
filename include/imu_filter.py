import numpy as np

class IMUKalmanFilter:
    def __init__(self, dt, accel_noise=0.1, gyro_noise=0.01, vo_noise=0.05):
        # State vector x = [pos(3), vel(3), ori(4 as quaternion)]
        self.dt = dt
        # Initialize state
        self.x = np.zeros((10,))
        self.x[6] = 1.0  # quaternion w = 1
        # State covariance
        self.P = np.eye(10) * 0.1
        # Process noise
        self.Q = np.diag([0.01]*3 + [accel_noise]*3 + [gyro_noise]*4)
        # Measurement noise (VO position + orientation)
        self.R = np.diag([vo_noise]*3 + [vo_noise]*3)

    def predict(self, accel, gyro):
        # Unpack
        p = self.x[0:3]
        v = self.x[3:6]
        q = self.x[6:10]  # quaternion [w, x, y, z]

        # Convert quaternion to rotation matrix
        qw, qx, qy, qz = q
        R = np.array([
            [1-2*(qy*qy+qz*qz),   2*(qx*qy-qz*qw),   2*(qx*qz+qy*qw)],
            [2*(qx*qy+qz*qw),   1-2*(qx*qx+qz*qz),   2*(qy*qz-qx*qw)],
            [2*(qx*qz-qy*qw),     2*(qy*qz+qx*qw), 1-2*(qx*qx+qy*qy)]
        ])

        # State propagation
        p_pred = p + v * self.dt + 0.5 * (R @ accel) * self.dt**2
        v_pred = v + (R @ accel) * self.dt
        # Quaternion update: q_dot = 0.5 * Omega(gyro) * q
        omega = np.array([0, *gyro])
        q_dot = 0.5 * self._quat_mul(omega, q)
        q_pred = q + q_dot * self.dt
        q_pred /= np.linalg.norm(q_pred)

        # Update state
        self.x[0:3] = p_pred
        self.x[3:6] = v_pred
        self.x[6:10] = q_pred

        # Jacobian F approx identity (small-angle) – for full accuracy derive analytically
        F = np.eye(10)
        # Covariance propagation
        self.P = F @ self.P @ F.T + self.Q

    def update_vo(self, pos_meas, ori_meas):
        # Measurement vector z = [p_x, p_y, p_z, yaw, pitch, roll]
        # Here we only fuse position and yaw/pitch/roll from quaternion
        # Convert ori_meas quaternion to euler
        yaw, pitch, roll = self._quat_to_euler(ori_meas)
        z = np.hstack((pos_meas, [yaw, pitch, roll]))

        # Prediction measurement
        p = self.x[0:3]
        q = self.x[6:10]
        ypr = self._quat_to_euler(q)
        h = np.hstack((p, ypr))

        # Jacobian H
        H = np.zeros((6, 10))
        H[0:3, 0:3] = np.eye(3)
        # Orientation to euler Jacobian approximate: use identity on quaternion part
        H[3:6, 6:9] = np.eye(3)

        # Innovation
        y = z - h
        # Covariance
        S = H @ self.P @ H.T + self.R
        K = self.P @ H.T @ np.linalg.inv(S)

        # State update
        self.x += K @ y
        # Covariance update
        self.P = (np.eye(10) - K @ H) @ self.P

    def get_state(self):
        return self.x[0:3].copy(), self.x[3:6].copy(), self.x[6:10].copy()

    def _quat_mul(self, a, b):
        # Hamilton product a ⊗ b
        aw, ax, ay, az = a
        bw, bx, by, bz = b
        return np.array([
            aw*bw - ax*bx - ay*by - az*bz,
            aw*bx + ax*bw + ay*bz - az*by,
            aw*by - ax*bz + ay*bw + az*bx,
            aw*bz + ax*by - ay*bx + az*bw
        ])

    def _quat_to_euler(self, q):
        # Convert quaternion to yaw, pitch, roll
        w, x, y, z = q
        # yaw (z-axis rotation)
        t0 = +2.0 * (w*z + x*y)
        t1 = +1.0 - 2.0 * (y*y + z*z)
        yaw = np.arctan2(t0, t1)
        # pitch (y-axis)
        t2 = +2.0 * (w*y - z*x)
        t2 = np.clip(t2, -1.0, 1.0)
        pitch = np.arcsin(t2)
        # roll (x-axis)
        t3 = +2.0 * (w*x + y*z)
        t4 = +1.0 - 2.0 * (x*x + y*y)
        roll = np.arctan2(t3, t4)
        return yaw, pitch, roll
