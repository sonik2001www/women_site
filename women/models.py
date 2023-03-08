from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class Women(models.Model):
    title = models.CharField(max_length=255, verbose_name="Заголовок")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')
    content = models.TextField(blank=True)
    photo = models.ImageField(blank=True, upload_to='photos/%Y/%m/%d/')
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=True)
    cat_id = models.ForeignKey('Category', on_delete=models.PROTECT)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_slug': self.slug})

    class Meta:
        verbose_name = "Відому жінку"
        verbose_name_plural = "Відомі жінки"
        ordering = ['-time_create', 'title']


class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})

    class Meta:
        verbose_name = "Категорію"
        verbose_name_plural = "Категорї"


class GameRoom(models.Model):
    user_1 = models.CharField(max_length=100, db_index=True)
    user_2 = models.CharField(max_length=100, db_index=True, default="не визначений")
    score_1 = models.IntegerField(default=0)
    score_2 = models.IntegerField(default=0)
    attempt_1 = models.IntegerField(default=0)
    attempt_2 = models.IntegerField(default=0)
    name_1 = models.CharField(max_length=100, db_index=True, default=0)
    name_2 = models.CharField(max_length=100, db_index=True, default=0)
    name_3 = models.CharField(max_length=100, db_index=True, default=0)
    year_1 = models.IntegerField(default=0)
    year_2 = models.IntegerField(default=0)
    year_3 = models.IntegerField(default=0)
    time_create = models.DateTimeField(auto_now_add=True)
    winner = models.CharField(max_length=100, db_index=True, default='нема')
    is_open = models.BooleanField(default=True)

    def get_absolute_url(self):
        return reverse('game', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['-time_create']


class Chat(models.Model):
    user_1 = models.CharField(max_length=100, db_index=True)
    user_2 = models.CharField(max_length=100, db_index=True)
    content = models.TextField(blank=True)
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse('chat', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['-time_update']





