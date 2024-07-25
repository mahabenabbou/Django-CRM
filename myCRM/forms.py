from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Order,Customer,Product,Shipment,Task,ContactLog

class SignUpForm(UserCreationForm):
    email= forms.EmailField(label="",widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Email Address'}))
    first_name= forms.CharField(label="",max_length="100",widget=forms.TextInput(attrs={'class':'form-control','placeholder':'First Name'}))
    last_name = forms.CharField(label="",max_length="100",widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Last Name'}))

    class Meta :
        model = User
        fields = ('username','first_name', 'last_name','email','password1','password2')
    
    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'User Name'
        self.fields['username'].label = ''
        self.fields['username'].help_text = '<span class="form-text text-muted"><small>Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</small></span>'

        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password1'].label = ''
        self.fields['password1'].help_text = '<ul class="form-text text-muted small"><li>Your password can\'t be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can\'t be a commonly used password.</li><li>Your password can\'t be entirely numeric.</li></ul>'

        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
        self.fields['password2'].label = ''
        self.fields['password2'].help_text = '<span class="form-text text-muted"><small>Enter the same password as before, for verification.</small></span>'	



class AddOrderForm(forms.ModelForm):
    customer = forms.ModelChoiceField(queryset=Customer.objects.all(),required=True,widget=forms.Select(attrs={"class": "form-control"}),label="")
    delivery_date = forms.DateField(required=True,widget=forms.widgets.DateInput(attrs={"placeholder":"Delevery Date","class":"form-control"}),label="")
    status = forms.ChoiceField(choices=Order.STATUS_CHOICES,required=True,widget=forms.Select(attrs={"class": "form-control"}),label="")
    total_amount =forms.DecimalField(required=True,widget=forms.widgets.NumberInput(attrs={"placeholder":"Total Amount","class":"form-control"}),label="")
    special_file = forms.FileField(required=False,widget=forms.widgets.ClearableFileInput(attrs={"class": "form-control"}),label="")
    class Meta:
        model = Order
        exclude = ("user","order_date")


class AddProductForm(forms.ModelForm):
    name = forms.CharField(required=True, widget=forms.TextInput(attrs={"placeholder": "Name", "class": "form-control"}), label="")
    description = forms.CharField(required=False, widget=forms.Textarea(attrs={"placeholder": "Description", "class": "form-control"}), label="")
    price = forms.DecimalField(required=True, widget=forms.NumberInput(attrs={"placeholder": "Price", "class": "form-control"}), label="")
    stock = forms.IntegerField(required=True, widget=forms.NumberInput(attrs={"placeholder": "Stock", "class": "form-control"}), label="")
    picture = forms.ImageField(required=False, widget=forms.FileInput(attrs={"class": "form-control"}), label="")

    class Meta:
        model = Product
        exclude = ("user",)


class AddShipmentForm(forms.ModelForm):
    order = forms.ModelChoiceField(queryset=Order.objects.all(),required=True,widget=forms.Select(attrs={"class": "form-control"}),label="")
    shipment_date = forms.DateField(required=True,widget=forms.widgets.DateInput(attrs={"placeholder":"Shipment Date","class":"form-control"}),label="")
    tracking_number = forms.CharField(required=True, widget=forms.TextInput(attrs={"placeholder": "Tracking Number", "class": "form-control"}), label="")
    carrier = forms.CharField(required=True, widget=forms.TextInput(attrs={"placeholder": "Carrier", "class": "form-control"}), label="")
    status = forms.ChoiceField(choices=Shipment.STATUS_CHOICES,required=True,widget=forms.Select(attrs={"class": "form-control"}),label="")
    special_file = forms.FileField(required=False,widget=forms.widgets.ClearableFileInput(attrs={"class": "form-control"}),label="")
    class Meta:
        model = Shipment
        exclude = ("user",)



class AddTaskForm(forms.ModelForm):
    created_at = forms.DateField(required=True,widget=forms.widgets.DateInput(attrs={"placeholder":"Created at","class":"form-control"}),label="")
    title = forms.CharField(required=True, widget=forms.TextInput(attrs={"placeholder": "Title", "class": "form-control"}), label="")
    description = forms.CharField(required=False, widget=forms.Textarea(attrs={"placeholder": "Description", "class": "form-control"}), label="")
    due_date = forms.DateField(required=True,widget=forms.widgets.DateInput(attrs={"placeholder":"Due Date","class":"form-control"}),label="")
    status = forms.ChoiceField(choices=Task.STATUS_CHOICES,required=True,widget=forms.Select(attrs={"class": "form-control"}),label="")
    priority = forms.ChoiceField(choices=Task.PRIORITY_CHOICES,required=True,widget=forms.Select(attrs={"class": "form-control"}),label="")

    class Meta:
        model = Task
        exclude = ("user",'created_by', 'updated_by')

class AddContactLogForm(forms.ModelForm):
    customer = forms.ModelChoiceField(queryset=Customer.objects.all(),required=True,widget=forms.Select(attrs={"class": "form-control"}),label="")
    contact_date = forms.DateField(required=True,widget=forms.widgets.DateInput(attrs={"placeholder":"contact date","class":"form-control"}),label="")
    contact_method = forms.ChoiceField(choices=ContactLog.METHOD_CHOICES,required=True,widget=forms.Select(attrs={"class": "form-control"}),label="")
    notes = forms.CharField(required=True, widget=forms.TextInput(attrs={"placeholder": "Note", "class": "form-control"}), label="")
    class Meta:
        model = ContactLog
        exclude = ("user",'created_by', 'updated_by')