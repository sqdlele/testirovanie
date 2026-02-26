from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from .models import Poll, Choice, Comment, Vote
from .forms import PollCreateForm, CommentForm, RegisterForm


def poll_list(request):
    polls = Poll.objects.all().select_related('created_by').prefetch_related('choice_set')
    return render(request, 'app/poll_list.html', {'polls': polls})


@login_required(login_url='/login/')
def poll_create(request):
    if request.method == 'POST':
        form = PollCreateForm(request.POST)
        if form.is_valid():
            form.save(user=request.user)
            return redirect('poll_list')
    else:
        form = PollCreateForm()
    return render(request, 'app/poll_form.html', {'form': form})


def poll_detail(request, pk):
    poll = get_object_or_404(Poll, pk=pk)
    comments = poll.comments.select_related('author').all()
    choices = poll.choice_set.all()
    total_votes = poll.total_votes()
    has_voted = False
    if request.user.is_authenticated:
        has_voted = Vote.objects.filter(poll=poll, user=request.user).exists()
    return render(request, 'app/poll_detail.html', {
        'poll': poll,
        'comments': comments,
        'comment_form': CommentForm(),
        'has_voted': has_voted,
        'choices': choices,
        'total_votes': total_votes,
    })


@require_http_methods(['POST'])
def poll_vote(request, pk):
    poll = get_object_or_404(Poll, pk=pk)
    if not request.user.is_authenticated:
        from django.urls import reverse
        from django.http import HttpResponseRedirect
        login_url = reverse('login') + '?next=' + reverse('poll_detail', args=[pk])
        return redirect(login_url)
    if Vote.objects.filter(poll=poll, user=request.user).exists():
        return redirect('poll_results', pk=poll.pk)
    choice_id = request.POST.get('choice')
    choice = get_object_or_404(Choice, pk=choice_id, poll=poll)
    Vote.objects.create(poll=poll, user=request.user, choice=choice)
    choice.votes += 1
    choice.save()
    return redirect('poll_results', pk=poll.pk)


@login_required(login_url='/login/')
@require_http_methods(['POST'])
def poll_comment(request, pk):
    poll = get_object_or_404(Poll, pk=pk)
    form = CommentForm(request.POST)
    if form.is_valid():
        Comment.objects.create(
            poll=poll,
            author=request.user,
            text=form.cleaned_data['text'].strip(),
        )
    return redirect('poll_detail', pk=pk)


def poll_results(request, pk):
    poll = get_object_or_404(Poll, pk=pk)
    choices = poll.choice_set.all()
    total = poll.total_votes()
    return render(request, 'app/poll_results.html', {
        'poll': poll,
        'choices': choices,
        'total_votes': total,
    })


def login_view(request):
    if request.user.is_authenticated:
        return redirect('poll_list')
    msg = None
    if request.method == 'POST':
        user = authenticate(
            request,
            username=request.POST.get('username'),
            password=request.POST.get('password'),
        )
        if user:
            login(request, user)
            return redirect(request.GET.get('next', 'poll_list'))
        msg = 'Неверный логин или пароль.'
    return render(request, 'app/login.html', {'message': msg})


def register_view(request):
    if request.user.is_authenticated:
        return redirect('poll_list')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            user = authenticate(
                request,
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            if user:
                login(request, user)
            return redirect('poll_list')
    else:
        form = RegisterForm()
    return render(request, 'app/register.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('poll_list')
