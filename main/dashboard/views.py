from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from item.models import Item
from conversation.models import Conversation


@login_required
def index(request):
    latest_items = Item.objects.filter(is_sold=False).order_by("-created_on")[0:10]
    items = Item.objects.filter(created_by=request.user)
    conversations = Conversation.objects.filter(members__in=[request.user.id])

    for conversation in conversations:
        conversation.item_name = conversation.item.name
        member_names = [member.username for member in conversation.members.all()]
        conversation.member_names = ", ".join(member_names)

    return render(
        request,
        "dashboard/index.html",
        {
            "items": items,
            "latest_items": latest_items,
            "conversations": conversations,
        },
    )
