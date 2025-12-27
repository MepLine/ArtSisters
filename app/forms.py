from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _
from .models import Comment
from .models import Blog
from .models import Feedback



# Форма входа
class BootstrapAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        label=_("Имя пользователя"),
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Имя пользователя"
        })
    )

    password = forms.CharField(
        label=_("Пароль"),
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "placeholder": "Пароль"
        })
    )


# Форма обратной свзяи
class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ("name", "email", "rating", "design", "features", "topic", "comment")
        labels = {
            "name": "Ваше имя",
            "email": "Email",
            "rating": "Оценка сайта (1–10)",
            "design": "Оформление сайта",
            "features": "Что понравилось (можно несколько)",
            "topic": "Какая тема вам интереснее?",
            "comment": "Пожелания и комментарии",
        }
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "rating": forms.NumberInput(attrs={"class": "form-control", "min": 1, "max": 10}),
            "topic": forms.Select(attrs={"class": "form-control"}),
            "comment": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
        }

    # чекбоксы (features) в БД будем хранить строкой через запятую
    features = forms.MultipleChoiceField(
        label="Что понравилось (можно несколько)",
        required=False,
        choices=[
            ("Контент", "Контент"),
            ("Дизайн", "Дизайн"),
            ("Удобство", "Удобство"),
            ("Скорость", "Скорость"),
        ],
        widget=forms.CheckboxSelectMultiple
    )

    def clean_features(self):
        vals = self.cleaned_data.get("features", [])
        return ", ".join(vals)


# Комментарии
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)
        labels = {
            'text': 'Комментарий'
        }

#Блог
class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ('title', 'summary', 'image', 'content')
        labels = {
            'title': 'Заголовок',
            'summary': 'Краткое содержание',
            'image': 'Картинка',
            'content': 'Полное содержание',
        }