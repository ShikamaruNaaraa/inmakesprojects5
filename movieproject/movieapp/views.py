from django.contrib import messages, auth
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Movie
from .forms import MovieForm

# Create your views here.
def index(request):
    movie=Movie.objects.all()
    context={'movie':movie}
    return render(request,'index.html',context)

def details(request,movie_id):
    movie=Movie.objects.get(id=movie_id)
    context = {'movie': movie}
    return render(request,'details.html',context)

def add_movie(request):
    if request.method=='POST':
        name=request.POST.get('name',)
        desc = request.POST.get('desc', )
        year = request.POST.get('year', )
        img = request.FILES['img']
        movie=Movie(name=name,desc=desc,year=year,img=img)
        movie.save()
    return render(request,'add.html')

def update(request,id):
    movie=Movie.objects.get(id=id)
    form=MovieForm(request.POST or None,request.FILES,instance=movie)
    if form.is_valid():
        form.save()
        return redirect('/')
    return render(request,'edit.html',{'movie':movie,'form':form})

def delete(request,id):
    if request.method=='POST':
        movie=Movie.objects.get(id=id)
        movie.delete()
        return redirect('/')
    return render(request,'delete.html')


# Create your views here.

def register(request):
    if request.method == 'POST':
        username=request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        cpassword = request.POST['cpassword']
        if password == cpassword:
            if User.objects.filter(email=email).exists():
                messages.info(request, "Email Taken")
                return redirect('/register')
            elif User.objects.filter(username=username).exists():
                messages.info(request, "Username Taken")
                return redirect('/register')
            else:
                user = User.objects.create_user(username=username,email=email, password=password, first_name=first_name, last_name=last_name)
                user.save();
                print("User created")
                return redirect('/login')
        else:
            messages.info(request, "Password not matching")
            return redirect('/register')
    return render(request, 'register.html')


def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(email=email, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, "Invalid User")
            return redirect('/login')
    return render(request,'login.html')

def logout(request):
    auth.logout(request)
    return redirect('/')
