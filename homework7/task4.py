import requests

url = "https://jsonplaceholder.typicode.com/posts/999999"  # несуществующий ресурс

response = requests.get(url)

if response.status_code == 200:
    print("Успешно!")
    print(response.json())
elif response.status_code == 400:
    print("Ошибка 400: Неверный запрос.")
elif response.status_code == 404:
    print("Ошибка 404: Ресурс не найден.")
else:
    print(f"Ошибка {response.status_code}: {response.text}")
