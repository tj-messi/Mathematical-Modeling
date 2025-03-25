import numpy as np
from scipy.optimize import minimize

# 约束函数，对应 MATLAB 的 fun3_2
def constraint_fun(x):
    th0 = np.array([243, 236, 220.5, 159, 230, 52])
    th = th0 + x
    
    x0 = np.array([150, 85, 150, 145, 130, 0])
    y0 = np.array([140, 85, 155, 50, 150, 0])
    
    constraints = []
    for i in range(5):
        for j in range(i + 1, 6):
            aij = 4 * (np.sin(np.radians((th[i] - th[j]) / 2)))**2
            bij = 2 * ((x0[i] - x0[j]) * (np.cos(np.radians(th[i])) - np.cos(np.radians(th[j]))) +
                       (y0[i] - y0[j]) * (np.sin(np.radians(th[i])) - np.sin(np.radians(th[j]))))
            cij = (x0[i] - x0[j])**2 + (y0[i] - y0[j])**2 - 64
            constraints.append(bij**2 - 4 * aij * cij)

    return np.array(constraints)

# 目标函数，对应 MATLAB 的 fun3_1
def objective_fun(delta):
    return np.sum(delta**2)

# 初始值
x0 = np.random.rand(6) * 60 - 30  # 生成 [-30, 30] 之间的随机数

# 约束
constraints = {'type': 'ineq', 'fun': constraint_fun}

# 边界
bounds = [(-30, 30)] * 6

# 使用 scipy.optimize 的 minimize 进行优化
result = minimize(objective_fun, x0, method='SLSQP', bounds=bounds, constraints=constraints)

# 输出结果
print("Optimal delta:", result.x)
print("Objective function value:", result.fun)
print("Optimization success:", result.success)
print("Message:", result.message)
