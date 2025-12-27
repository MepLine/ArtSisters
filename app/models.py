from django.db import models
from django.contrib import admin
from datetime import datetime
from django.urls import reverse
from django.contrib.auth.models import User


class Blog(models.Model):
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    summary = models.CharField(max_length=500, verbose_name="Краткое содержание")
    content = models.TextField(verbose_name="Полное содержание")
    image = models.ImageField(upload_to='blog_images/', default='lepka.jpg', blank=True, verbose_name="Картинка")


    posted = models.DateTimeField(
        default=datetime.now,
        db_index=True,
        verbose_name="Опубликована"
    )


    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog_detail', args=[str(self.id)])

    class Meta:
        verbose_name = "Статья блога"
        verbose_name_plural = "Статьи блога"


class Comment(models.Model):
    text = models.TextField(verbose_name="Комментарий")
    date = models.DateTimeField(verbose_name="Дата", default=datetime.now)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Автор"
    )
    post = models.ForeignKey(
        Blog,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name="Статья"
    )

    def __str__(self):
        return f'Комментарий от {self.author}'

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"
        ordering = ['-date']


class Feedback(models.Model):
    name = models.CharField(max_length=30, verbose_name="Имя")
    email = models.EmailField(blank=True, null=True, verbose_name="Email")

    rating = models.PositiveSmallIntegerField(verbose_name="Оценка (1–10)")

    design = models.CharField(
        max_length=20,
        choices=[
            ("Отлично", "Отлично"),
            ("Хорошо", "Хорошо"),
            ("Нормально", "Нормально"),
            ("Плохо", "Плохо"),
        ],
        verbose_name="Оформление сайта"
    )

    features = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="Что понравилось"
    )

    TOPIC_CHOICES = [
        ("Живопись", "Живопись"),
        ("Иллюстрация", "Иллюстрация"),
        ("Цифровое искусство", "Цифровое искусство"),
        ("Ручная работа", "Ручная работа"),
        ("Другое", "Другое"),
    ]

    topic = models.CharField(
        max_length=30,
        choices=TOPIC_CHOICES,
        default="Живопись",
        verbose_name="Интересная тема"
    )
    comment = models.TextField(max_length=500, verbose_name="Комментарий")

    created = models.DateTimeField(default=datetime.now, db_index=True, verbose_name="Дата")

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        ordering = ["-created"]

    def __str__(self):
        return f"{self.name} — {self.rating}/10"


admin.site.register(Blog)
admin.site.register(Comment)
admin.site.register(Feedback)

