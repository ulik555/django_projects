# Count: общее количество объектов
from django.db.models import Count
from django.shortcuts import render, get_object_or_404
from .models import Post, Comment
# подключаем файл forms.py
from .forms import EmailPostForm, CommentForm, SearchForm
# Отправка электронных писем
from django.core.mail import send_mail
from django.views.decorators.http import require_POST
# Для постраничной разбивки сайта
from django.views.generic import ListView
from taggit.models import Tag

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# поисковая строка
from django.contrib.postgres.search import TrigramSimilarity


# Представления(функции)
def post_list(request, tag_slug=None):
    post_list = Post.published.all()
    #
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        post_list = post_list.filter(tags__in=[tag])

    paginator = Paginator(post_list, 3)
    page_number = request.GET.get('page', 1)
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        # Если номер_страницы не является целым числом, доставьте первую страницу
        posts = paginator.page(1)
    except EmptyPage:
        # Если номер_страницы выходит за пределы диапазона, доставьте последнюю страницу результатов
        posts = paginator.page(paginator.num_pages)
    return render(request,
                'blog/post/list.html',
                {'posts': posts,
                'tag': tag})

class PostListView(ListView):
    # чтобы иметь конкретно-прикладной набор запросов QuerySet
    queryset = Post.published.all()
    # используется для результатов запроса.
    context_object_name = 'posts'
    # Постраничная разбивка с 3 постами на страницу
    paginate_by = 3
    # шаблон используется для прорисовки страницы шаблоном template_name
    template_name = 'blog/post/list.html'


# Это представление детальной информации о посте
def post_detail(request, year, month, day, post):  #
    # извелекает посты по дате
    post = get_object_or_404(Post, status=Post.Status.PUBLISHED,
    slug=post,
    publish__year=year,
    publish__month=month,
    publish__day=day)  # Указанная функция извлекает объект, соответствующий переданным параметрам, либо исключение HTTP с кодом состояния, равным 404

    # Список схожих постов
    # post_tags_ids = post.tags.values_list('id', flat=True)
    # similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)

    # similar_posts = similar_posts.annotate(same_tags=Count('tags'))\
    #                             .order_by('-same_tags','-publish')[:4]

    # чтобы извлекать все активные комментарии к посту
    comments = post.comments.filter(active=True)
    # экземпляр формы для комментария
    form = CommentForm()

    # прорисовать извлеченный пост с использованием шаблона html
    return render(request, 'blog/post/detail.html', {'post': post,
                'comments': comments, 'form': form,
})

def post_share(request, post_id):
    # получаем объект поста по id
    post = get_object_or_404(Post, id=post_id, \
                                status=Post.Status.PUBLISHED)
    sent = False
    # для отправки email
    if request.method == 'POST':
        # Форма была передана на обработку
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # если форма валидна - отправляем уведомление
            cd = form.cleaned_data
            # отправить электронное письмо
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} рекомендует прочесть " \
                    f"{post.title}"
            message = f"Read {post.title} at {post_url}\n\n" \
                    f"{cd['name']}\'s comments: {cd['comments']}"
            send_mail(subject, message, 'ulik345@yandex.ru',
                    [cd['to']])
            sent = True

    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'post': post,
                                                    'form': form,
                                                    'sent': sent})
# require_POST, разрешить запросы методом POST только для этого представления
@require_POST
def post_comment(request, post_id):
    'чтобы управлять передачей поста на обработку.'
    # По id поста извлекается опубликованный пост
    post = get_object_or_404(Post, id=post_id,
                            status=Post.Status.PUBLISHED)

    # для хранения комментарного объекта при его создании.
    comment = None
    # экземпляр формы, используя переданные на обработку POST-данные
    form = CommentForm(data=request.POST)
    if form.is_valid():  # проводится их валидация
        # Создать объект класса Comment, не сохраняя его в базе данных
        comment = form.save(commit=False)
        # Пост назначается созданному комментарию
        comment.post = post
        # Метод save() создает экземпляр модели, к которой форма
        # привязана и сохраняет его в базе данных
        comment.save()
    # Отобразить страницу с постом и формой для добав
    #ления комментария с ошибкой, если она есть
    return render(request, 'blog/post/comment.html',
                {'post': post, 'form': form, 'comment': comment})

# поисковая строка
def post_search(request):
    form = SearchForm()
    query = None
    results = []
#Для проверки того, что форма была передана на обработку
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            # search_vector = SearchVector('title', 'body', config='english')
            # выделяются основы слов и удаляются стоп-слова
            # search_query =  SearchQuery(query, config='english')
            # Получение всех публичных постов
            results = Post.published.annotate(
            # выполняется поиск опубликованных постов
                similarity=TrigramSimilarity('title', query),
                ).filter(similarity__gt=0.1).order_by('-similarity')
                # search=search_vector, rank=SearchRank(search_vector, search_query),
                # ).filter(search=search_query).order_by('-rank')

    return render(request,
                'blog/post/search.html',
                {'form': form,
                'query': query,
                'results': results})