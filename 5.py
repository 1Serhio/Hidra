from math import sin, pi
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation

def create_grid(length, time_slice, n, m, u0, mu):
    grid = []
    h = length / n
    t = time_slice / m
    for j in range(m):
        grid.append([0] * n)
    for i in range(n):
        grid[0][i] = u0(i * h)
    for j in range(m):
        grid[j][0] = mu(j * t)
    return grid, h, t

def u0_0(x):
    return 1.0 if 1 <= x <= 2 else 0.0

def u0_1(x):
    if x < 1 or x > 2:
        return 0
    elif x >= 1 and x < 1.5:
        return 2 * (x - 1)
    else:
        return 1 - 2 * (x - 1.5)

def u0_2(x):
    if x < 1 or x > 2:
        return 0
    else:
        return 0.5 * (1 + sin(2 * pi * (x - 1) - pi / 2))

def mu(t):
    return 0

def solve_single(t, grid, nu, h, tau):
    prev = grid[t - 1]
    curr = grid[t]
    n = len(curr)
    c1 = 1.0 / tau
    c2 = 1.0 / (2 * h)
    c3 = nu / (h ** 2)
    alpha = [0.0] * n
    beta = [0.0] * n
    alpha[1] = 0.0
    beta[1] = curr[0]
    for i in range(1, n - 1):
        u_val = prev[i]
        A = u_val * c2 + c3
        B = -c1 - 2 * c3
        C = -u_val * c2 + c3
        F = -c1 * prev[i]
        alpha[i + 1] = -C / (B + A * alpha[i])
        beta[i + 1] = (F - A * beta[i]) / (B + A * alpha[i])
    curr[-1] = beta[-1] / (1 - alpha[-1])
    for i in range(n - 2, -1, -1):
        curr[i] = alpha[i + 1] * curr[i + 1] + beta[i + 1]

def solve(grid, a, h, tau):
    for t in range(1, len(grid)):
        solve_single(t, grid, a, h, tau)

a = 0.05
w = 15
h = 10
n = w * 10
m = h * 20

targets = [u0_0, u0_1, u0_2]

if __name__ == '__main__':
    s = int(input('u0: '))
    if s < 1 or s > len(targets):
        print('u0 should be 1, 2 or 3')
        exit(1)
    target = targets[s - 1]

    grid, hx, tau = create_grid(w, h, n, m, target, mu)
    solve(grid, a, hx, tau)

    fig, ax = plt.subplots()
    x = np.linspace(0, w, n)
    ax.xaxis.set_major_locator(plt.MultipleLocator(1))

    def update(frame):
        plt.cla()
        plt.title(f"t = {tau * frame:.2f}")
        ax.plot(x, grid[frame], '-')
        plt.legend()

    def print_table(frame, x, grid, tau):
        print(f"\nTable of values at t = {tau * frame:.2f}")
        print("-" * 30)
        print(f"{'x':>8} | {'u(x,t)':>10}")
        print("-" * 30)
        for i in range(0, len(x), 1):  # Шаг 5 для компактности
            print(f"{x[i]:>8.3f} | {grid[frame][i]:>10.6f}")
        print("-" * 30)

    fr = input('Time: ')
    anim = len(fr) == 0
    if not anim:
        fr = int(float(fr) / tau)
        print_table(fr, x, grid, tau)
        update(fr)
    else:
        ani = animation.FuncAnimation(fig, update, frames=m, interval=30, repeat=False)

    plt.show()
