from django.shortcuts import render, redirect
from django.http import HttpResponse
# Create your views here.
from blog.models import Post, BlogComment
from django.contrib import messages
from blog.templatetags import extras


def blogHome(request):
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("postContent")
        user = request.user
        views = 0
        print("postHeading: "+title+" --> "+content)
        post = Post(title=title, content=content,
                    author=user, views=views, slug=title)
        post.save()

        return redirect('/')
    allPosts = Post.objects.all()
    context = {"allPosts": allPosts, 'user': request.user}
    return render(request, 'blog/blogHome.html', context)


def blogPost(request, slug):
    post = Post.objects.filter(slug=slug).first()
    post.views = post.views+1
    post.save()
    comments = BlogComment.objects.filter(post=post, parent=None)
    replies = BlogComment.objects.filter(post=post).exclude(parent=None)
    replyDict = {}
    for reply in replies:
        if reply.parent.sno not in replyDict.keys():
            replyDict[reply.parent.sno] = [reply]
        else:
            replyDict[reply.parent.sno].append(reply)

    context = {'post': post, 'comments': comments,
               'user': request.user, 'replyDict': replyDict}
    return render(request, 'blog/blogPost.html', context)


def postComment(request):
    if request.method == "POST":
        comment = request.POST.get('comment')
        user = request.user
        postSno = request.POST.get('postSno')
        post = Post.objects.get(sno=postSno)
        parentSno = request.POST.get("parentSno")
        if parentSno == "":
            comment = BlogComment(comment=comment, user=user, post=post)
            messages.success(
                request, "Your comment has been posted successfully")
        else:
            parent = BlogComment.objects.get(sno=parentSno)
            comment = BlogComment(
                comment=comment, user=user, post=post, parent=parent)
            messages.success(
                request, "Your reply has been posted successfully")

        comment.save()

    return redirect(f"/blog/{post.slug}")
