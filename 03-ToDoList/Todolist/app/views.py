from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods
from .models import Task
from .forms import TaskForm


def task_list(request):
    """Список всех задач и форма добавления."""
    tasks = Task.objects.all()
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("task_list")
    else:
        form = TaskForm()
    return render(request, "app/task_list.html", {"tasks": tasks, "form": form})


def task_edit(request, pk):
    """Редактирование задачи."""
    task = get_object_or_404(Task, pk=pk)
    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect("task_list")
    else:
        form = TaskForm(instance=task)
    return render(request, "app/task_form.html", {"form": form, "task": task})


@require_http_methods(["POST"])
def task_delete(request, pk):
    """Удаление задачи."""
    task = get_object_or_404(Task, pk=pk)
    task.delete()
    return redirect("task_list")


@require_http_methods(["POST"])
def task_toggle(request, pk):
    """Пометить задачу выполненной/невыполненной."""
    task = get_object_or_404(Task, pk=pk)
    task.completed = not task.completed
    task.save()
    return redirect("task_list")
