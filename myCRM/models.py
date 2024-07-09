from django.db import models

from django.contrib.auth.models import User




class Customer(models.Model):
    company_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=10)  # Changement en CharField pour plus de flexibilité
    notes = models.TextField(blank=True, null=True)
    logo = models.ImageField(blank=True , null = True)

    def _str_(self):
        return self.company_name

class Order(models.Model):
    PENDING = 'Pending'
    PROCESSING = 'Processing'
    SHIPPED = 'Shipped'
    DELIVERED = 'Delivered'
    CANCELED = 'Canceled'

    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (PROCESSING, 'Processing'),
        (SHIPPED, 'Shipped'),
        (DELIVERED, 'Delivered'),
        (CANCELED, 'Canceled'),
    ]

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)  # Ajout de auto_now_add pour définir la date automatiquement
    delivery_date = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    special_file = models.FileField(blank=True, null=True)


    def _str_(self):
        return f'Order {self.id} for {self.customer}'
 
class Product(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    picture = models.ImageField(blank=True , null = True)


    def _str_(self):
        return self.name


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    special_file = models.FileField(blank=True, null=True)

    def _str_(self):
        return f'{self.product.name} (x{self.quantity})'

class Shipment(models.Model):
    IN_TRANSIT = 'In Transit'
    DELIVERED = 'Delivered'
    FAILED = 'Failed'
    RETURNED = 'Returned'

    STATUS_CHOICES = [
        (IN_TRANSIT, 'In Transit'),
        (DELIVERED, 'Delivered'),
        (FAILED, 'Failed'),
        (RETURNED, 'Returned'),
    ]

    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    shipment_date = models.DateField()
    tracking_number = models.CharField(max_length=50)
    carrier = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=IN_TRANSIT)
    special_file = models.FileField(blank=True, null=True)


    def _str_(self):
        return f'Shipment {self.tracking_number} for Order {self.order.id}'

class Task(models.Model):
    PENDING = 'Pending'
    IN_PROGRESS = 'In Progress'
    COMPLETED = 'Completed'

    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (IN_PROGRESS, 'In Progress'),
        (COMPLETED, 'Completed'),
    ]

    LOW = 'Low'
    MEDIUM = 'Medium'
    HIGH = 'High'

    PRIORITY_CHOICES = [
        (LOW, 'Low'),
        (MEDIUM, 'Medium'),
        (HIGH, 'High'),
    ]
    created_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100)
    description = models.TextField()  # Correction de la faute d'orthographe
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    due_date = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING)
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default=MEDIUM)
    created_by = models.ForeignKey(User, related_name='tasks_created', on_delete=models.SET_NULL, null=True)
    updated_by = models.ForeignKey(User, related_name='tasks_updated', on_delete=models.SET_NULL, null=True)

    def _str_(self):
        return self.title

class ContactLog(models.Model):
    PHONE = 'Phone'
    EMAIL = 'Email'
    MEETING = 'Meeting'
    OTHER = 'Other'
    
    METHOD_CHOICES = [
        (PHONE, 'Phone'),
        (EMAIL, 'Email'),
        (MEETING, 'Meeting'),
        (OTHER, 'Other'),
    ]
    
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    contact_date = models.DateTimeField(auto_now_add=True)  # Ajout de auto_now_add pour définir la date automatiquement
    contact_method = models.CharField(max_length=20, choices=METHOD_CHOICES)
    notes = models.TextField()
    created_by = models.ForeignKey(User, related_name='contactlogs_created', on_delete=models.SET_NULL, null=True)
    updated_by = models.ForeignKey(User, related_name='contactlogs_updated', on_delete=models.SET_NULL, null=True)

    def _str_(self):
        return f'Contact with {self.customer} on {self.contact_date}'