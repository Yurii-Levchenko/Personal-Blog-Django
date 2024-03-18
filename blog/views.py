# for returning corresponding rendered html pages
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import DetailView, ListView
from django.views import View

from .models import Post, Author, Tag, Comment
from .forms import CommentForm

from rest_framework import viewsets
from .serializers import PostSerializer, AuthorSerializer, TagSerializer, CommentSerializer


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

# django views

def get_date(post):
    return post['date']
    # or return post.get('date')


# Create your views here.

class StartingPageView(ListView):
    template_name = "blog/index.html"
    model = Post
    ordering = ["-date",]
    context_object_name = "posts"

    def get_queryset(self):
        queryset = super().get_queryset()
        data = queryset[:3]
        return data
    

# def starting_page(request):
#     # sorted_posts = sorted(all_posts, key=get_date)
#     latest_posts = Post.objects.order_by('-date')[:3]
#     return render(request, "blog/index.html", {
#         "posts": latest_posts
#     })


class AllPostsView(ListView):
    template_name = "blog/all_posts.html"
    model = Post
    ordering = ["-date"]
    context_object_name = "all_posts"


# def posts(request):
#     all_posts = Post.objects.all()
#     return render(request, "blog/all_posts.html", {
#         'all_posts': all_posts
#     })


class PostDetailView(View):

    def is_stored_post(self, request, post_id):
        stored_posts = request.session.get("stored_posts")
        if stored_posts is not None:
            is_saved_for_later = post_id in stored_posts
        else:
            is_saved_for_later = False
        
        return is_saved_for_later

    def get(self, request, slug):
        post = Post.objects.get(slug=slug)
        
        context = {
            "post": post,
            "post_tags": post.tags.all(),
            "comment_form": CommentForm(),
            "comments": post.comments.all().order_by("-id"),
            "saved_for_later": self.is_stored_post(request, post.id),
        }
        return render(request, "blog/post-detail.html", context)

    def post(self, request, slug):
        comment_form = CommentForm(request.POST)
        post = Post.objects.get(slug=slug)

        if comment_form.is_valid():
            comment = comment_form.save(commit=False) # comment=False will not hit the db but instead create the instance
            comment.post = post # adding post field to 
            comment.save()

            return  HttpResponseRedirect(reverse("post-detail-page", args=[slug]))

        context = {
            "post": post,
            "post_tags": post.tags.all(),
            "comment_form": comment_form,
            "comments": post.comments.all().order_by("-id"), # comments is related name for post in comment model
            "saved_for_later": self.is_stored_post(request, post.id),
        }
        return render(request, "blog/post-detail.html", context)

    

# def post_detail(request, slug):
#     identified_post = get_object_or_404(Post, slug=slug)
    
#     return render(request, "blog/post-detail.html", {
#         "post": identified_post,
#         "post_tags": identified_post.tags.all()
#     })


class ReadLaterView(View):

    def get(self, request):
        stored_posts = request.session.get("stored_posts")
        context = {}

        if stored_posts is None or len(stored_posts) == 0:
            context["posts"] = []    
            context["has_posts"] = False
        else:
            posts = Post.objects.filter(id__in=stored_posts)
            context["posts"] = posts
            context["has_posts"] = True

        return render(request, "blog/read-later.html", context)

    def post(self, request):
        stored_posts = request.session.get("stored_posts")

        if stored_posts is None:
            stored_posts = []
        
        post_id = int(request.POST["post_id"])

        if post_id not in stored_posts:
            # im adding post's id, not object as a whole
            stored_posts.append(post_id)
        else:
            stored_posts.remove(post_id)
        
        request.session["stored_posts"] = stored_posts
        
        return HttpResponseRedirect("/read-later")