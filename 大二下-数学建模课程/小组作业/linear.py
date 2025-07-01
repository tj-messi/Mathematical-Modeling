from scipy.optimize import linprog

# 定义目标函数系数
c = [1, 1, 1]  # 对应 z = x1 + x2 + x3

# 定义不等式约束的系数（注意调整为小于等于的形式）
A = [
    [-2, -7.5, -3],  # 2x1 + 7.5x2 + 3x3 >= 1000 转换为 -2x1 - 7.5x2 - 3x3 <= -1000
    [-20, -5, -10]   # 20x1 + 5x2 + 10x3 >= 30000 转换为 -20x1 - 5x2 - 10x3 <= -30000
]

# 定义不等式的右侧常数
b = [-1000, -30000]

# 定义变量的边界
x_bounds = (0, None)  # x1 >= 0
y_bounds = (0, None)  # x2 >= 0
z_bounds = (0, None)  # x3 >= 0

# 使用线性规划求解最小化问题
result = linprog(c, A_ub=A, b_ub=b, bounds=[x_bounds, y_bounds, z_bounds], method='simplex')

# 输出结果
print("最优解：", result.x)
print("最小值：", result.fun)
