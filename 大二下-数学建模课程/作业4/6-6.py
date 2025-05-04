import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt

# 定义参数
d = 100
v1 = 1
v2 = 2
k = v1 / v2

# 定义解析解函数
y_analytic = lambda x: d / 2 * ((x/d)**(1 - k) - (x/d)**(1 + k))

# 绘制解析解曲线
x_vals = np.linspace(0, d, 400)
plt.plot(x_vals, y_analytic(x_vals), label='Series Approximation')

# 定义微分方程的右端项
def dxy(t, xy):
    x, y = xy
    denominator = np.sqrt(x**2 + y**2) + 1e-8  # 防止除以零
    dxdt = -v2 * x / denominator
    dydt = v1 - v2 * y / denominator
    return [dxdt, dydt]

# 定义事件函数：当 x < 1e-3 时触发终止
def event_x_zero(t, xy):
    x, y = xy
    return x - 1e-3  # 当 x < 1e-3 时返回负值，触发事件
event_x_zero.terminal = True  # 事件触发后终止积分
event_x_zero.direction = -1   # 仅检测下降穿过零点的事件

# 求解微分方程（时间区间设为足够大的范围，如 [0, 1000]）
sol = solve_ivp(
    dxy,
    [0, 1000],                # 时间区间上限设为较大值
    [d, 0],                   # 初始条件
    method='RK45',
    events=event_x_zero,      # 绑定事件检测
    dense_output=True
)

# 提取渡河时间
crossing_time = sol.t_events[0][0]
print(f"渡河时间 = {crossing_time:.2f} 秒")

# 绘制数值解
plt.plot(sol.y[0], sol.y[1], 'r*', markersize=3, label='Numerical Solution')

# 图形设置
plt.xlabel('x (米)')
plt.ylabel('y (米)')
plt.gca().invert_xaxis()  # 反转x轴（从100到0）
plt.legend()
plt.grid(True)
plt.show()