from django.contrib import admin
from django.contrib.auth.admin import User
from . import models
from .models import *

admin.site.register(User)
admin.site.register(Product)
admin.site.register(Ratings)
admin.site.register(Cart)
admin.site.register(Company)
admin.site.register(Brand)
admin.site.register(Ticket)
admin.site.register(Coment)
# Register your models here.
