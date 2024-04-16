import time
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect

from .forms import NewItemForm, EditItemForm
from .models import Category, Item


def marketplace(request):
    if request.user.is_authenticated:
        latest_items = Item.objects.filter(is_sold=False).order_by("-created_on")[0:10]
        items = (
            Item.objects.filter(is_sold=False)
            .exclude(created_by=request.user)
            .order_by("-created_on")
        )
    else:
        latest_items = Item.objects.filter(is_sold=False).order_by("-created_on")[0:10]
        items = Item.objects.filter(is_sold=False).order_by("-created_on")
    categories = Category.objects.all()

    return render(
        request,
        "item/marketplace.html",
        {
            "categories": categories,
            "latest_items": latest_items,
            "items": items,
        },
    )


def items(request):
    query = request.GET.get("query", "")
    category_id = request.GET.get("category", 0)
    categories = Category.objects.all()
    items = Item.objects.filter(is_sold=False)

    if category_id:
        items = items.filter(category_id=category_id)

    if query:
        items = items.filter(Q(name__icontains=query) | Q(description__icontains=query))

    return render(
        request,
        "item/items.html",
        {
            "items": items,
            "query": query,
            "categories": categories,
            "category_id": int(category_id),
        },
    )


def detail(request, pk):
    item = get_object_or_404(Item, pk=pk)
    related_items = Item.objects.filter(category=item.category, is_sold=False).exclude(
        pk=pk
    )[0:6]

    return render(
        request, "item/detail.html", {"item": item, "related_items": related_items}
    )


@login_required
def new(request):
    if request.method == "POST":
        form = NewItemForm(request.POST, request.FILES)

        if form.is_valid():
            item = form.save(commit=False)
            item.created_by = request.user
            item.save()

            return redirect("item:detail", pk=item.id)
    else:
        form = NewItemForm(request.POST or None, request.FILES or None)
        form.full_clean()
    print(form.errors)
    return render(
        request,
        "item/form.html",
        {
            "form": form,
            "title": "New item",
        },
    )


@login_required
def delete(request, pk):
    item = get_object_or_404(Item, pk=pk, created_by=request.user)
    item.delete()

    return redirect("dashboard:index")


@login_required
def edit(request, pk):
    item = get_object_or_404(Item, pk=pk, created_by=request.user)

    if request.method == "POST":
        form = EditItemForm(request.POST, request.FILES, instance=item)

        if form.is_valid():
            item.save()

            return redirect("item:detail", pk=item.id)
    else:
        form = EditItemForm(instance=item)

    return render(
        request,
        "item/form.html",
        {
            "form": form,
            "title": "Edit item",
        },
    )
