from django.shortcuts import render,  redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm
from .models import Customer,Order,Product,OrderItem,Shipment,Task,ContactLog

# Create your views here.

def home(request):
    #check to see if logging in 
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        #authenticate
        user = authenticate(request , username=username ,password=password )
        if user is not None :
            login(request , user)
            messages.success(request , "You have been logged in " )
            return redirect('home')
        else :
            messages.success(request, "Their was an error logging in please try again  ...")
            return redirect('home')
    else :
        return render(request , 'home.html' , {})



def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out ")
    return redirect('home')


def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            # Authentification and login 
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user =authenticate(username=username,password=password)
            login(request,user)
            messages.success(request,'regiter.html',"You Have Successfuly Register")
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request , 'register.html' , {'form':form})

def customers(request):
    customers  = Customer.objects.all()
    return render(request,"customers.html",{'customers': customers})

def orders(request):
    orders  = Order.objects.all()
    return render(request,"orders.html",{'orders': orders})

def products(request):
    products  = Product.objects.all()
    return render(request,"products.html",{'products': products})

def shipments(request):
    shipments  = Shipment.objects.all()
    return render(request,"shipments.html",{'shipments': shipments})

def tasks(request):
    tasks  = Task.objects.all()
    return render(request,"tasks.html",{'tasks': tasks})

def contactlogs(request):
    contactlogs = ContactLog.objects.all()
    return render(request,"contactlogs.html", {'contactlogs':contactlogs})