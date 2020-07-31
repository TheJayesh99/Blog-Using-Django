from django.shortcuts import render,HttpResponse,redirect
from blog.models import Post , Blogcomment
from django.contrib import messages
from blog.templatetags import extras


# Create your views here.

def BlogHome(request):
    allpost = Post.objects.all()
 
    context = {'allpost':allpost}
    return render(request,'blog/blog.html',context)

def BlogPost(request,slug):
    allpost = Post.objects.all()
    post = Post.objects.filter(slug = slug).first()
    
    comment = Blogcomment.objects.filter(post=post,parent=None)
    replys = Blogcomment.objects.filter(post=post).exclude(parent=None)
    replyDict={}
    for reply in replys:
        if reply.parent.sno not in replyDict.keys():
            replyDict[reply.parent.sno] = [reply]
        else:
            replyDict[reply.parent.sno].append(reply)
    
    context = {'post':post,'allpost':allpost,'comments': comment,'replyDict':replyDict}
    post.viwes = post.viwes+1
    post.save()
    return render(request,'blog/blogpost.html',context)


def postComment(request):
    if request.method=='POST':
        comment = request.POST['comment']
        user = request.user
        postSno = request.POST['postSno'] 
        post = Post.objects.get(sno=postSno)
        parentSno = request.POST['parentSno']
        if parentSno =="":
            comment = Blogcomment(comment=comment,user=user,post=post)
            comment.save()
            messages.success(request,"Your comment has been posted successfully")
        else:
            parent = Blogcomment.objects.get(sno=parentSno)
            comment = Blogcomment(comment=comment,user=user,post=post,parent=parent)
            comment.save()
            messages.success(request,"Your Reply has been posted successfully")
 
    return redirect(f'/blog/{post.slug}')  