import numpy as np
from scipy.optimize import minimize

# 定义目标函数：总成本（生产成本 + 存储成本）
def objective(vars):
    x1, x2, x3 = vars
    # 计算库存
    s1 = x1 - 40  # 第一季度末库存
    s2 = s1 + x2 - 60  # 第二季度末库存
    # 生产成本
    cost1 = 50 * x1 + 0.2 * x1**2
    cost2 = 50 * x2 + 0.2 * x2**2
    cost3 = 50 * x3 + 0.2 * x3**2
    # 存储成本
    storage_cost = 4 * s1 + 4 * s2
    # 总成本
    return cost1 + cost2 + cost3 + storage_cost
# 定义约束条件
constraints = [
    {'type': 'ineq', 'fun': lambda vars: vars[0] - 40},  # x1 = 80
    {'type': 'ineq', 'fun': lambda vars: (vars[0] ) + vars[1] - 100 },  # s1 + x2 = 120
    {'type': 'eq', 'fun': lambda vars: (vars[0] + vars[1] ) + vars[2] - 180},  # s2 + x3 = 160
    {'type': 'ineq', 'fun': lambda vars: 100 - vars[0]},  # x1 <= 100
    {'type': 'ineq', 'fun': lambda vars: 100 - vars[1]},  # x2 <= 100
    {'type': 'ineq', 'fun': lambda vars: 100 - vars[2]},  # x3 <= 100
]
# 初始猜测值
initial_guess = [80, 50, 50]  # x1, x2, x3
# 变量的非负约束
bounds = [(0, None), (0, None), (0, None)]  # x1, x2, x3 >= 0
# 求解优化问题
result = minimize(objective, initial_guess, method='SLSQP', bounds=bounds, constraints=constraints)
# 输出结果
if result.success:
    x1, x2, x3 = result.x
    s1 = x1 - 40
    s2 = s1 + x2 - 60
    total_cost = result.fun
    print(f"优化成功！")
    print(f"第一季度生产数量 x1: {x1:.2f} 台")
    print(f"第二季度生产数量 x2: {x2:.2f} 台")
    print(f"第三季度生产数量 x3: {x3:.2f} 台")
    print(f"第一季度末库存 s1: {s1:.2f} 台")
    print(f"第二季度末库存 s2: {s2:.2f} 台")
    print(f"第一季度生产成本: {50 * x1 + 0.2 * x1**2:.2f} 元")
    print(f"第二季度生产成本: {50 * x2 + 0.2 * x2**2:.2f} 元")
    print(f"第三季度生产成本: {50 * x3 + 0.2 * x3**2:.2f} 元")
    print(f"存储成本: {4 * s1 + 4 * s2:.2f} 元")
    print(f"总成本: {total_cost:.2f} 元")
else:
    print("优化失败！")
    print(result.message)