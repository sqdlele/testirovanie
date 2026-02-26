from django.contrib import admin
from .models import Poll, Choice, Comment, Vote


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 2


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0


@admin.register(Poll)
class PollAdmin(admin.ModelAdmin):
    list_display = ('question', 'created_by', 'created_at')
    inlines = [ChoiceInline, CommentInline]


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ('user', 'poll', 'choice')
    list_filter = ('poll',)
