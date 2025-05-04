from scipy.integrate import solve_ivp
import numpy as np
import matplotlib.pyplot as plt

def bessel_equations(x, y, n=0.5):
    y1, y2 = y
    dy1dx = y2
    dy2dx = (n**2 / x**2 - 1) * y1 - y2 / x
    return [dy1dx, dy2dx]

# Exact solution
def exact_solution(x):
    return np.sin(x) * np.sqrt(2 * np.pi / x)

# Avoid x=0 due to singularity, start slightly above
x0 = 0.1
# Initial conditions adjusted for starting at x0
y0 = [exact_solution(x0), 
      np.sqrt(2*np.pi/x0)*np.cos(x0) - np.sin(x0)*np.sqrt(2*np.pi/x0**3)/2]

# Numerical solution from x0 to 8
sol = solve_ivp(bessel_equations, [x0, 8], y0, t_eval=np.linspace(x0, 8, 1000))



# Create plot
plt.figure(figsize=(10, 6))
x_plot = np.linspace(0.1, 8, 1000)  # Start slightly above 0

# Numerical solution (from solve_ivp)
plt.plot(sol.t, sol.y[0], 'b-', linewidth=2, label='Numerical Solution')

# Exact solution
plt.plot(x_plot, exact_solution(x_plot), 'r--', linewidth=2, label='Exact Solution')

plt.xlabel('x', fontsize=12)
plt.ylabel('y(x)', fontsize=12)
plt.title('Solution of Bessel Equation (n=1/2) from 0 to 8', fontsize=14)
plt.legend(fontsize=12)
plt.grid(True, linestyle='--', alpha=0.7)
plt.xlim(0, 8)  # Ensure we show from 0 to 8

# Highlight the singularity at x=0
plt.annotate('Singularity at x=0', xy=(0.2, 2), xytext=(1, 3),
             arrowprops=dict(facecolor='black', shrink=0.05))

plt.show()