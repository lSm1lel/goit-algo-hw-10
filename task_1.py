"""Завдання 1. Видача решти жадібним алгоритмом і динамічним програмуванням."""

from statistics import median
from timeit import repeat


COINS = [50, 25, 10, 5, 2, 1]


def validate_amount(amount):
    if not isinstance(amount, int) or amount < 0:
        raise ValueError("Сума має бути невід'ємним цілим числом")


def find_coins_greedy(amount):
    """Вибирає найбільші доступні монети та повертає їхні кількості."""
    validate_amount(amount)
    result = {}
    for coin in COINS:
        count, amount = divmod(amount, coin)
        if count:
            result[coin] = count
    return result


def find_min_coins(amount):
    """Знаходить мінімальну кількість монет методом динамічного програмування."""
    validate_amount(amount)
    # min_count[s] зберігає найменшу кількість монет для суми s.
    min_count = [amount + 1] * (amount + 1)
    last_coin = [0] * (amount + 1)
    min_count[0] = 0

    for current_sum in range(1, amount + 1):
        for coin in COINS:
            if coin <= current_sum:
                candidate = min_count[current_sum - coin] + 1
                if candidate < min_count[current_sum]:
                    min_count[current_sum] = candidate
                    last_coin[current_sum] = coin

    result = {}
    remaining = amount
    while remaining > 0:
        coin = last_coin[remaining]
        result[coin] = result.get(coin, 0) + 1
        remaining -= coin
    return result


def compare_algorithms():
    """Повертає реальний час одного виклику для кількох сум."""
    results = []
    for amount in [113, 1000, 10_000, 100_000]:
        row = {"amount": amount}
        for name, function, number in [
            ("greedy", find_coins_greedy, 10_000),
            ("dynamic", find_min_coins, 10),
        ]:
            # Повільніший алгоритм запускаємо менше разів, але порівнюємо
            # час ОДНОГО виклику: тривалість серії ділимо на number.
            samples = repeat(lambda: function(amount), number=number, repeat=5)
            row[name] = median(samples) / number
        results.append(row)
    return results


def main():
    amount = 113
    greedy = find_coins_greedy(amount)
    dynamic = find_min_coins(amount)
    print("Завдання 1. Видача решти")
    print("Номінали монет:", COINS)
    print("Сума:", amount)
    print("Жадібний алгоритм:", greedy, "Кількість монет:", sum(greedy.values()))
    print("Динамічне програмування:", dynamic, "Кількість монет:", sum(dynamic.values()))
    print("\nМедіанний час одного виклику, мкс:")
    print(f"{'Сума':>10} {'Жадібний':>15} {'Динамічний':>15}")
    for row in compare_algorithms():
        print(f"{row['amount']:>10} {row['greedy'] * 1e6:>15.3f} "
              f"{row['dynamic'] * 1e6:>15.3f}")


if __name__ == "__main__":
    main()
