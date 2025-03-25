import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import CubicSpline
from scipy.integrate import trapz

# 1. 读取水位数据
data = np.loadtxt(r'D:\Mathematical Modeling\Mathematical-Modeling\大二下-数学建模课程\作业3\5.4.txt', delimiter=',', dtype=str)
times = []
heights = []
for row in data:
    time = float(row[0])
    height = row[1]
    times.append(time)
    if height == '':  # 标记泵水阶段
        heights.append(-1)  # 用 -1 表示无效数据
    else:
        heights.append(float(height) / 100)  # 转换为米

times = np.array(times)
heights = np.array(heights)

# 2. 计算体积 V
A = 1.95  # 底面积，单位：m²
def volume(h):
    return A * h

# 计算时间（单位：小时）
t = times / 3600.0

# 3. 移除泵水阶段的数据
# 找到泵水阶段 (h = -1) 的位置
no1 = np.where(heights == -1)[0]
no2 = []
for i in range(0, len(no1), 2):  # 泵水阶段成对出现
    start = no1[i]
    end = no1[i+1]
    no2.extend(range(start, end+1))

# 非泵水阶段的数据
tt = np.delete(t, no2)
h_clean = np.delete(heights, no2)

# 计算非泵水阶段的体积
V_clean = volume(h_clean)

# 4. 计算流出流量 f(t) = -dV/dt
dv = np.gradient(V_clean, tt)
f = -dv  # 流出流量为正

# 5. 插值 f(t)
cs = CubicSpline(tt, f, bc_type='natural')
tt0 = np.linspace(0, tt[-1], 1000)
f_fine = cs(tt0)

# 6. 绘制流出流量散点图和插值曲线
plt.figure(figsize=(10, 6))
plt.plot(tt, f, '*', label='Data Points')
plt.plot(tt0, f_fine, '-', label='Spline Interpolation')
plt.xlabel('Time (hours)')
plt.ylabel('Flow Rate (m³/h)')
plt.title('Flow Rate vs Time')
plt.legend()
plt.grid(True)
plt.show()

# 7. 计算 24 小时用水量
tt_24h = np.linspace(0, 24, 241)  # 0 到 24 小时，241 个点
f_24h = cs(tt_24h)
I = trapz(f_24h, tt_24h)
print(f"24 小时内的总用水量: {I:.1f} m³")