from django import forms
from django.contrib.auth.models import User
from .models import Poll, Choice


class PollCreateForm(forms.Form):
    question = forms.CharField(max_length=200, label='Вопрос')
    choice_1 = forms.CharField(max_length=200, label='Вариант 1')
    choice_2 = forms.CharField(max_length=200, label='Вариант 2')

    def save(self, user=None):
        poll = Poll.objects.create(
            question=self.cleaned_data['question'],
            created_by=user,
        )
        Choice.objects.create(poll=poll, text=self.cleaned_data['choice_1'])
        Choice.objects.create(poll=poll, text=self.cleaned_data['choice_2'])
        return poll


class CommentForm(forms.Form):
    text = forms.CharField(
        max_length=500,
        label='Комментарий',
        widget=forms.Textarea(attrs={'rows': 3, 'placeholder': 'Написать комментарий...'}),
    )


class RegisterForm(forms.ModelForm):
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'email')

    def clean_password2(self):
        if self.cleaned_data.get('password') != self.cleaned_data.get('password2'):
            raise forms.ValidationError('Пароли не совпадают')
        return self.cleaned_data['password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user
