from django.conf import settings
from django.contrib.syndication.views import Feed
from app.models import Post
from django.urls import reverse

class LatestPostsFeed(Feed):
    title='DataTau - Latest Posts'
    link='/feeds/'
    description='The latest posts on DataTau'

    def items(self):
        return Post.objects.order_by('-insert_date')[:settings.TOP_N_ITEMS]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.url or ''

    def item_link(self, item):
        return reverse('post', args=[item.id])