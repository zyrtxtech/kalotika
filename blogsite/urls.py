from django.urls import path
from .views import (
    PostListView,
    PostDetailView,
    like_post,
    add_comment,
    CategoryListView,
    CategoryDetailView,
    TagListView,
    TagDetailView,
    PostLikeView,
    CommentCreateView,
    CommentLikeView,
    ArchiveView,
)

urlpatterns = [
    path("blog/", PostListView.as_view(), name="index"),
    # Category views
    path("blog/categories/", CategoryListView.as_view(), name="category_list"),
    path(
        "blog/category/<slug:slug>/",
        CategoryDetailView.as_view(),
        name="category_detail",
    ),
    # Tag views
    path("blog/tags/", TagListView.as_view(), name="tag_list"),
    path("blog/tag/<slug:slug>/", TagDetailView.as_view(), name="tag_detail"),
    # Post detail and actions
    path("blog/<slug:slug>/", PostDetailView.as_view(), name="post_detail"),
    path("blog/<slug:slug>/like/", like_post, name="like_post"),
    path("blog/<slug:slug>/comment/", add_comment, name="add_comment"),
    # Post actions (like, comment)
    path("blog/post/<slug:slug>/like/", PostLikeView.as_view(), name="post_like"),
    path(
        "blog/post/<slug:slug>/comment/",
        CommentCreateView.as_view(),
        name="comment_create",
    ),
    path(
        "blog/post/<slug:slug>/comment/<int:pk>/like/",
        CommentLikeView.as_view(),
        name="comment_like",
    ),
    # Archive view
    path("blog/archive/<int:year>/<int:month>/", ArchiveView.as_view(), name="archive"),
]
