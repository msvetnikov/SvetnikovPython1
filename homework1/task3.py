class NegativeNumberFound(Exception): pass
class EvenNumberFound(Exception): pass

try:
    nums = list(map(int, input("Целые через пробел: ").split()))
    if any(n < 0 for n in nums): raise NegativeNumberFound("Есть отрицательное число.")
    if any(n % 2 == 0 for n in nums): raise EvenNumberFound("Есть чётное число.")
    print("Сумма:", sum(nums))
except ValueError:
    print("Ошибка: нужны целые числа.")
except (NegativeNumberFound, EvenNumberFound) as e:
    print("Пользовательское исключение:", e)
