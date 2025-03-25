import numpy as np
from scipy.optimize import minimize

# 定义目标函数 fun3_2
def fun3_2(x):
    # 初始化参数
    g = np.array([])  # 空数组
    # 8 个不支持在线性约束条件的整数
    th0 = np.array([243, 236, 220.5, 159, 230, 52])
    th = th0 + x
    x0 = np.array([150, 85, 150, 145, 130, 0])
    y0 = np.array([140, 85, 155, 50, 150, 0])
    k = 1
    
    # 循环 i 从 1 到 5
    for i in range(1, 6):  # Python 中 range(1, 6) 是 1 到 5
        # 循环 j 从 i+1 到 6
        for j in range(i + 1, 7):  # range(i+1, 7) 是 i+1 到 6
            # 计算 aij, bij, cij
            aij = 4 * (np.sin(th[i-1] - th[j-1]) / 2)**2
            bij = 2 * ((x0[i-1] - x0[j-1]) * (np.cos(th[i-1]) - np.cos(th[j-1])) + 
                      (y0[i-1] - y0[j-1]) * (np.sin(th[i-1]) - np.sin(th[j-1])))
            cij = (x0[i-1] - x0[j-1])**2 + (y0[i-1] - y0[j-1])**2 - 64
            # 计算 f(k)
            f_k = bij**2 - 4 * aij * cij
            k = k + 1
            # 将 f_k 添加到 g 中
            g = np.append(g, f_k)
    
    return g

# 主程序
# 定义 delta
fun3_1 = lambda delta: np.sum(delta**2)

# 初始猜测值
x0 = np.zeros(6)  # 对应 MATLAB 中的 x = 0

# 使用 fmincon 的等价函数 minimize
# 约束条件：-30 * ones(6,1), 30 * ones(6,1)
bounds = [(-30, 30)] * 6  # 6 个变量，每个变量的范围是 [-30, 30]

# 随机数种子
np.random.seed(1)

# 调用 minimize 进行优化
result = minimize(fun3_1, x0, method='SLSQP', bounds=bounds, constraints={'type': 'ineq', 'fun': lambda x: -fun3_2(x)})

# 输出结果
print("优化结果：")
print("x 的值：", result.x)
print("目标函数值：", result.fun)
print("是否成功：", result.success)
print("消息：", result.message)