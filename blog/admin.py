from django.contrib import admin
from .models import Post, Comment

# В этот класс можно вставлять информацию о том, как показывать модель на сайте и как с ней взаимодействовать.
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):  # сообщаем сайту администрирования, что модель зарегистрирована
    # позволяет задавать поля модели, которые вы хотите показывать на странице
    list_display = ('title', 'slug', 'author', 'publish', 'status')
    list_filter = ['status', 'created', 'publish', 'author']
    search_fields = ['title', 'body']  # строка поиска
    # предзаполнять поле slug данными
    prepopulated_fields = {'slug': ('title',)}
    # author отображается поисковым виджетом
    raw_id_fields = ['author']
    date_hierarchy = 'publish'  # навигационные ссылки
    ordering = ['status', 'publish']  # заданы критерии сортировки

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'post', 'created', 'active']
    list_filter = ['active', 'created', 'updated']
    search_fields = ['name', 'email', 'body']