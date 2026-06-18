from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db.models import Q
from .models import Task
from .forms import TaskForm, UserRegisterForm


def register(request):
    if request.user.is_authenticated:
        return redirect("task_list")
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(
                request,
                f"Welcome, {user.username}! Your account has been created successfully.",
            )
            return redirect("task_list")
        else:
            messages.error(
                request, "Registration failed. Please check the errors below."
            )
    else:
        form = UserRegisterForm()
    return render(request, "registration/register.html", {"form": form})


@login_required
def task_list(request):
    # Get all tasks for the current user
    tasks = Task.objects.filter(user=request.user)

    # Search query
    search_query = request.GET.get("q", "")
    if search_query:
        tasks = tasks.filter(
            Q(title__icontains=search_query) | Q(description__icontains=search_query)
        )

    # Status filter
    status_filter = request.GET.get("status", "all")
    if status_filter == "active":
        tasks = tasks.filter(completed=False)
    elif status_filter == "completed":
        tasks = tasks.filter(completed=True)

    # Priority filter
    priority_filter = request.GET.get("priority", "")
    if priority_filter:
        tasks = tasks.filter(priority=priority_filter)

    # Category filter
    category_filter = request.GET.get("category", "")
    if category_filter:
        tasks = tasks.filter(category=category_filter)

    # Stats for the dashboard
    total_tasks = Task.objects.filter(user=request.user).count()
    completed_tasks = Task.objects.filter(user=request.user, completed=True).count()
    active_tasks = total_tasks - completed_tasks
    completion_rate = (
        int((completed_tasks / total_tasks * 100)) if total_tasks > 0 else 0
    )

    # Quick create form
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            messages.success(request, f'Task "{task.title}" created successfully!')
            return redirect("task_list")
    else:
        form = TaskForm()

    context = {
        "tasks": tasks,
        "form": form,
        "search_query": search_query,
        "status_filter": status_filter,
        "priority_filter": priority_filter,
        "category_filter": category_filter,
        "total_tasks": total_tasks,
        "completed_tasks": completed_tasks,
        "active_tasks": active_tasks,
        "completion_rate": completion_rate,
        "priorities": Task.PRIORITY_CHOICES,
        "categories": Task.CATEGORY_CHOICES,
    }
    return render(request, "tasks/list.html", context)


@login_required
def task_create(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            messages.success(request, f'Task "{task.title}" created successfully!')
            return redirect("task_list")
    else:
        form = TaskForm()
    return render(
        request, "tasks/form.html", {"form": form, "title": "Create New Task"}
    )


@login_required
def task_edit(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, f'Task "{task.title}" updated successfully!')
            return redirect("task_list")
    else:
        form = TaskForm(instance=task)
    return render(
        request, "tasks/form.html", {"form": form, "task": task, "title": "Edit Task"}
    )


@login_required
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method == "POST" or request.GET.get("confirm") == "yes":
        title = task.title
        task.delete()
        messages.success(request, f'Task "{title}" was deleted.')
        return redirect("task_list")
    return render(request, "tasks/confirm_delete.html", {"task": task})


@login_required
@require_POST
def task_toggle(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    task.completed = not task.completed
    task.save()

    # Recalculate stats for response
    total_tasks = Task.objects.filter(user=request.user).count()
    completed_tasks = Task.objects.filter(user=request.user, completed=True).count()
    completion_rate = (
        int((completed_tasks / total_tasks * 100)) if total_tasks > 0 else 0
    )

    return JsonResponse(
        {
            "success": True,
            "completed": task.completed,
            "completed_count": completed_tasks,
            "active_count": total_tasks - completed_tasks,
            "completion_rate": completion_rate,
        }
    )


def user_logout(request):
    logout(request)
    messages.info(request, "You have been logged out successfully.")
    return redirect("login")
