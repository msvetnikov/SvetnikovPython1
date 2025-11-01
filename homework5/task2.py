import threading
import time

def print_numbers(name):
    for i in range(1, 11):
        print(f"{name}: {i}")
        time.sleep(1)

if __name__ == "__main__":
    threads = []

    # создаём и запускаем 3 потока
    for n in range(3):
        t = threading.Thread(target=print_numbers, args=(f"thread-{n+1}",))
        threads.append(t)
        t.start()

    # ждём завершения всех потоков
    for t in threads:
        t.join()

    print("all done")
