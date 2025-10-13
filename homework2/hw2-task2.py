# считаем общую стоимость заказа из файла формата:

file_name = "prices.txt"
total = 0

f = open(file_name, "r")
for line in f:            # проходимся по строкам
    line = line.strip()   # убираем пробелы и переносы
    if line == "":        # пропустить пустые строки
        continue
    parts = line.split("\t")  # разделяем по табуляции
    name = parts[0]           # название
    qty = int(parts[1])       # количество
    price = int(parts[2])     # цена за единицу
    total = total + qty * price  # добавить стоимость позиции
f.close()
print("Итого:", total)
