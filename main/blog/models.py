from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User
from PIL import Image
from tinymce.models import HTMLField
import os, tempfile


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status="published")


class Post(models.Model):
    STATUS_CHOICES = (
        ("draft", "Draft"),
        ("published", "Published"),
    )
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique_for_date="publish")
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="blog_posts"
    )
    thumbnail = models.ImageField(
        default="images/default_photo.jpg", upload_to="images/"
    )
    overview = models.TextField(blank=True)
    body = HTMLField(blank=True, null=False, default="")
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="draft")

    class Meta:
        ordering = ("-publish",)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse(
            "blog:post_detail",
            args=[self.publish.year, self.publish.month, self.publish.day, self.slug],
        )

    objects = models.Manager()  # The default manager.
    published = PublishedManager()  # Our custom manager.

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        for image_field in [self.thumbnail]:
            if image_field:
                image_path = image_field.path
                img = Image.open(image_path)
                if img.height > 500 or img.width > 500:
                    output_size = (500, 500)
                    img.thumbnail(output_size)
                    # Overwrite the original image file with the resized one
                    img.save(image_path)
