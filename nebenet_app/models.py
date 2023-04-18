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
# Create your models here.

class User(AbstractUser):
    email = models.EmailField(unique=True)
    image = models.ImageField(upload_to ='img/')
    date = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse('usuarios-detalles', kwargs={'pk': self.pk})

class Brand(models.Model):
    bra_name = models.CharField(max_length=50, blank=False)
    bra_img = models.ImageField(upload_to ='img/')
    bra_contact = models.URLField(max_length=200)

    def __str__(self):
        return self.bra_name

class Product(models.Model):
    pro_name = models.CharField(max_length=50, blank=False)
    pro_price = models.DecimalField(max_digits=10, decimal_places=2)
    pro_description = models.CharField(max_length=1000, blank=False)
    pro_characteristics =  models.CharField(max_length=1000, blank=False)
    pro_sale = models.BooleanField()
    pro_brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    pro_img = models.ImageField(upload_to ='img/')
    pro_salenumber = models.DecimalField(max_digits=2, decimal_places=0)
    cpu='cpu'
    gpu='gpu'
    none='N/A'
    schedamadre='Scheda madre'
    hdd='hdd'
    ssd='ssd'
    m2='m.2'
    caso='caso'
    ram='ram'
    ae='Alimentazione elettrica'
    vent='ventilazione'
    per='periferica'
    laptop='laptop'
    pc='computer'
    COMPONENT = [
        (cpu,'CPU'),
        (gpu,'GPU'),
        (schedamadre,'Scheda madre'),
        (hdd,'HDD'),
        (ssd,'SSD'),
        (m2,'M.2'),
        (ram,'RAM'),
        (caso,'Caso'),
        (ae,'Alimentazione elettrica'),
        (vent,'Ventilazione'),
        (per,'Periferica'),
        (pc,'Computer'),
        (laptop,'computer portatile'),
        (none,'none'),
    ]
    pro_type = models.CharField(
    'Component*',
    max_length=23,
    choices=COMPONENT,
    default='none',
    null=True
    )
    def __str__(self):
        return self.pro_name

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

class Cart(models.Model):
    sc_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    sc_pro = models.ManyToManyField(Product)
    sc_price = models.DecimalField(max_digits=11, decimal_places=2)
    sc_quantity = models.IntegerField()
    def __str__(self):
        return self.sc_user
    
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
