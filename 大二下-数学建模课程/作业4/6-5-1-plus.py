from scipy.integrate import solve_ivp
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

# ================== Exact Solution ==================
def exact_solution(x):
    """Exact solution for Bessel equation (n=0.5)"""
    return np.sin(x) * np.sqrt(2 * np.pi / x)

def exact_derivative(x):
    """Derivative of exact solution (for initial conditions)"""
    return np.sqrt(2*np.pi/x)*np.cos(x) - np.sin(x)*np.sqrt(2*np.pi/x**3)/2

# ================== Numerical Solution ==================
def bessel_equations(x, y, n=0.5):
    """First-order system for Bessel equation"""
    y1, y2 = y
    dy1dx = y2
    dy2dx = (n**2 / x**2 - 1) * y1 - y2 / x
    return [dy1dx, dy2dx]

# Avoid singularity at x=0
x0 = 0.1
x_end = 8
y0 = [exact_solution(x0), exact_derivative(x0)]

# Numerical solution with high accuracy
sol = solve_ivp(bessel_equations, [x0, x_end], y0, 
                t_eval=np.linspace(x0, x_end, 1000),
                method='DOP853', rtol=1e-8, atol=1e-8)

# ================== Analysis ==================
x_vals = sol.t
y_num = sol.y[0]
y_exact = exact_solution(x_vals)

# 1. Absolute error
abs_error = np.abs(y_num - y_exact)

# 2. Relative error (with safeguard against division by zero)
relative_error = np.abs(y_num - y_exact) / (np.abs(y_exact) + 1e-12)

# 3. Residual analysis
def residual(x, y, y_prime, y_double_prime):
    """Compute residual of Bessel equation"""
    return x**2 * y_double_prime + x * y_prime + (x**2 - 0.25) * y

# Numerical derivatives
y_prime_num = np.gradient(y_num, x_vals)
y_double_prime_num = np.gradient(y_prime_num, x_vals)
residuals = residual(x_vals, y_num, y_prime_num, y_double_prime_num)

# ================== Plotting ==================
plt.figure(figsize=(14, 10))

# ----- Main plot: Solutions -----
plt.subplot(2, 2, (1, 2))
plt.plot(x_vals, y_num, 'b-', lw=2, label='Numerical Solution')
plt.plot(x_vals, y_exact, 'r--', lw=1.5, label='Exact Solution')
plt.xlabel('x')
plt.ylabel('y(x)')
plt.title('Bessel Equation Solution Comparison (n=0.5)')
plt.legend()
plt.grid(True)

# Add zoom area indicator
zoom_x = (3, 4)
zoom_rect = Rectangle((zoom_x[0], -0.5), zoom_x[1]-zoom_x[0], 1, 
                     linewidth=1, edgecolor='k', facecolor='none', linestyle='--')
plt.gca().add_patch(zoom_rect)
plt.text(zoom_x[0], -0.6, 'Zoom Area', ha='left')

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
plt.plot(x_vals[zoom_mask], y_exact[zoom_mask], 'r--', lw=1.5, label='Exact')
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
plt.title('Bessel Equation Residual Analysis')
plt.grid(True, which='both')
plt.show()