# копируем содержимое одного файла в другой

src = "source.txt"        # исходный файл
dst = "destination.txt"   # файл назначения

f = open(src, "r")        # открываем файл
data = f.read()           # читаем
f.close()

g = open(dst, "w")        # открываем файл для записи
g.write(data)             # записываем текст в новый файл
g.close()

print("Готово: скопировано в", dst)
