# Репозиторий заданий

*Для всех приложений требуется Python 3.xx*

---

## Настройка

В корне репозитория создай виртуальное окружение и установи зависимости для всех проектов:

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Дальше при работе с любым заданием нужно активировать этот venv 

---

## Запуск приложений и тестов

### 01-calculator

**Запуск приложения:**
```bash
cd 01-calculator
python calculator.py
```

**Тесты:**
```bash
cd 01-calculator
python -m unittest test_calculator -v
```

---

### 02-chat

**Запуск приложения:**
```bash
cd 02-chat/megachat
python manage.py migrate
python manage.py runserver
```

**Тесты:**
```bash
cd 02-chat/megachat
python manage.py test app
```

---

### 03-ToDoList

**Запуск приложения:**
```bash
cd 03-ToDoList/Todolist
python manage.py migrate
python manage.py runserver
```

В браузере: http://127.0.0.1:8000/

**Тесты:**
```bash
cd 03-ToDoList/Todolist
python manage.py test app
```
