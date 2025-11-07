import requests

url = "https://jsonplaceholder.typicode.com/posts"

new_post = {
    "title": "Мой новый пост",
    "body": "Текст поста",
    "userId": 1
}

response = requests.post(url, json=new_post)
data = response.json()

print("Создан пост!")
print(f"ID: {data['id']}")
print(f"Содержимое: {data}")
