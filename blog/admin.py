from django.contrib import admin
from .models import BlogPost, Comment, Like




class CommentInline(admin.TabularInline):
    model = Comment
    extra = 1

class LikeInline(admin.TabularInline):
    model = Like
    extra = 1

class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publication_date')
    search_fields = ('title', 'author__username')
    inlines = [CommentInline, LikeInline]

class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'author', 'created_date')
    search_fields = ('post__title', 'author__username')

class LikeAdmin(admin.ModelAdmin):
    list_display = ('post', 'user')
    search_fields = ('post__title', 'user__username')


admin.site.register(BlogPost, BlogPostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Like, LikeAdmin)