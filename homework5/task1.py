import threading
import time

def print_squares():
    for i in range(1, 11):
        print(f"square {i} = {i ** 2}")
        time.sleep(0.1)  # небольшая пауза, чтобы потоки чередовались

def print_cubes():
    for i in range(1, 11):
        print(f"cube   {i} = {i ** 3}")
        time.sleep(0.1)

if __name__ == "__main__":
    # создаём два потока
    t1 = threading.Thread(target=print_squares)
    t2 = threading.Thread(target=print_cubes)

    # запускаем потоки
    t1.start()
    t2.start()

    # ждём завершения обоих
    t1.join()
    t2.join()

    print("done")