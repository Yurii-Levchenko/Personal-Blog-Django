from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register('posts', views.PostsRestView)
router.register('authors', views.AuthorRestView)
router.register('tags', views.TagsRestView)
router.register('comments', views.CommentsRestView)

urlpatterns = [
    path('', include(router.urls)),

]