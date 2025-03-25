import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import CubicSpline
from scipy.integrate import trapz

# 1. 加载数据
data = np.loadtxt(r'D:\Mathematical Modeling\Mathematical-Modeling\大二下-数学建模课程\作业3\5.4.txt', delimiter=',', dtype=str)
t0 = []
h0 = []
for row in data:
    t0.append(float(row[0]))
    height = row[1]
    h0.append(float(height))

t0 = np.array(t0)
h0 = np.array(h0)

# 2. 参数定义
hs = 0.3024  # 单位换算因子，1 E = 0.3024 m
D = 57 * hs  # 水箱直径，单位：m
h = h0 *hs  # 水位数据，单位：m（数据中水位单位是 10⁻² m）
t = t0 / 3600  # 时间单位转换为小时

# 3. 计算体积 V
V = (np.pi / 4) * D**2 * h  # 体积，单位：m³

# 4. 计算流出流量 f(t) = -dV/dt
dv = np.gradient(V, t)
dv2 = -dv  # 流出流量为正

# 5. 移除泵水阶段的数据
no1 = np.where(h0 == -1)[0]  # 找到泵水阶段的索引
no2 = []
for i in range(0, len(no1), 2):  # 泵水阶段成对出现
    start = no1[i] - 1
    end = no1[i+1] + 1
    no2.extend(range(start, end+1))

# 非泵水阶段的数据
tt = np.delete(t, no2)
dv2_clean = np.delete(dv2, no2)

# 6. 使用三次样条插值拟合 f(t)
cs = CubicSpline(tt, dv2_clean, bc_type='natural')  # 自然边界条件的三次样条插值
tt0 = np.linspace(0, tt[-1], 1000)  # 插值点
fdv = cs(tt0)  # 插值后的流出流量

# 7. 绘制流出流量散点图和插值曲线
plt.figure(figsize=(10, 6))
plt.plot(tt, dv2_clean, '*', label='Data Points')
plt.plot(tt0, fdv, '-', label='Cubic Spline Interpolation')
plt.xlabel('Time (hours)')
plt.ylabel('Flow Rate (m³/h)')
plt.title('Flow Rate vs Time (Cubic Spline Interpolation)')
plt.legend()
plt.grid(True)
plt.show()

# 8. 计算 24 小时用水量
tt0_24h = np.linspace(0, 24, 241)  # 0 到 24 小时，241 个点
fdv_24h = cs(tt0_24h)
I = trapz(fdv_24h, tt0_24h)
print(f"24 小时内的总用水量: {I:.1f} m³")