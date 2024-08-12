from django.contrib import admin
from .models import Post, Category, Tag, Comment, Archive
from django.contrib import admin
from .models import Post
from tinymce.widgets import TinyMCE
from django import forms


class PostAdminForm(forms.ModelForm):
    content = forms.CharField(widget=TinyMCE(attrs={"cols": 80, "rows": 30}))

    class Meta:
        model = Post
        fields = "__all__"


class PostAdmin(admin.ModelAdmin):
    form = PostAdminForm


admin.site.register(Post, PostAdmin)

admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Comment)
admin.site.register(Archive)
