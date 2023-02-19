from django.contrib import admin
from .models import Author, Category, Post, Comment


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('author_acc', 'rating',)
    search_fields = ('author_acc',)


class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'p_type', 'title', 'author', 'rating', 'time')
    list_display_links = ('title', )
    search_fields = ('author', 'title', )
    list_editable = ('p_type',)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'text', 'rating', 'time')
    list_display_links = ('text',)
    search_fields = ('user', 'text')
    list_filter = ('user', 'rating', 'time')


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'cat_name', 'slug')
    list_display_links = ('cat_name',)
    search_fields = ('cat_name',)
    exclude = ['slug']


admin.site.register(Author, AuthorAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Category, CategoryAdmin)
