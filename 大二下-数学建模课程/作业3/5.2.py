import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import CloughTocher2DInterpolator
from mpl_toolkits.mplot3d import Axes3D

# 1. 读取数据
data = np.loadtxt(r'D:\Mathematical Modeling\Mathematical-Modeling\大二下-数学建模课程\作业3\5.2.txt', delimiter=',')  # 读取 data51.txt 文件
x = data[:, 0]  # x 坐标
y = data[:, 1]  # y 坐标
z = data[:, 2]  # height 值

# 2. 定义插值网格
x0 = np.arange(0, 5601, 400)  # 原始 x 坐标范围 [0, 5600]，间隔 400
y0 = np.arange(4800, -401, -400)  # 原始 y 坐标范围 [4800, 0]，间隔 400
X0, Y0 = np.meshgrid(x0, y0)  # 原始网格

# 3. 创建插值网格（间隔为 50）
x_new = np.arange(0, 5601, 50)  # 新 x 坐标范围 [0, 5600]，间隔 50
y_new = np.arange(4800, -51, -50)  # 新 y 坐标范围 [4800, 0]，间隔 50
X, Y = np.meshgrid(x_new, y_new)  # 新网格

# 4. 进行二维插值
# 将原始数据点 (x, y, z) 整理为插值输入
points = np.vstack((x, y)).T  # (x, y) 坐标点
values = z  # 对应的 height 值

# 使用 CloughTocher2DInterpolator 进行插值（类似 MATLAB 的 cscape）
interp = CloughTocher2DInterpolator(points, values)

# 计算插值后的值
Z = interp(np.vstack((X.ravel(), Y.ravel())).T).reshape(X.shape)

# 5. 绘制等高线图和三维表面图
plt.figure(figsize=(12, 5))

# 等高线图
plt.subplot(1, 2, 1)
contour = plt.contourf(X, Y, Z, 10, cmap='jet')  # 10 个等高线，颜色映射为 jet
plt.colorbar(contour, label='Height')  # 添加颜色条
plt.xlabel('X')
plt.ylabel('Y')
plt.title('Contour Plot')

# 三维表面图
ax = plt.subplot(1, 2, 2, projection='3d')
surf = ax.plot_surface(X, Y, Z, cmap='jet')
plt.colorbar(surf, ax=ax, shrink=0.5, aspect=5, label='Height')  # 添加颜色条
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Height')
ax.set_title('3D Surface Plot')

# 调整布局并显示
plt.tight_layout()
plt.show()