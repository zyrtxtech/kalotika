from django.urls import path
from . import views
from .views import PostDetailView, like_post, add_comment

urlpatterns = [
    path("", views.PostListView.as_view(), name="post_list"),
    path("<slug:slug>/", PostDetailView.as_view(), name="post_detail"),
    path("<slug:slug>/like/", like_post, name="like_post"),
    path("<slug:slug>/comment/", add_comment, name="add_comment"),
    path(
        "category/<slug:slug>/",
        views.CategoryDetailView.as_view(),
        name="category_detail",
    ),
    path("tag/<slug:slug>/", views.TagDetailView.as_view(), name="tag_detail"),
    path("post/<slug:slug>/like/", views.PostLikeView.as_view(), name="post_like"),
    path(
        "post/<slug:slug>/comment/",
        views.CommentCreateView.as_view(),
        name="add_comment",
    ),
    path(
        "post/<slug:slug>/comment/<int:pk>/like/",
        views.CommentLikeView.as_view(),
        name="comment_like",
    ),
    path(
        "archive/<int:year>/<int:month>/", views.ArchiveView.as_view(), name="archive"
    ),
]
