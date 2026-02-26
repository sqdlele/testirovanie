from django.test import TestCase, Client
from django.urls import reverse
from app.models import Task


class TaskCRUDTests(TestCase):
    # Сценарий: создание задачи и проверка, что объект попал в коллекцию Task.objects
    def test_create_task_appears_in_queryset(self):
        Task.objects.create(title="Купить молоко")
        all_tasks = list(Task.objects.all())
        self.assertEqual(len(all_tasks), 1)
        self.assertEqual(all_tasks[0].title, "Купить молоко")
        self.assertFalse(all_tasks[0].completed)

    def test_task_list_view_returns_all_tasks_in_context(self):
        # Сценарий: несколько задач в БД — список на странице содержит те же объекты
        Task.objects.create(title="Задача 1")
        Task.objects.create(title="Задача 2")
        response = self.client.get(reverse("task_list"))
        self.assertEqual(response.status_code, 200)
        tasks_in_context = list(response.context["tasks"])
        self.assertEqual(len(tasks_in_context), 2)
        titles = [t.title for t in tasks_in_context]
        self.assertIn("Задача 1", titles)
        self.assertIn("Задача 2", titles)

    def test_edit_task_updates_object_in_db(self):
        # Сценарий: создаём задачу, редактируем через POST — в бд сохраняется новое значение
        task = Task.objects.create(title="Старый заголовок")
        self.client.post(reverse("task_edit", args=[task.pk]), {"title": "Новый заголовок"})
        task.refresh_from_db()
        self.assertEqual(task.title, "Новый заголовок")

    def test_delete_task_removes_from_queryset(self):
        # Сценарий: создаём задачу, удаляем через представление — в Task.objects её больше нет
        task = Task.objects.create(title="Удаляемая")
        self.client.post(reverse("task_delete", args=[task.pk]))
        self.assertNotIn(task, Task.objects.all())
        self.assertEqual(Task.objects.count(), 0)

    def test_toggle_completed_sets_task_completed_true(self):
        # Сценарий: задача не выполнена, нажимаем «Выполнено» — у объекта task.completed = True
        task = Task.objects.create(title="Сделать", completed=False)
        self.client.post(reverse("task_toggle", args=[task.pk]))
        task.refresh_from_db()
        self.assertTrue(task.completed)

    def test_toggle_completed_sets_task_completed_false(self):
        # Сценарий: задача выполнена, нажимаем «Снять отметку» — у объекта task.completed = False.
        task = Task.objects.create(title="Готово", completed=True)
        self.client.post(reverse("task_toggle", args=[task.pk]))
        task.refresh_from_db()
        self.assertFalse(task.completed)
