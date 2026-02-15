from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST
import json
from .models import Room, Message


def index(request):
    slug = request.GET.get('slug', '').strip().lower()
    if slug:
        room_obj = get_object_or_404(Room, slug=slug)
        return redirect('app:room', slug=room_obj.slug)
    rooms = Room.objects.all().order_by('-created_at')
    return render(request, 'app/index.html', {'rooms': rooms})


def create_room(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip() or 'Новая комната'
        room = Room.objects.create(name=name)
        return redirect('app:room', slug=room.slug)
    return redirect('app:index')


def room(request, slug):
    room_obj = get_object_or_404(Room, slug=slug)
    user_name = request.session.get('user_name', '')

    if request.method == 'POST' and 'set_username' in request.POST:
        user_name = request.POST.get('user_name', '').strip()
        if user_name:
            request.session['user_name'] = user_name
        request.session.modified = True
        return redirect('app:room', slug=slug)

    recent_messages = room_obj.messages.all()[:50]
    return render(request, 'app/room.html', {
        'room': room_obj,
        'user_name': user_name,
        'recent_messages': recent_messages,
    })


@require_POST
def delete_room(request, slug):
    room_obj = get_object_or_404(Room, slug=slug)
    room_obj.delete()
    return redirect('app:index')


@require_GET
def get_messages(request, slug):
    try:
        room_obj = Room.objects.get(slug=slug)
        last_id = int(request.GET.get('last_id', 0))
        new_messages = room_obj.messages.filter(id__gt=last_id)[:50]
        messages_data = [
            {
                'id': msg.id,
                'user_name': msg.user_name,
                'content': msg.content,
                'timestamp': msg.timestamp.strftime('%H:%M'),
            }
            for msg in new_messages
        ]
        return JsonResponse({'messages': messages_data})
    except Room.DoesNotExist:
        return JsonResponse({'error': 'Комната не найдена'}, status=404)


@csrf_exempt
@require_POST
def send_message(request):
    try:
        data = json.loads(request.body)
        room_slug = data.get('room')
        content = data.get('content', '').strip()
        if not content:
            return JsonResponse({'error': 'Сообщение не может быть пустым'}, status=400)
        room_obj = Room.objects.get(slug=room_slug)
        user_name = request.session.get('user_name') or 'Аноним'
        message = Message.objects.create(
            room=room_obj,
            user_name=user_name,
            content=content,
        )
        return JsonResponse({
            'success': True,
            'message': {
                'id': message.id,
                'user_name': message.user_name,
                'content': message.content,
                'timestamp': message.timestamp.strftime('%H:%M'),
            },
        })
    except Room.DoesNotExist:
        return JsonResponse({'error': 'Комната не найдена'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
