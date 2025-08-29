# CodeCourse — платформа для обучения программированию🎓  

Онлайн-платформа для изучения программирования с поддержкой курсов, уроков, 
ролей пользователей (преподаватели и студенты), а также управлением доступом через группы и права.

---

## 📌 Описание  
Цель проекта — предоставить базовый каркас для онлайн-школы.  

Основные функции:  
- Создание курсов
- Добавление уроков к курсам
- Разделение ролей пользователей: **преподаватели** и **студенты** 
- Управление доступом с помощью **групп и прав**
- Возможность быстро заполнить проект тестовыми данными и так же легко их удалить

---

## ⚙️ Установка  
1. Клонируйте репозиторий:  
   ```bash
   git clone https://github.com/ElviraOndar/otus-django-project
   cd otus-django-project
   ```
   
2. Создайте виртуальное окружение:
   ```bash
   python3 -m venv .venv
   ```
   Активируйте виртуальное окружение:

   - На Mac/Linux:
      ```bash
      source .venv/bin/activate
      ```
   - На Windows (PowerShell):
      ```bash
      .venv\Scripts\Activate.ps1
      ```

3. Установите зависимости:  
   ```bash
   pip install -r requirements.txt
   pip install python-decouple
   ```
4. Настройка секретного ключа:

- Сгенерируйте ключ:
 ```bash
   python -c "import secrets; print(secrets.token_urlsafe())"
   ```
- Создайте файл .env в корне проекта и добавьте:
```bash
   SECRET_KEY=ваш_уникальный_секретный_ключ
   ```
- В settings.py используйте:
```bash
   from decouple import config
  SECRET_KEY = config('SECRET_KEY')
   ```

5. Примените миграции:  
   ```bash
   python manage.py migrate
   ```
6. Создайте суперпользователя (для доступа в админку):  
   ```bash
   python manage.py createsuperuser
   ```
   
---

## 🚀 Использование

1. Запуск сервера:  
   ```bash
   python manage.py runserver
   ```
   После запуска проект будет доступен по адресу:
👉 http://127.0.0.1:8000

2. Заполнение тестовыми данными:  
   ```bash
   python manage.py seed_data
   ```
   Это создаст:
- Группы teachers и students с нужными правами
- Двух преподавателей (teacher1, teacher2)
- 6 студентов (student1, student2... student6)
- 2 курса и по 2 урока для каждого курса
- Запишет всех студентов на оба курса
🔑 Пароль для всех пользователей: password123

✅ Пример входа

- Логин: teacher1, Пароль: password123

- Логин: student1, Пароль: password123

3. Удаление тестовых данных
   ```bash
   python manage.py seed_data --flush
   ```

