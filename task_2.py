"""Завдання 2. Інтеграл x² на [0, 2] методом Монте-Карло."""

from pathlib import Path
import random


def f(x):
    return x ** 2


def monte_carlo_integral(function, a, b, num_points=100_000, seed=42):
    """Оцінює інтеграл через середнє значення функції у випадкових точках."""
    if not isinstance(num_points, int) or num_points <= 0:
        raise ValueError("Кількість точок має бути додатним цілим числом")
    rng = random.Random(seed)
    total = 0.0
    for _ in range(num_points):
        x = rng.uniform(a, b)
        total += function(x)
    return (b - a) * total / num_points


def compare_integrals():
    """Порівнює оцінки Монте-Карло з точним аналітичним результатом."""
    a, b = 0, 2
    exact = (b ** 3 - a ** 3) / 3
    results = []
    for num_points in [1000, 10_000, 100_000, 1_000_000]:
        estimate = monte_carlo_integral(f, a, b, num_points, seed=42)
        absolute_error = abs(estimate - exact)
        results.append({
            "points": num_points,
            "estimate": estimate,
            "absolute_error": absolute_error,
            "relative_error_percent": absolute_error / abs(exact) * 100,
        })
    return results


def draw_plot():
    """Зберігає графік функції та зафарбовану область інтегрування."""
    import matplotlib.pyplot as plt

    x = [-0.5 + 3 * i / 399 for i in range(400)]
    y = [f(value) for value in x]
    area_x = [2 * i / 200 for i in range(201)]
    area_y = [f(value) for value in area_x]

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(x, y, color="firebrick", linewidth=2, label="f(x) = x²")
    ax.fill_between(area_x, area_y, color="gray", alpha=0.3,
                    label="Площа під графіком на [0, 2]")
    ax.axvline(0, color="gray", linestyle="--")
    ax.axvline(2, color="gray", linestyle="--")
    ax.set(xlim=(-0.5, 2.5), ylim=(0, 6.5), xlabel="x", ylabel="f(x)",
           title="Інтеграл функції f(x) = x² від 0 до 2")
    ax.grid(alpha=0.25)
    ax.legend()
    fig.tight_layout()
    path = Path(__file__).resolve().parent / "integral_plot.png"
    fig.savefig(path, dpi=160)
    plt.close(fig)
    return path


def main():
    print("Завдання 2. Метод Монте-Карло")
    print("Функція: f(x) = x², межі інтегрування: [0, 2]")
    print(f"Аналітичний результат: 8/3 = {8 / 3:.10f}")
    print("Seed генератора випадкових чисел: 42")
    print(f"{'Точок':>10} {'Монте-Карло':>15} {'Абс. похибка':>15} {'Відн. похибка, %':>18}")
    for row in compare_integrals():
        print(f"{row['points']:>10} {row['estimate']:>15.8f} "
              f"{row['absolute_error']:>15.8f} {row['relative_error_percent']:>18.5f}")
    print("Графік збережено:", draw_plot())


if __name__ == "__main__":
    main()
