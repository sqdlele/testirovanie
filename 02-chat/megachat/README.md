# Чат

Чат (комнаты, сообщения по WebSocket.)

`Необходим python 3.XX`

**Запуск:**  -> `py -m venv venv`  -> `cd megachat` -> `pip install -r requirements.txt` -> `python manage.py migrate` -> `python manage.py runserver`

---
## Тесты

файл: `app/tests.py`, 6 тестов.

---
**test_create_room** - Создание комнаты через форму -> в БД одна комната с нужным именем и slug длины 6. 

**test_delete_room** - Удаление комнаты по slug -> в БД комнат не остаётся. 

**test_send_and_get_messages** - Отправка сообщения в комнату -> оно появляется в `room.messages`, api get_messages возвращает тот же список. 

**test_empty_message_not_saved** - Отправка пустого/пробельного текста -> сообщение не создаётся, `room.messages` пуста. 

**test_index_shows_rooms_and_room_page_has_messages** - Комната с сообщением -> на главной она в `context['rooms']`, на странице комнаты — в `context['recent_messages']`. 

**test_username_in_session_then_send_message**  Ввод имени в комнате -> имя в сессии, отправка сообщения -> в БД сообщение с этим `user_name`. 

**Запуск тестов:** `python manage.py test app`

