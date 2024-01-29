# from django.db import models
# from django.utils import timezone
# # User чтобы создавать взаимосвязи между пользователями и постами
# from django.contrib.auth.models import User
# from taggit.managers import TaggableManager
# from django.urls import reverse

# # тут создаются классы для создания БД

# class PublishedManager(models.Manager):
#     def get_queryset(self):
#         # возвращает набор запросов QuerySet
#         return super().get_queryset()\
#             .filter(status=Post.Status.PUBLISHED)

# class Post(models.Model):

#     class Status(models.TextChoices):
#         DRAFT = 'DF', "Черновик"
#         PUBLISHED = 'PB', 'Published'


#     title = models.CharField(max_length=200)
#     # должно быть уникальным для даты, сохраненной в поле publish.
#     slug = models.SlugField(max_length=250, unique_for_date='publish')
#     # Это поле определяет взаимосвязь многие-к-одному
#     author = models.ForeignKey(User, on_delete=models.CASCADE,
#                             related_name='blog_posts')

#     body = models.TextField()
#     publish = models.DateTimeField(default=timezone.now)
#     created = models.DateTimeField(auto_now_add=True)
#     updated = models.DateTimeField(auto_now=True)
#     status = models.CharField(max_length=2,
#                             choices=Status.choices,
#                             default=Status.DRAFT)

#     objects = models.Manager() # менеджер, применяемый по умолчанию
#     published = PublishedManager() # конкретно-прикладной менеджер
#     tags = TaggableManager()
#     class Meta:
#         ordering = ('-publish',)  # сортировка по дате
#         indexes = [models.Index(fields=['-publish']),
#                 ]

#     def __str__(self) -> str:
#         return self.title

#     def get_absolute_url(self):
#         """Возвращает URL для этой статьи."""
#         return reverse('blog:post_detail',
#                     args=[self.publish.year, self.publish.month,
#                         self.publish.day, self.slug])

# class Comment(models.Model):
#     # ForeignKey добавлено , чтобы связать каждый комментарий с 1 постом
#     post = models.ForeignKey(Post, on_delete=models.CASCADE,
#                             related_name='comments')
#     #
#     name = models.CharField(max_length=80)
#     email = models.EmailField()
#     body = models.TextField()
#     # хранить дату и время создания комментария.
#     created = models.DateTimeField(auto_now_add=True)
#     # позволит del неуместные комментарии вручную с по­мощью сайта администрирования
#     updated = models.DateTimeField(auto_now=True)
#     active = models.BooleanField(default=True)

#     class Meta:
#         # по умолчанию сортировать комментарии в хронологическом порядке
#         ordering = ['created']
#         indexes = [models.Index(fields=['created']),]

#     def __str__(self) -> str:
#         return f'Комментарий от {self.name} o {self.post}'

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from taggit.managers import TaggableManager


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()\
                    .filter(status=Post.Status.PUBLISHED)


class Post(models.Model):

    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'

    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250,
                            unique_for_date='publish')
    author = models.ForeignKey(User,
                            on_delete=models.CASCADE,
                            related_name='blog_posts')
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=2,
                            choices=Status.choices,
                            default=Status.DRAFT)

    objects = models.Manager() # The default manager.
    published = PublishedManager() # Our custom manager.
    tags = TaggableManager()

    class Meta:
        ordering = ['-publish']
        indexes = [
            models.Index(fields=['-publish']),
        ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post_detail',
                    args=[self.publish.year,
                            self.publish.month,
                            self.publish.day,
                            self.slug])


class Comment(models.Model):
    post = models.ForeignKey(Post,
                            on_delete=models.CASCADE,
                            related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['created']
        indexes = [
            models.Index(fields=['created']),
        ]

    def __str__(self):
        return f'Comment by {self.name} on {self.post}'