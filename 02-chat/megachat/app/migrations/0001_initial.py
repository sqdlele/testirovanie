# Generated manually for megachat app

from django.db import migrations, models
import django.db.models.deletion
import app.models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.CharField(default=app.models.generate_slug, max_length=10, unique=True)),
                ('name', models.CharField(max_length=100, verbose_name='Название чата')),
                ('created_at', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_name', models.CharField(max_length=40, verbose_name='имя пользователя')),
                ('content', models.TextField(verbose_name='текст сообщения')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='app.room')),
            ],
            options={
                'ordering': ['timestamp'],
            },
        ),
    ]
