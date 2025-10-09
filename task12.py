try:
    a = float(input("Первое число: "))
    b = float(input("Второе число: "))
    print("Результат:", a / b)
except ZeroDivisionError:
    print("Ошибка: деление на ноль.")
except ValueError:
    print("Ошибка: введите числа.")
finally:
    print("Готово.")
