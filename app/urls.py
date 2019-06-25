from django.contrib.auth.decorators import login_required
from django.contrib.sitemaps.views import sitemap
from django.urls import path

from . import views
from .sitemaps import PostSitemap, StaticViewSitemap

sitemaps = {
    'posts': PostSitemap,
    'static': StaticViewSitemap,
}

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:page>', views.index, name='more'),
    path('submit', login_required(views.submit), name='submit'),
    path('post/<int:post_id>', views.post, name='post'),
    path('post/<int:post_id>/comment', login_required(views.post_comment), name='post_comment'),
    path('post/<int:post_id>/edit', login_required(views.post_edit), name='post_edit'),
    path('post/<int:post_id>/delete', login_required(views.post_delete), name='post_delete'),
    path('comment/<int:comment_id>', views.comment, name='comment'),
    path('comment/<int:comment_id>/reply', login_required(views.comment_reply), name='comment_reply'),
    path('comment/<int:comment_id>/edit', login_required(views.comment_edit), name='comment_edit'),
    path('comment/<int:comment_id>/delete', login_required(views.comment_delete), name='comment_delete'),
    path('profile/<int:user_id>', views.profile, name='profile'),
    path('profile/<int:user_id>/submissions', views.submissions, name='submissions'),
    path('profile/<int:user_id>/submissions/<int:page>', views.submissions, name='submissions_more'),
    path('profile/<int:user_id>/comments', views.comments, name='comments'),
    path('profile/<int:user_id>/comments/<int:page>', views.comments, name='comments_more'),
    path('profile/<int:user_id>/update', login_required(views.update_profile), name='update_profile'),
    path('upvote-post', views.upvote_post, name='upvote_post'),
    path('upvote-comment', views.upvote_comment, name='upvote_comment'),
    path('site/<str:site>', views.site, name='site'),
    path('site/<str:site>/<int:page>', views.site, name='site_more'),
    path('new', views.new, name='new'),
    path('new/<int:page>', views.new, name='new_more'),
    path('ask', views.ask, name='ask'),
    path('ask/<int:page>', views.ask, name='ask_more'),
    path('show', views.show, name='show'),
    path('show/<int:page>', views.show, name='show_more'),
    path('under-construction', views.under_construction, name='under_construction'),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps},
         name='django.contrib.sitemaps.views.sitemap'),
]
