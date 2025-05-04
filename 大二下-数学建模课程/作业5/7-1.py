import numpy as np
from scipy.stats import t, norm
from scipy.stats import ttest_1samp

# 1. 初始化数据
x0 = np.array([1050, 1100, 1120, 1250, 1280])  # 样本数据
n = len(x0)  # 样本大小 n = 5
alpha = 0.10  # 置信水平 1-alpha = 0.9

# 2. 计算样本均值和样本标准差
x_mean = np.mean(x0)  # 样本均值
S = np.std(x0, ddof=1)  # 样本标准差，ddof=1 表示自由度为 n-1

# 3. 计算 t 分布的分位数
Ta = t.ppf(1 - alpha/2, n-1)  # t 分布的 1-alpha/2 分位数，自由度为 n-1

# 4. 计算置信区间
standard_error = S / np.sqrt(n)  # 标准误差
margin = Ta * standard_error  # 置信区间的半宽
ci_lower = x_mean - margin  # 置信区间下限
ci_upper = x_mean + margin  # 置信区间上限

# 5. 输出结果
print(f"样本均值: {x_mean}")
print(f"样本标准差: {S}")
print(f"t 分位数 (t_{1-alpha/2}, {n-1}): {Ta}")
print(f"置信区间: ({ci_lower}, {ci_upper})")

# 6. 使用 scipy 的 t 检验直接计算置信区间（验证）
ci = t.interval(alpha=1-alpha, df=n-1, loc=x_mean, scale=standard_error)
print(f"使用 t.interval 计算的置信区间: {ci}")