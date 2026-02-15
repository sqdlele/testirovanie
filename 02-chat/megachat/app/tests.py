import json
from django.test import TestCase, Client
from django.urls import reverse
from .models import Room, Message


class ChatTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_create_room(self):
        # сценарий
        #  пользователь создаёт комнату -> в бд появляется одна комната, редирект в неё
        self.client.post(reverse('app:create_room'), {'name': 'Чат'})
        self.assertEqual(Room.objects.count(), 1)
        room = Room.objects.first()
        self.assertEqual(room.name, 'Чат')
        self.assertEqual(len(room.slug), 6)

    def test_delete_room(self):
        # Сценарий: 
        # комната есть -> пользователь удаляет её -> в бд комнат нет
        room = Room.objects.create(name='Удалить', slug='deltst')
        self.client.post(reverse('app:delete_room', kwargs={'slug': room.slug}))
        self.assertEqual(Room.objects.count(), 0)

    def test_send_and_get_messages(self):
        # Сценарий: 
        # в комнате отправляем сообщение -> оно попадает в room.messages, api возвращает тот же список
        room = Room.objects.create(name='Чат', slug='r1')
        self.client.post(
            reverse('app:send_message'),
            json.dumps({'room': 'r1', 'content': 'Привет'}),
            content_type='application/json',
        )
        self.assertEqual(room.messages.count(), 1)
        self.assertEqual(room.messages.first().content, 'Привет')
        r = self.client.get(reverse('app:get_messages', kwargs={'slug': 'r1'}))
        self.assertEqual(len(r.json()['messages']), 1)
        self.assertEqual(r.json()['messages'][0]['content'], 'Привет')

    def test_empty_message_not_saved(self):
        # Сценарий: 
        # отправляем пустой текст -> сообщение не создаётся
        room = Room.objects.create(name='Чат', slug='r2')
        self.client.post(
            reverse('app:send_message'),
            json.dumps({'room': 'r2', 'content': '   '}),
            content_type='application/json',
        )
        self.assertEqual(room.messages.count(), 0)

    def test_index_shows_rooms_and_room_page_has_messages(self):
        # Сценарий: 
        # создаём комнату с сообщением -> на главной она в списке, в комнате -> в recent_messages
        room = Room.objects.create(name='Комната', slug='idx1')
        Message.objects.create(room=room, user_name='А', content='Сообщение')
        r_index = self.client.get(reverse('app:index'))
        rooms = r_index.context['rooms']
        self.assertEqual(list(rooms), [room])
        r_room = self.client.get(reverse('app:room', kwargs={'slug': 'idx1'}))
        self.assertEqual(r_room.context['room'], room)
        self.assertEqual(len(r_room.context['recent_messages']), 1)
        self.assertEqual(r_room.context['recent_messages'][0].content, 'Сообщение')

    def test_username_in_session_then_send_message(self):
        # Сценарий: 
        # входим в комнату с именем -> имя в сессии, отправленное сообщение сохраняется с этим именем
        Room.objects.create(name='Чат', slug='r3')
        self.client.post(
            reverse('app:room', kwargs={'slug': 'r3'}),
            {'set_username': '1', 'user_name': 'Юзер'},
        )
        self.assertEqual(self.client.session['user_name'], 'Юзер')
        self.client.post(
            reverse('app:send_message'),
            json.dumps({'room': 'r3', 'content': 'Текст'}),
            content_type='application/json',
        )
        msg = Message.objects.get(room__slug='r3')
        self.assertEqual(msg.user_name, 'Юзер')
        self.assertEqual(msg.content, 'Текст')
