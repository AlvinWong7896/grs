from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from item.models import Item


@login_required
def index(request):
    latest_items = Item.objects.filter(is_sold=False).order_by("-created_on")[0:10]
    items = Item.objects.filter(created_by=request.user)

    return render(
        request,
        "dashboard/index.html",
        {
            "items": items,
            "latest_items": latest_items,
        },
    )
