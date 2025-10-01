import matplotlib.pyplot as plt
import pandas as pd

excel_file = 'wheel_speeds.xlsx'

df = pd.read_excel(excel_file)

required_columns = ['t', 'v_R', 'v_L']
for col in required_columns:
    if col not in df.columns:
        raise ValueError(f"Column '{col}' is missing from the Excel file.")


t = df['t'].values
v_R = df['v_R'].values
v_L = df['v_L'].values

plt.figure(figsize=(12, 6))  # グラフのサイズを指定

plt.plot(t, v_R, linestyle='-', color='r', label='Right Wheel Speed')

plt.plot(t, v_L, linestyle='-', color='b', label='Left Wheel Speed')

plt.title('Left and Right Wheel Speeds Over Time')
plt.xlabel('Time (seconds)')
plt.ylabel('Speed (m/s)')

plt.legend()

plt.grid(True)

plt.tight_layout()

plt.show()
