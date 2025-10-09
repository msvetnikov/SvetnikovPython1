items = ["яблоко", "банан", "вишня", "дыня"]
try:
    i = int(input(f"Индекс 0..{len(items)-1}: "))
    print("Элемент:", items[i])
except ValueError:
    print("Ошибка: нужен целый индекс.")
except IndexError:
    print("Ошибка: индекс вне диапазона.")
