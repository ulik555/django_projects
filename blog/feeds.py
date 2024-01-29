import markdown
from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords_html
from django.urls import reverse_lazy
from .models import Post


class LatestPostsFeed(Feed):
    'новостную лентa'

    title = 'My blog'
    # reverse_lazy() генерировать URL-адрес для атрибута link
    link = reverse_lazy('blog:post_list')
    description = 'New posts of my blog.'

    def items(self):
        'извлекает включаемые в новостную ленту объекты'
        return Post.published.all()[:5]

    def item_title(self, item):
        ''
        return item.title

    def item_description(self, item):
        # markdown() , чтобы конвертировать контент в формате Markdown в формат HTML
        return truncatewords_html(markdown.markdown(item.body), 30)

    def item_pubdate(self, item):
        return item.publish