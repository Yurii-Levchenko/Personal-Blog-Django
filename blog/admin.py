from django.contrib import admin
from .models import Author, Post, Tag, Comment


class AuthorAdmin(admin.ModelAdmin):
    list_display = ("full_name",)


class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    list_display = ('title', 'date', "author")
    list_filter = ('author', 'date', 'tags')


class TagAdmin(admin.ModelAdmin):
    list_display = ('caption',)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('user_name', 'post')

# enough to registrate and manage data on admin panel
admin.site.register(Author, AuthorAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Comment, CommentAdmin)
