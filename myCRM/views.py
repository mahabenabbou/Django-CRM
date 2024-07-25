from django.shortcuts import render,  redirect,get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import SignUpForm,AddOrderForm,AddProductForm, AddShipmentForm, AddTaskForm, AddContactLogForm
from .models import Customer,Order,Product,OrderItem,Shipment,Task,ContactLog
from datetime import datetime
from django.db.models.functions import TruncMonth
from django.db.models import Count
from django.http import JsonResponse

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
    else:    
        if request.user.is_authenticated:
            context = {
                'num_customers': Customer.objects.count(),
                'num_orders': Order.objects.count(),
                'num_products': Product.objects.count(),
                'num_shipments': Shipment.objects.count(),
                'num_tasks': Task.objects.filter(status__in=['Pending', 'In Progress']).count()
            }
            return render(request, 'home.html', context)
        else:
            return render(request, 'home.html', {})



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
    if request.user.is_authenticated:
        if request.user.is_staff:  # Assuming managers are staff
            tasks = Task.objects.all()
        else:
            tasks = Task.objects.filter(assigned_to=request.user)
        return render(request, "tasks.html", {'tasks': tasks})
    else:
        messages.success(request, "You must be logged in to view tasks!")
        return redirect('home')

def contactlogs(request):
    contactlogs = ContactLog.objects.all()
    return render(request,"contactlogs.html", {'contactlogs':contactlogs})

def orderitems(request):
    orderitems = OrderItem.objects.all()
    return render(request,"orderitems.html", {'orderitems':orderitems})



def moreinfoOrder(request,pk):
    if request.user.is_authenticated:
        moreinfoOrder=Order.objects.get(id=pk)
        return render(request , 'moreinfoOrder.html' , {'moreinfoOrder': moreinfoOrder})
    else:
        messages.success(request,"you must be logged in to view that page")
        return redirect('home')

def deleteOrder(request,pk):
    if request.user.is_authenticated:
        delete_itOrder=Order.objects.get(id=pk)
        delete_itOrder.delete()
        messages.success(request,"Order Deleted Successfully !")
        return redirect('orders')
    else:
        messages.success(request,"You Must LogIn First  !")
        return redirect('home')
    
def addOrder(request):
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
        
        return render(request, "addOrder.html", {'form': form})
    else:
        messages.success(request, "You must be logged in first!")
        return redirect('home')
    
def updateOrder(request, pk):
    if request.user.is_authenticated:
        current_order = Order.objects.get(id=pk)
        form = AddOrderForm(request.POST or None, instance=current_order)
        if form.is_valid():
            form.save()
            messages.success(request, "Record Has Been Updated!")
            return redirect('orders')
        return render(request, "updateOrder.html", {'form': form, 'pk': pk})
    else:
        messages.warning(request, "You must be logged in.")
        return redirect('home')
    





def moreinfoProduct(request,pk):
    if request.user.is_authenticated:
        moreinfoProduct=Product.objects.get(id=pk)
        return render(request , 'moreinfoProduct.html' , {'moreinfoProduct': moreinfoProduct})
    else:
        messages.success(request,"you must be logged in to view that page")
        return redirect('home')

def deleteProduct(request,pk):
    if request.user.is_authenticated and request.user.is_staff :
        delete_itProduct=Product.objects.get(id=pk)
        delete_itProduct.delete()
        messages.success(request,"Product Deleted Successfully !")
        return redirect('products')
    else:
        messages.success(request,"You are not allowed to delete this product !")
        return redirect('home')
    
def addProduct(request):
    if request.user.is_authenticated and request.user.is_staff :
        if request.method == "POST":
            form = AddProductForm(request.POST, request.FILES)
            if form.is_valid():
                product = form.save(commit=False)
                product.user = request.user
                product.Product_date = datetime.now()  # Set the Product date to the current date and time
                product.save()
                messages.success(request, "Product Added Successfully!")
                return redirect('products')
        else:
            form = AddProductForm()
        
        return render(request, "addProduct.html", {'form': form})
    else:
        messages.success(request, "You are not allowed to add a product !")
        return redirect('home')
    
def updateProduct(request, pk):
    if request.user.is_authenticated and request.user.is_staff:
        product = get_object_or_404(Product, pk=pk)
        if request.method == 'POST':
            form = AddProductForm(request.POST, request.FILES, instance=product)
            if form.is_valid():
                form.save()
                messages.success(request, "Product updated successfully!")
                return redirect('products')
        else:
            form = AddProductForm(instance=product)
        return render(request, 'updateProduct.html', {'form': form, 'pk': pk})
    else:
        messages.success(request, "You must be logged in and be an admin to update products!")
        return redirect('home')




def moreinfoShipment(request,pk):
    if request.user.is_authenticated:
        moreinfoShipment=Shipment.objects.get(id=pk)
        return render(request , 'moreinfoShipment.html' , {'moreinfoShipment': moreinfoShipment})
    else:
        messages.success(request,"you must be logged in to view that page")
        return redirect('home')

def deleteShipment(request,pk):
    if request.user.is_authenticated:
        delete_itShipment=Shipment.objects.get(id=pk)
        delete_itShipment.delete()
        messages.success(request,"Shipment Deleted Successfully !")
        return redirect('shipements')
    else:
        messages.success(request,"You Must LogIn First  !")
        return redirect('home')
    
def addShipment(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = AddShipmentForm(request.POST, request.FILES)
            if form.is_valid():
                shipment = form.save(commit=False)
                shipment.user = request.user
                shipment.shipment_date = datetime.now()  # Set the shipment date to the current date and time
                shipment.save()
                messages.success(request, "Shipment Added Successfully!")
                return redirect('shipements')
        else:
            form = AddShipmentForm()
        
        return render(request, "addShipment.html", {'form': form})
    else:
        messages.success(request, "You must be logged in first!")
        return redirect('home')
    
def updateShipment(request, pk):
    if request.user.is_authenticated:
        current_shipement = Shipment.objects.get(id=pk)
        form = AddShipmentForm(request.POST or None, instance=current_shipement)
        if form.is_valid():
            form.save()
            messages.success(request, "Record Has Been Updated!")
            return redirect('shipments')
        return render(request, "updateShipment.html", {'form': form, 'pk': pk})
    else:
        messages.warning(request, "You must be logged in.")
        return redirect('home')
    



def moreinfoTask(request, pk):
    if request.user.is_authenticated:
        task = get_object_or_404(Task, id=pk)
        if request.user == task.assigned_to or request.user.is_staff:
            return render(request, 'moreinfoTask.html', {'moreinfoTask': task})  # Ensure the context key matches the template
        else:
            messages.success(request, "You are not authorized to view this task!")
            return redirect('tasks')
    else:
        messages.success(request, "You must be logged in to view this page!")
        return redirect('home')
    
def deleteTask(request,pk):
    if request.user.is_authenticated and request.user.is_staff:
        delete_itTask = Task.objects.get(id=pk)
        delete_itTask.delete()
        messages.success(request, "Task Deleted Successfully!")
        return redirect('tasks')
    else:
        messages.success(request, "You must be logged in and be an admin to delete tasks!")
        return redirect('home')
    
def addTask(request):
    if request.user.is_authenticated and request.user.is_staff:
        if request.method == "POST":
            form = AddTaskForm(request.POST, request.FILES)
            if form.is_valid():
                task = form.save(commit=False)
                task.created_by = request.user
                task.save()
                messages.success(request, "Task Added Successfully!")
                return redirect('tasks')
        else:
            form = AddTaskForm()
        
        return render(request, "addTask.html", {'form': form})
    else:
        messages.success(request, "You must be logged in and be an admin to create a task!")
        return redirect('home')
    
def updateTask(request, pk):
    if request.user.is_authenticated:
        current_task = Task.objects.get(id=pk)
        if request.user == current_task.assigned_to or request.user.is_staff:
            form = AddTaskForm(request.POST or None, instance=current_task)
            if form.is_valid():
                form.save()
                messages.success(request, "Record Has Been Updated!")
                return redirect('tasks')
            return render(request, "updateTask.html", {'form': form, 'pk': pk})
        else:
            messages.warning(request, "You are not authorized to update this task.")
            return redirect('tasks')
    else:
        messages.warning(request, "You must be logged in.")
        return redirect('home')



def moreinfoContactLog(request,pk):
    if request.user.is_authenticated:
        moreinfoContactLog=ContactLog.objects.get(id=pk)
        return render(request , 'moreinfoContactLog.html' , {'moreinfoContactLog': moreinfoContactLog})
    else:
        messages.success(request,"you must be logged in to view that page")
        return redirect('home')

def deleteContactLog(request,pk):
    if request.user.is_authenticated:
        delete_itcontactlog=ContactLog.objects.get(id=pk)
        delete_itcontactlog.delete()
        messages.success(request,"contactlog Deleted Successfully !")
        return redirect('contactlogs')
    else:
        messages.success(request,"You Must LogIn First  !")
        return redirect('home')
    
def addContactLog(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = AddContactLogForm(request.POST, request.FILES)
            if form.is_valid():
                contactlog = form.save(commit=False)
                contactlog.user = request.user
                contactlog.contactlog_date = datetime.now()  # Set the contactlog date to the current date and time
                contactlog.save()
                messages.success(request, "contactlog Added Successfully!")
                return redirect('contactlogs')
        else:
            form = AddContactLogForm()
        
        return render(request, "addContactLog.html", {'form': form})
    else:
        messages.success(request, "You must be logged in first!")
        return redirect('home')
    
def updateContactLog(request, pk):
    if request.user.is_authenticated:
        current_shipement = ContactLog.objects.get(id=pk)
        form = AddContactLogForm(request.POST or None, instance=current_shipement)
        if form.is_valid():
            form.save()
            messages.success(request, "Record Has Been Updated!")
            return redirect('contactlogs')
        return render(request, "updateContactLog.html", {'form': form, 'pk': pk})
    else:
        messages.warning(request, "You must be logged in.")
        return redirect('home')
    
def orders_per_month_view(request):
    orders_per_month = Order.objects.annotate(
        month=TruncMonth('order_date')
    ).values('month').annotate(
        count=Count('id')
    ).order_by('month')

    data = {
        'months': [entry['month'].strftime('%Y-%m') for entry in orders_per_month],
        'counts': [entry['count'] for entry in orders_per_month],
    }

    # Print data to console for debugging
    print(data)

    return JsonResponse(data)