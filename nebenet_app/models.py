from django.db import models
from statistics import mode
from unicodedata import category
from unittest.util import _MAX_LENGTH
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from location_field.models.plain import PlainLocationField
from django.core.validators import MaxValueValidator, MinValueValidator 

# Create your models here.

class User(AbstractUser):
    email = models.EmailField(unique=True)
    image = models.ImageField(upload_to ='img/')
    date = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse('usuarios-detalles', kwargs={'pk': self.pk})
    # to save the data
    def register(self):
        self.save()
  
    @staticmethod
    def get_customer_by_email(email):
        try:
            return User.objects.get(email=email)
        except:
            return False
  
    def isExists(self):
        if User.objects.filter(email=self.email):
            return True
  
        return False

class Brand(models.Model):
    bra_name = models.CharField(max_length=50, blank=False)
    bra_img = models.ImageField(upload_to ='img/')
    bra_contact = models.URLField(max_length=200)

    def __str__(self):
        return self.bra_name

class Category(models.Model):
    name = models.CharField(max_length=50)
  
    @staticmethod
    def get_all_categories():
        return Category.objects.all()
  
    def __str__(self):
        return self.name

class Product(models.Model):
    pro_name = models.CharField(max_length=50, blank=False)
    pro_price_after = models.DecimalField(blank=True, null=True, max_digits=10, decimal_places=2)
    pro_price = models.DecimalField(max_digits=10, decimal_places=2)
    pro_description = models.CharField(max_length=1000, blank=False)
    pro_characteristics =  models.CharField(max_length=1000, blank=False)
    pro_sale = models.BooleanField()
    pro_brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    pro_img = models.ImageField(upload_to ='img/')
    pro_salenumber = models.PositiveIntegerField(blank=True, default=10, validators=[MinValueValidator(1), MaxValueValidator(100)])
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    def __str__(self):
        return self.pro_name
    
    @staticmethod
    def get_products_by_id(ids):
        return Product.objects.filter(id__in=ids)
  
    @staticmethod
    def get_all_products():
        return Product.objects.all()
  
    @staticmethod
    def get_all_products_by_categoryid(category_id):
        if category_id:
            return Product.objects.filter(category=category_id)
        else:
            return Product.get_all_products()

class Company(models.Model):
    co_name = models.CharField(max_length=30, blank=False)
    co_city = models.CharField(max_length=255)
    co_ubi = PlainLocationField(based_fields=['co_city'], zoom=7)
    co_tlf = models.IntegerField()
    co_mail = models.EmailField(unique=True)

    def __str__(self):
        return self.co_name

rates=[(1,1),(2,2),(3,3),(4,4),(5,5)]
class Ratings(models.Model):
    ra_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ra_product = models.ForeignKey(Product, on_delete=models.CASCADE)
    ra_number = models.IntegerField(choices=rates)
    ra_text = models.CharField(max_length=800, blank=False)

    
class Ticket(models.Model):
    ti_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ti_mail = models.EmailField('Contatto email*',blank=False)
    ti_title = models.CharField('Titolo*',max_length=1000, blank=False)
    Problema = models.CharField('Descrivi il tuo problema*',max_length=1000, blank=False)
    ti_img = models.ImageField('Aggiungi uno screenshot (facoltativo)',blank=True)
    ti_personal = models.BooleanField("Trattamento dei dati personali(Obbligatorio)*",blank=False)
    ti_time = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.ti_title

class Coment(models.Model):
    co_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    co_text = models.CharField('Descrivi il tuo problema*',max_length=1000, blank=False)
    co_ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    ti_time = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.co_text

#E-COMERCE
class Order(models.Model):
    product = models.ForeignKey(Product,
                                on_delete=models.CASCADE)
    customer = models.ForeignKey(User,
                                 on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.IntegerField()
    address = models.CharField(max_length=50, default='', blank=True)
    phone = models.CharField(max_length=50, default='', blank=True)
    date = models.DateField(auto_now=True)
    status = models.BooleanField(default=False)
  
    def placeOrder(self):
        self.save()
  
    @staticmethod
    def get_orders_by_customer(customer_id):
        return Order.objects.filter(customer=customer_id).order_by('-date')
