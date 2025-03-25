import numpy as np
from scipy.optimize import minimize

# 目标函数 (最大化问题转化为最小化 -f(x))
def objective(x):
    return -(2*x[0] + 3*x[0]**2 + 3*x[1] + x[1]**2 + x[2])
# 约束条件
def constraint1(x):
    return 10 - (x[0] + 2*x[0]**2 + x[1] + 2*x[1]**2 + x[2])  # ≤ 10
def constraint2(x):
    return 50 - (x[0] + x[0]**2 + x[1] + x[1]**2 - x[2])  # ≤ 50
def constraint3(x):
    return 40 - (2*x[0] + x[0]**2 + 2*x[1] + x[2])  # ≤ 40
def constraint4(x):
    return x[0]**2 + x[2] - 2  # 等式约束 x1^2 + x3 = 2
def constraint5(x):
    return x[0] + 2*x[1] - 1  # ≥ 1 (转换为 ≤ -1)
# 变量的边界 (x1 >= 0, x2, x3 无约束)
bounds = [(0, None), (None, None), (None, None)]
# 约束定义
constraints = [
    {'type': 'ineq', 'fun': constraint1},  # 不等式约束
    {'type': 'ineq', 'fun': constraint2},  
    {'type': 'ineq', 'fun': constraint3},  
    {'type': 'eq', 'fun': constraint4},    # 等式约束
    {'type': 'ineq', 'fun': constraint5}   
]
# 选择合适的初始点（根据 MATLAB 参考解）
x0 = np.random.rand(3)
# 求解非线性规划问题，使用 SLSQP 算法
solution = minimize(objective, x0, bounds=bounds, constraints=constraints, method='SLSQP')
# 输出最优解
print("Optimal solution: x1 =", solution.x[0], ", x2 =", solution.x[1], ", x3 =", solution.x[2])
print("Maximum value of objective function:", -solution.fun)