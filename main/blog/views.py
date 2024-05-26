from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from .models import Post
from item.models import Item


def home(request):
    return render(request, "core/index.html")


@login_required
def user_blog_posts(request):
    user = request.user
    latest_items = Item.objects.filter(is_sold=False).order_by("-created_on")[0:8]
    object_list = Post.objects.filter(author=user, status="published")
    paginator = Paginator(object_list, 4)  # 4 posts per page
    page = request.GET.get("page")
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(
        request,
        "blog/user_posts.html",
        {"page": page, "posts": posts, "latest_items": latest_items},
    )


def post_list(request):
    latest_items = Item.objects.filter(is_sold=False).order_by("-created_on")[0:8]
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


def search(request):
    # subjects = Subject.objects.all()
    object_list = Post.published.all()
    query = request.GET.get("query")

    if query:
        object_list = object_list.filter(
            Q(title__icontains=query)
            | Q(overview__icontains=query)
            | Q(body__icontains=query)
        )

    # subject_id = request.GET.get("subject")
    # if subject_id:
    #     posts = posts.filter(subject_id=subject_id)

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
        {
            "posts": posts,
            "page": page,
            # "subjects": subjects,
        },
    )


@csrf_exempt
@login_required
def upload_image(request):
    pass
