from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

from item.models import Item
from .forms import ConversationMessageForm
from .models import Conversation


@login_required
def new_conversation(request, item_pk):
    latest_items = Item.objects.filter(is_sold=False).order_by("-created_on")[0:10]
    item = get_object_or_404(Item, pk=item_pk)

    if item.created_by == request.user:
        return redirect("dashboard:index")

    conversations = Conversation.objects.filter(item=item).filter(
        members__in=[request.user.id]
    )

    if conversations:
        return redirect("conversation:detail", pk=conversations.first().id)

    if request.method == "POST":
        form = ConversationMessageForm(request.POST)

        if form.is_valid():
            conversation = Conversation.objects.create(item=item)
            conversation.members.add(request.user)
            conversation.members.add(item.created_by)
            conversation.save()

            conversation_message = form.save(commit=False)
            conversation_message.conversation = conversation
            conversation_message.created_by = request.user
            conversation_message.save()

            return redirect("item:detail", pk=item_pk)
    else:
        form = ConversationMessageForm()

    return render(
        request,
        "conversation/new.html",
        {"form": form, "item": item, "latest_items": latest_items},
    )


@login_required
def inbox(request):
    latest_items = Item.objects.filter(is_sold=False).order_by("-created_on")[0:10]
    conversations = Conversation.objects.filter(members__in=[request.user.id])
    for conversation in conversations:
        conversation.item_name = conversation.item.name
        member_names = [member.username for member in conversation.members.all()]
        conversation.member_names = ", ".join(member_names)
    return render(
        request,
        "conversation/inbox.html",
        {"conversations": conversations, "latest_items": latest_items},
    )


@login_required
def detail(request, pk):
    latest_items = Item.objects.filter(is_sold=False).order_by("-created_on")[0:10]
    conversation = Conversation.objects.filter(members__in=[request.user.id]).get(pk=pk)
    conversation.item_name = conversation.item.name
    member_names = [member.username for member in conversation.members.all()]
    conversation.member_names = ", ".join(member_names)
    if request.method == "POST":
        form = ConversationMessageForm(request.POST)

        if form.is_valid():
            conversation_message = form.save(commit=False)
            conversation_message.conversation = conversation
            conversation_message.created_by = request.user
            conversation_message.save()

            conversation.save()

            return redirect("conversation:detail", pk=pk)
    else:
        form = ConversationMessageForm()

    return render(
        request,
        "conversation/detail.html",
        {
            "conversation": conversation,
            "form": form,
            "conversation.item_name": conversation.item_name,
            "latest_items": latest_items,
        },
    )
