from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Conversation, ConversationMessage


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ("item", "created_at", "modified_at")
    list_filter = ("created_at", "modified_at")


@admin.register(ConversationMessage)
class ConversationMessageAdmin(admin.ModelAdmin):
    list_display = ("conversation", "created_at", "created_by")
    list_filter = ("created_by", "created_at")
