from email.mime import message
from django.db.models import query
from django.shortcuts import render,HttpResponse, redirect
from .models import Contact
from django.contrib import messages
from concateblog.models import Post
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

# Create your views here.
def home(request):
    
    return render(request, 'home/home.html')

def quiz(request):
    
    return render(request, 'home/quiz.html')
       

def about(request):
    
    # messages.success(request, 'Welcome To About!')
    return render(request, 'home/about.html')


def contact(request):
    
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        content = request.POST['content']
        # print(name,email,phone,content)

        if len(name)<2 or len(email)<5 or len(phone)<10 or len(content)<2:
            messages.error(request,'Please fill form correctly.')
        else:    
            contact = Contact(name=name,email=email,phone=phone,content=content)
            contact.save()
            messages.success(request,'form submitted successfully')

    return render(request, 'home/contact.html')
   
    
def search(request):
    query= request.GET['query']
    if len(query) >50:
        allPosts = Post.objects.none()
    else:    
        # allPosts = Post.objects.all()
        allPoststitle = Post.objects.filter(title__icontains=query)
        allPostsContent = Post.objects.filter(content__icontains=query)
        allPosts = allPoststitle.union(allPostsContent)
    if allPosts.count()== 0:
        messages.warning(request,'No Search results found,Please refine your query.')   
    params = {'allPosts':allPosts,'query':query}
    return render(request, 'home/search.html', params)
    # return HttpResponse('This is Search')

def submitSignup(request):
    if request.method == 'POST':
        # Get the post parameters
        uname = request.POST['uname']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1= request.POST['pass1']
        pass2 = request.POST['pass2']

        #validation
        if len(uname) > 10:
            messages.error(request,"Username must be under 10 characters")
            return redirect('home')

        if not uname.isalnum():
            messages.error(request,"Username must be contains only letters & numbers")
            return redirect('home')    

        if pass1 != pass2:
            messages.error(request,"Password do not match")
            return redirect('home')    

        # create the user
        myuser = User.objects.create_user(uname, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()
        messages.success(request, 'Your account has been created successfully.')
        return redirect('home')


    else:
        return HttpResponse('404-not found')    


def submitLogin(request):
    if request.method == 'POST':
        # Get the post parameters
        loginuname = request.POST['loginuname']
        loginpass =  request.POST['loginpass']

        user = authenticate(username=loginuname, password=loginpass)

        if user is not None:
            login(request, user)
            messages.success(request, 'Successfully Logged In')
            return redirect("home")
        else:
            messages.error(request, "Invalid Credentials,Please Try Again")
            return redirect("home")    

    return HttpResponse("404-Not Found")
    

def submitLogout(request):
        logout(request)
        messages.success(request, 'Logout Successfully')
        return redirect("home")
    
        
