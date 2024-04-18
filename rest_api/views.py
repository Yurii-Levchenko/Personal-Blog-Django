from django.shortcuts import render

from rest_framework import viewsets
from .serializers import PostSerializer, AuthorSerializer, TagSerializer, CommentSerializer
from blog.models import Post, Author, Tag, Comment

# rest framework views

class PostsRestView(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

class AuthorRestView(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer


class  TagsRestView(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

class CommentsRestView(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer