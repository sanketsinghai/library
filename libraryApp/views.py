from django.db import reset_queries
from django.shortcuts import redirect, render,get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
# Create your views here.
from .forms import AdminSigupForm,BookForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import *
def home(request):
    return render(request, 'home.html')

def main(request):
    context = {}
    context['segment'] = 'index'
    b=Book.objects.all()
    context['books']= b
    n=Book.objects.filter(status=False).count()
    context['issuedbook']=n
    n2=Book.objects.all().count()
    context['total']=n2
    context['available']=abs(n2-n)
    user=User.objects.all().count()
    context['totaluser']=user

    return render(request, 'index.html', context)

def register(request):
    form=AdminSigupForm()
    if request.method== 'POST':
        form=AdminSigupForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'Account was created for ' + user)
            return redirect("login")
    context={'form':form}
    return render(request, 'register.html',context)

def loginpage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password =request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('main')
        else:
            messages.info(request, 'Username OR password is incorrect')

    return render(request, 'login.html')

@login_required(login_url="login")
def logoutUser(request):
	logout(request)
	return redirect('login')

@login_required(login_url="login")
def bookdetails(request):
    b=Book.objects.all()
    context= {"books":b}
    return render(request, 'booklist.html', context) 

@login_required(login_url="login")
def addbook_view(request):
    #now it is empty book form for sending to html
    form=BookForm()
    if request.method=='POST':
        #now this form have data from html
        form=BookForm(request.POST)
        if form.is_valid():
            user=form.save()
            return redirect(main)
    return render(request,'addbook.html',{'form':form})



@login_required(login_url="login")
def deletebook(request, id=None):
    instance = get_object_or_404(Book, id=id)
    instance.delete()
    return redirect('main')


@login_required(login_url="login")
def updatestatus(request, id=None):
    instance = get_object_or_404(Book, id=id)
    if instance.status:
        instance.status=False
        instance.save()
        return redirect('main')
    else:
        instance.status=True
        instance.save()
        return redirect('main')
   