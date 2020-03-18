from django.urls import path
from . import views
from django.core.paginator import Paginator 
from .views import PostListView, PostDetailView,PostCreateView,PostUpdateView,PostDeleteView,UserPostListView,PostLatestListView,PostAboutListView
urlpatterns = [
    path('user/<username>', UserPostListView.as_view(), name = "user-post"),
    path('', PostListView.as_view(), name = "blog-home"),
    path('<int:pk>/', PostDetailView.as_view(), name = 'post-detail'),
    path('create/', PostCreateView.as_view(), name = 'post-create'),
    path('<int:pk>/update/', PostUpdateView.as_view(), name = 'post-update'),
    path('<int:pk>/delete/', PostDeleteView.as_view(), name = 'post-delete'),
    path('latest/',PostLatestListView.as_view(),name = 'latest-post'),
    path('about/', PostAboutListView.as_view(), name = "blog-about"),
]