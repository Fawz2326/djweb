"""
Definition of forms.
"""

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _
from django.db import models
from .models import Comment
from .models import Blog


class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses boostrap CSS."""
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'Имя пользователя'}))
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Пароль'}))


class FeedbackForm(forms.Form):
    name = forms.CharField(label='Ваше имя', min_length=2, max_length=100)
    gender = forms.ChoiceField(label='Ваш пол',
                               choices=[('1', 'Мужской'), ('2', 'Женский')],
                               widget=forms.RadioSelect, initial=1)
    age = forms.ChoiceField(label = 'Какой ваш возраст?',
                            choices = (('1', 'Меньше 18'), ('2', 'От 18 до 21'), ('3', 'Больше 21')), initial = 1)
    notice = forms.BooleanField(label='Хотите получать уведомления на e-mail?',
                                         required=False)
    email = forms.EmailField(label='Bau e-mail', min_length=7)
    message = forms.CharField(label='Ваш комментарий',
                              widget=forms.Textarea(attrs={'rows' :12, 'cols' :20}))

class CommentForm (forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)
        labels = {'text': "Комментарий"}

class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ('title', 'description', 'content', 'image',)
        labels = {'title': "Заголовок", 'description': "Краткое содержание", 'content': "Полное содержание", 'image': "Картинка"}

