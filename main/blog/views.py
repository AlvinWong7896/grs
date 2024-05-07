from django.shortcuts import render, get_object_or_404
from .models import Post
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from item.models import Item


def home(request):
    return render(request, "core/index.html")


def post_list(request):
    latest_items = Item.objects.filter(is_sold=False).order_by("-created_on")[0:10]
    object_list = Post.published.all()
    paginator = Paginator(object_list, 4)  # 4 posts in each page
    page = request.GET.get("page")
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)
    return render(
        request,
        "blog/post/list.html",
        {"page": page, "posts": posts, "latest_items": latest_items},
    )


def post_detail(request, year, month, day, post):
    latest_items = Item.objects.filter(is_sold=False).order_by("-created_on")[0:10]
    post = get_object_or_404(
        Post,
        slug=post,
        status="published",
        publish__year=year,
        publish__month=month,
        publish__day=day,
    )
    return render(
        request, "blog/post/detail.html", {"post": post, "latest_items": latest_items}
    )
