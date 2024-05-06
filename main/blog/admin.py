from django import forms
from django.contrib import admin
from .models import Post

from tinymce.widgets import TinyMCE


class PostAdminForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["overview"].widget = forms.Textarea()
        self.fields["body"].widget = TinyMCE(attrs={"cols": 80, "rows": 30})


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    form = PostAdminForm
    list_display = ("title", "slug", "author", "publish", "status")
    list_filter = ("status", "created", "publish", "author")
    search_fields = ("title", "body")
    prepopulated_fields = {"slug": ("title",)}
    raw_id_fields = ("author",)
    date_hierarchy = "publish"
    ordering = ("status", "publish")
