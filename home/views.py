from django.shortcuts import render, HttpResponse, redirect
from home.models import Contact
from blog.models import Post
from django.contrib import messages
from django.contrib.auth import authenticate , login , logout
from django.contrib.auth.models import User
from django.db.models import F

# Create your views here.
def home(request):
    allpost = Post.objects.all()
   
    postDict={}
    for view in allpost:
        postDict[view.sno] = [view.viwes]
    postDict = sorted(postDict.items(), key=lambda x: x[1], reverse=True )  
    
    showPosts = []
    for i in postDict:
        showPosts.append(i[0] )
   
    context = {'allpost':allpost,'showPosts':showPosts[:3]}
    return render(request ,'home/home.html',context)


def contact(request):
    if request.method == 'POST' :
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        content = request.POST['content']
        
        if len(name)<3 or len(email)<3 or len(phone)<10 or len(content)<4:
            messages.error(request, 'Please Check All The Fields Are Filled Correctly')
        else:
            messages.success(request,'Your Message Has Been Successfully Sent ')
            contact = Contact(name = name,email=email,phone=phone,contact = content)
            contact.save()
    return render(request,'home/contact.html')

def about(request):
    return render(request,'home/about.html')


def search(request):
    query = request.GET['query']
    if len(query)>80 or len(query)==0:
        allpost = Post.objects.none()
    else:
        allpostTitle = Post.objects.filter(title__icontains = query)
        allpostContent = Post.objects.filter(content__icontains = query)
        allpostauthor = Post.objects.filter(author__icontains = query)
        allpost = allpostTitle.union(allpostContent,allpostauthor)
    if allpost.count()==0:
        messages.warning(request,"Sorry we cant find you what you want please clearify your query")
    params = {'allpost':allpost,'query':query} 
    return render(request,'home/search.html',params)

def signup(request):
    if request.method == 'POST' :
        
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        #crete check for signup
        #To Check Username
        if len(username)>10 :
            messages.error(request,"Username length should be less than 10 ")
            return redirect('home')
        if not username.isalnum():
            messages.error(request,"Username should contain only alphabets and numbers")
            return redirect('home')
        if pass1 != pass2 :
            messages.error(request,'Passwords do not match , please retry Sign UP')
            return redirect('home')
        #crete user
        myuser = User.objects.create_user(username,email,pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()
        messages.success(request,"Your iCoder Account has been created successfully")
        return redirect('home')
    else:
        return HttpResponse("404 - error")

def handellogin(request):
    if request.method == 'POST' :
        
        loginusername = request.POST['loginusername']
        loginpassword = request.POST['loginpassword']

        user = authenticate(username = loginusername ,password = loginpassword )
        if user is not None:
            login(request,user)
            messages.success(request,"LogIn Successfully")
            return redirect("home")
        else:
            messages.error(request,"Invalid Details")
            return redirect("home")
    else:
        return HttpResponse("404 - error")
def handellogout(request):
    logout(request)
    messages.success(request,'logout Successfully')
    return redirect("home")
    pass