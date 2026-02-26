from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from app.models import Poll, Choice, Vote


class PollCreationTests(TestCase):
    # Создание опроса: после POST опрос и варианты появляются в бд
    def setUp(self):
        User.objects.create_user('testuser', 't@t.com', 'pass')
        self.client.login(username='testuser', password='pass')

    def test_create_poll_appears_in_queryset(self):
        response = self.client.post(reverse('poll_create'), {
            'question': 'Лучший язык?',
            'choice_1': 'Python',
            'choice_2': 'JavaScript',
        })
        self.assertEqual(response.status_code, 302)
        polls = list(Poll.objects.all())
        self.assertEqual(len(polls), 1)
        self.assertEqual(polls[0].question, 'Лучший язык?')
        self.assertEqual(polls[0].created_by.username, 'testuser')
        choices = list(polls[0].choice_set.all())
        self.assertEqual(len(choices), 2)
        texts = [c.text for c in choices]
        self.assertIn('Python', texts)
        self.assertIn('JavaScript', texts)

    def test_poll_list_shows_created_polls(self):
        # сценарий: создаём опрос через модель — на странице списка он в context
        Poll.objects.create(question='Тестовый опрос')
        response = self.client.get(reverse('poll_list'))
        self.assertEqual(response.status_code, 200)
        poll_list = list(response.context['polls'])
        self.assertEqual(len(poll_list), 1)
        self.assertEqual(poll_list[0].question, 'Тестовый опрос')


class VotingLogicTests(TestCase):
    # логика голосования: один пользователь — один голосb, повторный голос не увеличивает счётчик

    def setUp(self):
        self.user = User.objects.create_user('voter', 'v@t.com', 'pass')
        self.poll = Poll.objects.create(question='Опрос')
        self.choice_a = Choice.objects.create(poll=self.poll, text='вариант A', votes=0)
        self.choice_b = Choice.objects.create(poll=self.poll, text='вариант B', votes=0)
        self.client.login(username='voter', password='pass')

    def test_vote_increments_choice_votes(self):
        self.client.post(reverse('poll_vote', args=[self.poll.pk]), {'choice': self.choice_a.pk})
        self.choice_a.refresh_from_db()
        self.assertEqual(self.choice_a.votes, 1)
        self.assertTrue(Vote.objects.filter(poll=self.poll, user=self.user, choice=self.choice_a).exists())

    def test_second_vote_same_user_does_not_increment(self):
        self.client.post(reverse('poll_vote', args=[self.poll.pk]), {'choice': self.choice_a.pk})
        self.client.post(reverse('poll_vote', args=[self.poll.pk]), {'choice': self.choice_a.pk})
        self.choice_a.refresh_from_db()
        self.assertEqual(self.choice_a.votes, 1)
        self.assertEqual(Vote.objects.filter(poll=self.poll, user=self.user).count(), 1)


class PollResultsTests(TestCase):
    # получение результатов: в context передаются опрос, варианты и общее число голосов

    def test_results_context_has_total_and_choices(self):
        poll = Poll.objects.create(question='Вопрос')
        Choice.objects.create(poll=poll, text='Да', votes=3)
        Choice.objects.create(poll=poll, text='Нет', votes=2)
        response = self.client.get(reverse('poll_results', args=[poll.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['poll'], poll)
        self.assertEqual(response.context['total_votes'], 5)
        choices = list(response.context['choices'])
        self.assertEqual(len(choices), 2)

    def test_results_total_votes_zero_when_no_votes(self):
        poll = Poll.objects.create(question='Вопрос')
        Choice.objects.create(poll=poll, text='Да', votes=0)
        Choice.objects.create(poll=poll, text='Нет', votes=0)
        response = self.client.get(reverse('poll_results', args=[poll.pk]))
        self.assertEqual(response.context['total_votes'], 0)


class CommentTests(TestCase):
    # комментарии: залогиненный пользователь может добавить комментарий к опросу

    def test_authenticated_user_can_add_comment(self):
        from app.models import Comment
        user = User.objects.create_user('u', 'u@t.com', 'pass')
        poll = Poll.objects.create(question='Опрос', created_by=user)
        self.client.login(username='u', password='pass')
        self.client.post(reverse('poll_comment', args=[poll.pk]), {'text': 'комментарий'})
        comments = list(poll.comments.all())
        self.assertEqual(len(comments), 1)
        self.assertEqual(comments[0].text, 'комментарий')
        self.assertEqual(comments[0].author, user)
