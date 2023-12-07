from django.db import models


class Emails(models.Model):
    subject = models.CharField(max_length=100)
    message = models.TextField(max_length=1000)
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    edited_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.id
