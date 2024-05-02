import time
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect

from .forms import NewItemForm, EditItemForm
from .models import Category, Item


def marketplace(request, category_id=None):
    if request.user.is_authenticated:
        latest_items = Item.objects.filter(is_sold=False).order_by("-created_on")[0:6]
        items = (
            Item.objects.filter(is_sold=False)
            .exclude(created_by=request.user)
            .order_by("-created_on")
        )
    else:
        latest_items = Item.objects.filter(is_sold=False).order_by("-created_on")[0:6]
        items = Item.objects.filter(is_sold=False).order_by("-created_on")

    paginator = Paginator(items, 20)  # 20 items per page
    page = request.GET.get("page")
    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver the first page
        items = paginator.page(1)
    except EmptyPage:
        # If page is out of range, deliver last page of results
        items = paginator.page(paginator.num_pages)

    categories = Category.objects.all()
    if category_id is not None:
        category = get_object_or_404(Category, id=category_id)
        items = items.filter(category=category)
    return render(
        request,
        "item/marketplace.html",
        {
            "categories": categories,
            "latest_items": latest_items,
            "page": page,
            "items": items,
        },
    )


def search(request):
    items = Item.objects.filter(is_sold=False)
    categories = Category.objects.all()

    query = request.GET.get("query")
    if query:
        items = items.filter(Q(name__icontains=query) | Q(description__icontains=query))

    category_id = request.GET.get("category")
    if category_id:
        items = items.filter(category_id=category_id)

    min_price = request.GET.get("min_price")
    max_price = request.GET.get("max_price")
    if min_price and max_price:
        items = items.filter(price__gte=min_price, price__lte=max_price)
    elif min_price:
        items = items.filter(price__gte=min_price)
    elif max_price:
        items = items.filter(price__lte=max_price)

    material = request.GET.get("material")
    if material:
        items = items.filter(material=material)

    frame_size = request.GET.get("frame_size")
    if frame_size:
        items = items.filter(frame_size=frame_size)

    tire_size = request.GET.get("tire_size")
    if tire_size:
        items = items.filter(tire_size=tire_size)

    brake_type = request.GET.get("brake_type")
    if brake_type:
        items = items.filter(brake_type=brake_type)

    return render(
        request,
        "item/marketplace.html",
        {
            "items": items,
            "categories": categories,
        },
    )


def detail(request, pk):
    latest_items = Item.objects.filter(is_sold=False).order_by("-created_on")[0:6]
    item = get_object_or_404(Item, pk=pk)
    related_items = Item.objects.filter(category=item.category, is_sold=False).exclude(
        pk=pk
    )[0:12]

    total_images = 1
    if item.image_2:
        total_images += 1
    if item.image_3:
        total_images += 1
    if item.image_4:
        total_images += 1
    return render(
        request,
        "item/detail.html",
        {
            "item": item,
            "related_items": related_items,
            "total_images": total_images,
            "latest_items": latest_items,
        },
    )


@login_required
def new(request):
    latest_items = Item.objects.filter(is_sold=False).order_by("-created_on")[0:6]
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
            "latest_items": latest_items,
        },
    )


@login_required
def delete(request, pk):
    latest_items = Item.objects.filter(is_sold=False).order_by("-created_on")[0:6]
    item = get_object_or_404(Item, pk=pk, created_by=request.user)
    item.delete()

    return redirect("dashboard:index")


@login_required
def edit(request, pk):
    latest_items = Item.objects.filter(is_sold=False).order_by("-created_on")[0:6]
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
            "latest_items": latest_items,
        },
    )
