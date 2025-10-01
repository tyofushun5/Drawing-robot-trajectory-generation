import os

import cv2 as cv
import numpy as np
import pandas as pd


script_dir = os.path.dirname(__file__)
parent_dir = os.path.dirname(script_dir)
img_dir = os.path.join(script_dir, 'images')
image_filename = 'git.png' #Your image filename
image_path = os.path.join(parent_dir, img_dir, image_filename)

desired_points = 800
scale = 1
dt_per_point = 0.05

img = cv.imread(image_path)

img = cv.resize(img, (600, 600))
H, W, _ = img.shape

gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
img_canny = cv.Canny(gray, 100, 200)

contours, _ = cv.findContours(
    img_canny,
    cv.RETR_EXTERNAL,
    cv.CHAIN_APPROX_NONE
)
if len(contours) == 0:
    print("輪郭が検出されませんでした。")

max_contour = max(contours, key=cv.contourArea)

all_points = max_contour.reshape(-1, 2)
total_points = len(all_points)
if total_points == 0:
    print("最大輪郭が空でした。")

if total_points > desired_points:
    idxs = np.linspace(0, total_points - 1, desired_points, dtype=int)
    sampled_points = all_points[idxs]
else:
    sampled_points = all_points

x0, y0 = sampled_points[0]

excel_data = []
for i, (x, y) in enumerate(sampled_points):
    # 時間 t
    t = i * dt_per_point

    X_world = (x - x0) * scale

    Y_world = ((H - y) - (H - y0)) * scale

    excel_data.append([t, X_world, Y_world])

df = pd.DataFrame(excel_data, columns=["t", "x", "y"])
df.to_excel("coordinates.xlsx", index=False)

print(
    f"元の点数: {total_points} → サンプリング後: {len(sampled_points)} 点")
print(
    f"スケール={scale} で縮小し出力しました。")
