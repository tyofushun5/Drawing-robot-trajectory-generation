import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

W = 0.146
scale = 0.001

df = pd.read_excel("coordinates.xlsx")
df = df.sort_values(by="t").drop_duplicates(subset="t")

t_array = df["t"].to_numpy()
x_array = df["x"].to_numpy() * scale
y_array = df["y"].to_numpy() * scale

vx = np.zeros_like(x_array)
vy = np.zeros_like(y_array)

for i in range(1, len(t_array) - 1):
    dt_i = t_array[i + 1] - t_array[i - 1]
    vx[i] = (x_array[i + 1] - x_array[i - 1]) / dt_i
    vy[i] = (y_array[i + 1] - y_array[i - 1]) / dt_i

dt_front = t_array[1] - t_array[0]
vx[0] = (x_array[1] - x_array[0]) / dt_front
vy[0] = (y_array[1] - y_array[0]) / dt_front

dt_back = t_array[-1] - t_array[-2]
vx[-1] = (x_array[-1] - x_array[-2]) / dt_back
vy[-1] = (y_array[-1] - y_array[-2]) / dt_back

v = np.sqrt(vx**2 + vy**2)
theta = np.arctan2(vy, vx)
theta_unwrapped = np.unwrap(theta)

omega = np.zeros_like(theta_unwrapped)
for i in range(1, len(theta_unwrapped) - 1):
    dt_i = t_array[i + 1] - t_array[i - 1]
    omega[i] = (theta_unwrapped[i + 1] - theta_unwrapped[i - 1]) / dt_i

omega[0] = (theta_unwrapped[1] - theta_unwrapped[0]) / dt_front
omega[-1] = (theta_unwrapped[-1] - theta_unwrapped[-2]) / dt_back

v_R = v + (omega * W / 2.0)
v_L = v - (omega * W / 2.0)

x_reconstructed = [x_array[0]]
y_reconstructed = [y_array[0]]
theta_reconstructed = [theta_unwrapped[0]]

for i in range(len(v_R) - 1):
    v_avg = 0.5 * (v_R[i] + v_L[i])
    omega_i = (v_R[i] - v_L[i]) / W

    delta_t = t_array[i+1] - t_array[i]

    theta_new = theta_reconstructed[-1] + omega_i * delta_t
    x_new = x_reconstructed[-1] + v_avg * np.cos(theta_new) * delta_t
    y_new = y_reconstructed[-1] + v_avg * np.sin(theta_new) * delta_t

    theta_reconstructed.append(theta_new)
    x_reconstructed.append(x_new)
    y_reconstructed.append(y_new)


plt.figure(figsize=(10, 6))
plt.plot(x_array, y_array, 'o-', label="Original Data", alpha=0.7)
plt.plot(x_reconstructed, y_reconstructed, '-', label="Reconstructed", color="blue")
plt.xlabel("X [m]")
plt.ylabel("Y [m]")
plt.axis('equal')
plt.title("One-Stroke Trajectory Reconstruction")
plt.legend()
plt.grid(True)
plt.show()

result_df = pd.DataFrame({
    "t": t_array,
    "v_R": v_R,
    "v_L": v_L,
})
result_df = result_df.round(4)
result_df.to_excel("wheel_speeds.xlsx", index=False)
print("完了！'wheel_speeds.xlsx' に連続値の左右車輪速度を出力しました。")
