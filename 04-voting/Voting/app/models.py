from django.db import models
from django.conf import settings


class Poll(models.Model):
    question = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='created_polls',
    )

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.question

    def total_votes(self):
        return sum(c.votes for c in self.choice_set.all())


class Choice(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    class Meta:
        ordering = ['pk']

    def __str__(self):
        return self.text


class Comment(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='poll_comments',
    )
    text = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return self.text[:50]


class Vote(models.Model):
    """Один голос одного пользователя в одном опросе."""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='poll_votes',
    )
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name='votes')
    choice = models.ForeignKey(
        Choice,
        on_delete=models.CASCADE,
        related_name='vote_records',
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'poll'], name='one_vote_per_user_per_poll'),
        ]

    def __str__(self):
        return f'{self.user.username} -> {self.choice.text}'
