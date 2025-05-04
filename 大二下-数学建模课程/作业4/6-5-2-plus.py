from scipy.integrate import solve_ivp
import numpy as np
from math import factorial
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

# ================== Series Solution ==================
def series_solution(x):
    """Power series approximation (first 5 terms)"""
    return (1 - (1/factorial(2))*x**2 + (2/factorial(4))*x**4 - 
           (9/factorial(6))*x**6 + (55/factorial(8))*x**8)

# ================== Numerical Solution ==================
def equation(x, y):
    """First-order system for y'' + y cos(x) = 0"""
    y1, y2 = y
    dy1dx = y2
    dy2dx = -y1 * np.cos(x)
    return [dy1dx, dy2dx]

# Numerical solution with high accuracy
sol = solve_ivp(equation, [0, 2], [1, 0], 
                t_eval=np.linspace(0, 2, 1000),
                method='DOP853', rtol=1e-8, atol=1e-8)

# ================== Analysis ==================
x_vals = sol.t
y_num = sol.y[0]  # Numerical solution
y_series = series_solution(x_vals)  # Series approximation

# 1. Absolute error
abs_error = np.abs(y_num - y_series)

# 2. Relative error (with safeguard against division by zero)
relative_error = np.abs(y_num - y_series) / (np.abs(y_num) + 1e-12)

# 3. Residual analysis (for numerical solution)
def residual(x, y, y_prime, y_double_prime):
    """Compute residual of y'' + y cos(x) = 0"""
    return y_double_prime + y * np.cos(x)

# Numerical derivatives
y_prime_num = np.gradient(y_num, x_vals)
y_double_prime_num = np.gradient(y_prime_num, x_vals)
residuals = residual(x_vals, y_num, y_prime_num, y_double_prime_num)

# ================== Plotting ==================
plt.figure(figsize=(14, 10))

# ----- Main plot: Solutions -----
plt.subplot(2, 2, (1, 2))
plt.plot(x_vals, y_num, 'b-', lw=2, label='Numerical Solution')
plt.plot(x_vals, y_series, 'r--', lw=1.5, label='Series Approximation')
plt.xlabel('x')
plt.ylabel('y(x)')
plt.title('Solution Comparison: y\'\' + y cos(x) = 0')
plt.legend()
plt.grid(True)

# Add zoom area indicator
zoom_x = (1.5, 2.0)
zoom_rect = Rectangle((zoom_x[0], -0.2), zoom_x[1]-zoom_x[0], 0.4, 
                     linewidth=1, edgecolor='k', facecolor='none', linestyle='--')
plt.gca().add_patch(zoom_rect)
plt.text(zoom_x[0], -0.25, 'Zoom Area', ha='left')

# ----- Subplot 1: Absolute Error -----
plt.subplot(2, 2, 3)
plt.semilogy(x_vals, abs_error, 'g-', lw=1.5)
plt.xlabel('x')
plt.ylabel('Absolute Error (log scale)')
plt.title('Absolute Error Analysis')
plt.grid(True, which='both')

# ----- Subplot 2: Zoomed Comparison -----
plt.subplot(2, 2, 4)
zoom_mask = (x_vals >= zoom_x[0]) & (x_vals <= zoom_x[1])
plt.plot(x_vals[zoom_mask], y_num[zoom_mask], 'b-', lw=2, label='Numerical')
plt.plot(x_vals[zoom_mask], y_series[zoom_mask], 'r--', lw=1.5, label='Series')
plt.xlabel('x')
plt.ylabel('y(x)')
plt.title(f'Zoomed View ({zoom_x[0]} < x < {zoom_x[1]})')
plt.legend()
plt.grid(True)

plt.tight_layout()

# ================== Statistics ==================
print("\n===== Error Statistics =====")
print(f"Max Absolute Error: {np.max(abs_error):.2e}")
print(f"Mean Absolute Error: {np.mean(abs_error):.2e}")
print(f"Max Relative Error: {np.max(relative_error)*100:.2f}%")
print(f"Mean Relative Error: {np.mean(relative_error)*100:.2f}%")
print(f"Max Residual: {np.max(np.abs(residuals)):.2e}")

# ================== Residual Plot ==================
plt.figure(figsize=(10, 5))
plt.semilogy(x_vals, np.abs(residuals), 'm-', lw=1.5)
plt.xlabel('x')
plt.ylabel('Residual (log scale)')
plt.title('Residual Analysis: |y\'\' + y cos(x)|')
plt.grid(True, which='both')
plt.show()