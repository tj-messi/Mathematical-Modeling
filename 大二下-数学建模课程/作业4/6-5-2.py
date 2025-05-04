from scipy.integrate import solve_ivp
import numpy as np
from math import factorial
import matplotlib.pyplot as plt

def equation(x, y):
    y1, y2 = y
    dy1dx = y2
    dy2dx = -y1 * np.cos(x)
    return [dy1dx, dy2dx]

# 初始条件和求解区间
sol = solve_ivp(equation, [0, 2], [1, 0], t_eval=np.linspace(0, 2, 1000))

# 幂级数解（前5项）
def series_solution(x):
    return (1 - (1/factorial(2))*x**2 + (2/factorial(4))*x**4 - 
           (9/factorial(6))*x**6 + (55/factorial(8))*x**8)

# 绘图
x_series = np.linspace(0, 2, 1000)
plt.plot(x_series, series_solution(x_series), 'P-', label='Series Approximation')
plt.plot(sol.t, sol.y[0], '*-r', label='Numerical Solution')
plt.legend()
plt.grid()
plt.show()