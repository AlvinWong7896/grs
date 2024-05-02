from django import forms
from django.contrib import admin
from .models import Post
from tinymce.widgets import TinyMCE


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    body = forms.CharField(widget=TinyMCE(attrs={"cols": 80, "rows": 30}))
    list_display = ("title", "slug", "author", "publish", "status")
    list_filter = ("status", "created", "publish", "author")
    search_fields = ("title", "body")
    prepopulated_fields = {"slug": ("title",)}
    raw_id_fields = ("author",)
    date_hierarchy = "publish"
    ordering = ("status", "publish")
