from django.shortcuts import render
from blog.models import Post, Comment
from blog.forms import CommentForm
from django.http import HttpResponseRedirect

# Create your views here.


def blog_index(request):
    """Displays all of the posts."""
    posts = Post.objects.all().order_by("-created_on")
    context = {
        "posts": posts,
    }
    return render(request, "blog/index.html", context=context)


def blog_detail(request, pk):
    """Displays full post along with comments."""
    post = Post.objects.get(pk=pk)
    form = CommentForm()
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = Comment(
                author=form.cleaned_data["author"],
                body=form.cleaned_data["body"],
                post=post,
            )
            comment.save()
            return HttpResponseRedirect(request.path_info)

    comments = Comment.objects.filter(post=post)
    context = {
        "post": post,
        "comments": comments,
        "form": CommentForm(),
    }
    return render(request, "blog/detail.html", context=context)


def blog_category(request, category):
    """Posts are shown based on categories."""
    posts = Post.objects.filter(
        categories__name__contains=category).order_by('-created_on')
    context = {
        "category": category,
        "posts": posts,
    }

    return render(request, "blog/category.html", context=context)
