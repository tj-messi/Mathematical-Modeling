import numpy as np
import matplotlib.pyplot as plt

# 1. 输入数据
x = np.array([1, 2, 3, 4, 5, 6, 7, 8])
y = np.array([15.3, 20.5, 27.4, 36.6, 49.1, 65.6, 87.87, 117.6])

# 2. 对数变换
Y = np.log(y)  # Y = ln(y)

# 3. 最小二乘法拟合 Y = A + bx
# 构造正规方程的系数矩阵
n = len(x)
sum_x = np.sum(x)
sum_x2 = np.sum(x**2)
sum_Y = np.sum(Y)
sum_xY = np.sum(x * Y)

# 正规方程：[[n, sum_x], [sum_x, sum_x2]] @ [A, b] = [sum_Y, sum_xY]
A_matrix = np.array([[n, sum_x], [sum_x, sum_x2]])
B_matrix = np.array([sum_Y, sum_xY])

# 解线性方程组
A, b = np.linalg.solve(A_matrix, B_matrix)

# 4. 还原参数 a 和 b
a = np.exp(A)  # a = e^A

print(f"拟合参数：a = {a:.2f}, b = {b:.4f}")
print(f"拟合模型：y = {a:.2f} * e^({b:.4f}x)")

# 5. 绘制拟合曲线和数据点
# 生成用于绘图的 x 值（更密集的点）
x_fit = np.linspace(1, 8, 100)
y_fit = a * np.exp(b * x_fit)  # 拟合值

# 绘图
plt.figure(figsize=(8, 6))
plt.scatter(x, y, color='red', label='Data Points', s=100)  # 原始数据点
plt.plot(x_fit, y_fit, color='blue', label=f'Fit: y = {a:.2f}e^({b:.4f}x)')  # 拟合曲线
plt.xlabel('x')
plt.ylabel('y')
plt.title('Exponential Fit using Least Squares')
plt.legend()
plt.grid(True)
plt.show()

# 6. 计算拟合误差（可选）
y_pred = a * np.exp(b * x)
error = np.sum((y - y_pred)**2)
print(f"误差平方和：{error:.2f}")