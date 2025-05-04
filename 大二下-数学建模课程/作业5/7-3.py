import numpy as np
import pandas as pd
import statsmodels.api as sm
from statsmodels.formula.api import ols

# 输入数据
data = np.array([
    [98, 93, 103, 92, 110],  # j=1
    [100, 108, 118, 99, 111],  # j=2
    [129, 140, 108, 105, 116]  # j=3
])

# 转换为 DataFrame
J, T = data.shape  # J=3, T=5
rows = []
for j in range(J):
    for t in range(T):
        rows.append([j+1, t+1, data[j, t]])
df = pd.DataFrame(rows, columns=['j', 't', 'X'])
df['j'] = df['j'].astype('category')
df['t'] = df['t'].astype('category')

# 拟合双因素方差分析模型（无交互项）
model = ols('X ~ C(j) + C(t)', data=df).fit()
anova_table = sm.stats.anova_lm(model, typ=2)

# 输出 ANOVA 表
print("双因素方差分析结果（无交互项）：")
print(anova_table)

# 提取 F 值并进行假设检验
alpha = 0.05
F_crit_A = 3.8853  # F_0.05(2, 12)
F_crit_B = 3.26    # F_0.05(4, 12)

F_A = anova_table['F']['C(j)']
F_B = anova_table['F']['C(t)']

# 结论
print("\n假设检验结论：")
print(f"因素 j: H0: m1 = m2 = m3, H1: m1, m2, m3 不全相等")
print(f"F = {F_A:.2f}, {'拒绝 H0' if F_A > F_crit_A else '接受 H0'} (临界值 F_0.05(2,12) = {F_crit_A})")

print(f"\n因素 t: H0: m.1 = m.2 = m.3 = m.4 = m.5, H1: m.1, m.2, m.3, m.4, m.5 不全相等")
print(f"F = {F_B:.2f}, {'拒绝 H0' if F_B > F_crit_B else '接受 H0'} (临界值 F_0.05(4,12) = {F_crit_B})")