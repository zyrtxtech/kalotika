from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import ListView, DetailView
from .models import Post, Category, Tag, Comment, Archive
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import DetailView
from .models import Post, Comment
from .forms import CommentForm


class PostListView(ListView):
    model = Post
    template_name = "blog/post_list.html"  # Specify your own template name/location
    context_object_name = "posts"
    paginate_by = 10  # Paginate your posts if needed


class PostDetailView(DetailView):
    model = Post
    template_name = "blog/post_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        context["total_likes"] = post.total_likes()
        context["is_liked"] = post.likes.filter(id=self.request.user.id).exists()
        context["comments"] = Comment.objects.filter(post=post, approved=True).order_by(
            "-created_at"
        )
        context["comment_form"] = CommentForm()
        return context


def like_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    return HttpResponseRedirect(reverse("post_detail", args=[slug]))


def add_comment(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return HttpResponseRedirect(reverse("post_detail", args=[slug]))
    return redirect("post_detail", slug=slug)


class CategoryListView(ListView):
    model = Category
    template_name = "blog/category_list.html"
    context_object_name = "categories"


class CategoryDetailView(DetailView):
    model = Category
    template_name = "blog/category_detail.html"
    context_object_name = "category"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = self.get_object()
        context["posts"] = category.posts.all()
        return context


class TagListView(ListView):
    model = Tag
    template_name = "blog/tag_list.html"
    context_object_name = "tags"


class TagDetailView(DetailView):
    model = Tag
    template_name = "blog/tag_detail.html"
    context_object_name = "tag"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["posts"] = Post.objects.filter(tags=self.object)
        return context


class PostLikeView(View):
    def post(self, request, slug):
        post = get_object_or_404(Post, slug=slug)
        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)
        return redirect("post_detail", slug=slug)


class CommentCreateView(View):
    def post(self, request, slug):
        post = get_object_or_404(Post, slug=slug)
        content = request.POST.get("content")
        Comment.objects.create(
            post=post,
            author=request.user.username,
            email=request.user.email,
            content=content,
        )
        return redirect("post_detail", slug=slug)


class CommentLikeView(View):
    def post(self, request, slug, pk):
        comment = get_object_or_404(Comment, id=pk)
        if comment.comment_likes.filter(id=request.user.id).exists():
            comment.comment_likes.remove(request.user)
        else:
            comment.comment_likes.add(request.user)
        return redirect("post_detail", slug=slug)


class ArchiveView(ListView):
    template_name = "blog/archive.html"
    context_object_name = "posts"

    def get_queryset(self):
        year = self.kwargs["year"]
        month = self.kwargs["month"]
        return Post.objects.filter(published_at__year=year, published_at__month=month)
