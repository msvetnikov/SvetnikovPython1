import requests

url = "https://jsonplaceholder.typicode.com/posts"

response = requests.get(url)

# Выводим заголовки
print("Заголовки ответа:")
for k, v in response.headers.items():
    print(f"{k}: {v}")

# Выводим первые 5 постов
print("\nПервые 5 постов:")
posts = response.json()

for post in posts[:5]:
    print(f"\nID: {post['id']}")
    print(f"Title: {post['title']}")
    print(f"Body: {post['body']}")
