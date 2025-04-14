import pandas as pd
import matplotlib.pyplot as plt

# Excelファイルのパスを指定
excel_file = 'wheel_speeds.xlsx'  # 実際のファイルパスに置き換えてください

# Excelファイルからデータを読み込む
df = pd.read_excel(excel_file)

# 必要な列が存在するか確認
required_columns = ['t', 'v_R', 'v_L']
for col in required_columns:
    if col not in df.columns:
        raise ValueError(f"Column '{col}' is missing from the Excel file.")

# 時間軸と車輪速度の取得
t = df['t'].values       # 時間 (秒)
v_R = df['v_R'].values   # 右車輪速度
v_L = df['v_L'].values   # 左車輪速度
# 折れ線グラフの作成
plt.figure(figsize=(12, 6))  # グラフのサイズを指定

# 右車輪速度をプロット（マーカーなし）
plt.plot(t, v_R, linestyle='-', color='r', label='Right Wheel Speed')

# 左車輪速度をプロット（マーカーなし）
plt.plot(t, v_L, linestyle='-', color='b', label='Left Wheel Speed')

# グラフのタイトルとラベルを設定
plt.title('Left and Right Wheel Speeds Over Time')
plt.xlabel('Time (seconds)')
plt.ylabel('Speed (m/s)')  # 速度の単位に応じて変更してください

# 凡例を表示
plt.legend()

# グリッドを表示（オプション）
plt.grid(True)

# レイアウトを調整
plt.tight_layout()

# グラフを表示
plt.show()
