from django.db import models
import string
import random

# генерация ссылки для комнаты
def generate_slug():
    lenght = 6 
    chars = string.ascii_lowercase + string.digits
    while True:
        slug = ''.join(random.choice(chars) for _ in range(lenght))
        if not Room.objects.filter(slug=slug).exists():
            return slug
        
class Room(models.Model):
    slug = models.CharField(max_length=10, unique=True, default=generate_slug)
    name = models.CharField(max_length=100, verbose_name="Название чата")
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)

class Message(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="messages")
    user_name = models.CharField(max_length=40, verbose_name="имя пользователя")
    content = models.TextField(verbose_name="текст сообщения") 
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta: 
        ordering = ['timestamp']

    def __str__(self):
        return f"{self.user_name}:{self.content[:20]}"   


# Create your models here.
