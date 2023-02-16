from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
from blog.models import Post


def blogHome(request):
    allPosts = Post.objects.all()
    context = {"allPosts": allPosts}
    return render(request, 'blog/blogHome.html', context)


def blogPost(request, slug):
    post = Post.objects.filter(slug=slug)
    return render(request, 'blog/blogPost.html', {'post': post[0]})
