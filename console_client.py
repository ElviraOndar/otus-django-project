import requests

# Получаем токен
data = {
    'username': 'student1',
    'password': 'stud_pass1',
}

url = 'http://127.0.0.1:8000/api/token/'  # JWT endpoint
response = requests.post(url, json=data)

print("Response:", response.text)
assert response.status_code == 200, f"Ошибка авторизации: {response.status_code}"

access_token = response.json()['access']

# Проверяем доступ с токеном: обращаемся к списку курсов
headers = {
    'Authorization': f'Bearer {access_token}',
}

url = 'http://127.0.0.1:8000/api/courses/'
response = requests.get(url, headers=headers)

assert response.status_code == 200, f"Ошибка доступа: {response.status_code}"

print("✅ JWT работает! Статус:", response.status_code)

