try:
    import math
    x = float(input("Число для sqrt: "))
    if x < 0: raise ValueError("sqrt отрицательного невозможен для вещественных.")
    print("sqrt:", math.sqrt(x))
except ImportError:
    print("Ошибка: модуль math недоступен.")
except ValueError as e:
    print("Ошибка:", e)
