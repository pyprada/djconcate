from django.http.response import HttpResponse
from django.shortcuts import redirect, render,HttpResponse
from soupsieve import comments
from .models import Post, BlogComment
from django.contrib import messages
from concateblog.templatetags import extra

# Create your views here.
def concateblogHome(request):
    allposts= Post.objects.all()
    context = {'allposts':allposts}
    # return HttpResponse('This is concateblogHome Page')
    return render(request, 'blog/blogHome.html', context)

def concateblogPost(request, slug):
    # return HttpResponse(f'This is concateblogPost Page {slug}') 
    post = Post.objects.filter(slug=slug).first()
    comments = BlogComment.objects.filter(post=post,parent=None)
    replies = BlogComment.objects.filter(post=post).exclude(parent=None)
    repDict={}
    for reply in replies:
        if reply.parent.sno not in repDict.keys():
            repDict[reply.parent.sno] = [reply]
        else:
            repDict[reply.parent.sno].append(reply)    

    context = {'post':post,'comments':comments, 'user':request.user, 'repDict':repDict}
    return render(request, 'blog/blogPost.html', context)

def postComment (request,):
    if request.method == 'POST':
        comment = request.POST.get("comment")
        user = request.user
        postsrno = request.POST.get("postsrno")
        post = Post.objects.get(srno=postsrno)
        parentsno = request.POST.get("parentsno")
        if parentsno == "":
            comment = BlogComment(comment=comment, user=user, post=post)
            comment.save()
            messages.success(request, "Your comment has been posted successfully")
        else:
            parent = BlogComment.objects.get(sno=parentsno)
            comment = BlogComment(comment=comment, user=user, post=post, parent=parent)
            comment.save()
            messages.success(request, "Your reply has been posted successfully")
    return redirect(f"/concateblog/{post.slug}")