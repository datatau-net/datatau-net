from django.contrib import admin

from .models import Post, PostVoteTracking, Comment, CommentVoteTracking


class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'url_link', 'user', 'votes', 'show_dt', 'ask_dt']


class PostVoteTrackingAdmin(admin.ModelAdmin):
    list_display = ['user', 'post']


class CommentAdmin(admin.ModelAdmin):
    list_display = ['content', 'user', 'post', 'votes']


class CommentVoteTrackingAdmin(admin.ModelAdmin):
    list_display = ['user', 'comment']


admin.site.register(Post, PostAdmin)
admin.site.register(PostVoteTracking, PostVoteTrackingAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(CommentVoteTracking, CommentVoteTrackingAdmin)
