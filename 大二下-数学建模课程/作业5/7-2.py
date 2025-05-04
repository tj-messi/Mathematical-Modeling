import numpy as np
from scipy.stats import chi2

# 样本数据
data = [
    15.0, 15.8, 15.2, 15.1, 15.9, 14.7, 14.8, 15.5, 15.6, 15.3,
    15.1, 15.3, 15.0, 15.6, 15.7, 14.8, 14.5, 14.2, 14.9, 14.9,
    15.2, 15.0, 15.3, 15.6, 15.1, 14.9, 14.2, 14.6, 15.8, 15.2,
    15.9, 15.2, 15.0, 14.9, 14.8, 14.5, 15.1, 15.5, 15.5, 15.1,
    15.1, 15.0, 15.3, 14.7, 14.5, 15.5, 15.0, 14.7, 14.6, 14.2
]

# 已知的分组信息
intervals = [float('-inf'), 14.71, 14.88, 15.05, 15.22, 15.39, 15.56, float('inf')]
observed_freq = [11, 3, 10, 10, 4, 4, 8]  # 观测频数 m_i
theoretical_prob = [0.1974, 0.1261, 0.1506, 0.1545, 0.1360, 0.1028, 0.1325]  # 理论概率 p_i

# 样本总数
n = 50

# 计算理论频数 n * p_i
theoretical_freq = [n * p for p in theoretical_prob]

# 计算χ²统计量
chi_square_stat = 0
for i in range(len(observed_freq)):
    chi_square_stat += (observed_freq[i] - theoretical_freq[i])**2 / theoretical_freq[i]

print(f"计算的χ²统计量: {chi_square_stat:.4f}")

# 自由度 df = k - r - 1
k = len(intervals) - 1  # 分组数
r = 2  # 估计了均值和方差
df = k - r - 1
print(f"自由度: {df}")

# 置信水平 α = 0.05，查找临界值
alpha = 0.05
critical_value = chi2.ppf(1 - alpha, df)
print(f"临界值 (χ²_0.05({df})): {critical_value:.4f}")

# 比较χ²统计量和临界值
if chi_square_stat < critical_value:
    print("χ²统计量 < 临界值，不拒绝原假设，直径距离服从正态分布。")
else:
    print("χ²统计量 >= 临界值，拒绝原假设，直径不服从正态分布。")