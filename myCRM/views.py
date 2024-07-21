from django.shortcuts import render,  redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import SignUpForm,AddOrderForm
from .models import Customer,Order,Product,OrderItem,Shipment,Task,ContactLog
from datetime import datetime


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

def moreinfo(request,pk):
    if request.user.is_authenticated:
        moreinfo=Order.objects.get(id=pk)
        return render(request , 'moreinfo.html' , {'moreinfo': moreinfo})
    else:
        messages.success(request,"you must be logged in to view that page")
        return redirect('home')

def delete(request,pk):
    if request.user.is_authenticated:
        delete_it=Order.objects.get(id=pk)
        delete_it.delete()
        messages.success(request,"Order Deleted Successfully !")
        return redirect('orders')
    else:
        messages.success(request,"You Must LogIn First  !")
        return redirect('home')
    
def add(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = AddOrderForm(request.POST, request.FILES)
            if form.is_valid():
                order = form.save(commit=False)
                order.user = request.user
                order.order_date = datetime.now()  # Set the order date to the current date and time
                order.save()
                messages.success(request, "Order Added Successfully!")
                return redirect('orders')
        else:
            form = AddOrderForm()
        
        return render(request, "add.html", {'form': form})
    else:
        messages.success(request, "You must be logged in first!")
        return redirect('home')
    
def update(request, pk):
    if request.user.is_authenticated:
        current_order = Order.objects.get(id=pk)
        form = AddOrderForm(request.POST or None, instance=current_order)
        if form.is_valid():
            form.save()
            messages.success(request, "Record Has Been Updated!")
            return redirect('orders')
        return render(request, "update.html", {'form': form, 'pk': pk})
    else:
        messages.warning(request, "You must be logged in.")
        return redirect('home')