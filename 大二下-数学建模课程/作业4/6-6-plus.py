import numpy as np
from scipy.integrate import solve_ivp
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

# ================== 参数优化 ==================
d = 100       # 初始水平距离 (m)
v1 = 1        # 水流速度 (m/s)
v2 = 2        # 小船速度 (m/s)
k = v1 / v2   # 速度比

def analytic_solution(x):
    """小船航迹的解析解公式"""
    return (d / 2) * ((x/d)**(1 - k) - (x/d)**(1 + k))

# ================== 事件检测优化 ==================
def event_x_zero(t, xy):
    """当x < 1m时终止计算"""
    return xy[0] - 1  # 检测x=1时触发终止
event_x_zero.terminal = True
event_x_zero.direction = -1

# ================== 数值解求解优化 ==================
def dydt(t, xy):
    x, y = xy
    denominator = np.sqrt(x**2 + y**2) + 1e-6  # 增大epsilon提高稳定性
    return [-v2 * x / denominator, v1 - v2 * y / denominator]

# 控制计算规模：减少时间点数量
sol = solve_ivp(
    dydt,
    [0, 200],
    [d, 0],
    method='DOP853',
    events=event_x_zero,  # 添加事件检测
    rtol=1e-6,            # 适当降低精度要求
    atol=1e-6,
    t_eval=np.linspace(0, 200, 2000)  # 减少到2000个点
)

# ================== 数据对齐优化 ==================
# 提取有效数据（去除事件触发后的无效点）
valid = sol.t <= sol.t_events[0][0]
x_num = sol.y[0][valid]
y_num = sol.y[1][valid]

# 使用线性插值替代三次样条
y_interp = interp1d(
    np.flip(x_num),  # 输入必须单调递增
    np.flip(y_num),
    kind='linear',
    bounds_error=False,
    fill_value=np.nan
)

# ================== 误差分析优化 ==================
x_eval = np.linspace(1, 100, 500)  # 从x=1开始避免边界问题
y_numeric = y_interp(x_eval)
valid_mask = ~np.isnan(y_numeric)

# ================== 简化绘图 ==================
plt.figure(figsize=(12, 6))

# 主图
plt.plot(x_eval[valid_mask], analytic_solution(x_eval[valid_mask]), 
        'b-', label='解析解')
plt.plot(x_eval[valid_mask], y_numeric[valid_mask], 
        'r--', label='数值解')
plt.xlabel('x (米)'), plt.ylabel('y (米)')
plt.title('优化后的小船航线对比')
plt.legend(), plt.grid(True)

# 误差子图
plt.figure(figsize=(12, 6))
abs_error = np.abs(y_numeric[valid_mask] - analytic_solution(x_eval[valid_mask]))
plt.semilogy(x_eval[valid_mask], abs_error, 'g-')
plt.xlabel('x (米)'), plt.ylabel('difference')
plt.title('difference')
plt.grid(True)

plt.show()

# ================== 控制台优先输出 ==================
print("\n===== 运行状态报告 =====")
print(f"实际计算时间区间: [0, {sol.t[-1]:.2f}]秒")
print(f"有效数据点数: {len(x_num)}")
print(f"最大绝对误差: {np.nanmax(abs_error):.2e}米")

