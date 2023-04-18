"""nebenet URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from nebenet_app.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    #index
    path('', index, name='index'),
    #sign log etc
    path('registro/', FormUser.as_view(), name='user-add'),
    path("accounts/", include("django.contrib.auth.urls")),

    #User
    path('usuarios/', User_List.as_view(), name="usuarios-lista"),
    path('usuarios/<int:pk>', User_Detail.as_view(), name="usuarios-detalles"),
    path('usuarios/<int:pk>/update', Update_User.as_view(), name="usuarios-update"),

    #Brands
    path('brand/', Brand_List.as_view(), name="brands"),
    path('brand/<int:pk>/', Brand_Detail.as_view(), name='brands_details'),
    path('brand/add/', Brand_Create.as_view(), name="brands_add"),
    path('brand/<int:pk>/update', Brand_Update.as_view(), name='brands_update'),
    path('brand/<int:pk>/delete/', Brand_Delete.as_view(), name='brands_delete'),

    #Products
    path('product/', Product_List.as_view(), name="products"),
    path('product/<int:pk>/', Product_Detail.as_view(), name='products_details'),
    path('product/add/', Product_Create.as_view(), name="products_add"),
    path('product/<int:pk>/update', Product_Update.as_view(), name='products_update'),
    path('product/<int:pk>/delete/', Product_Delete.as_view(), name='products_delete'),
#Mirar que pasa con las url xd
    #Tickets
    path('ticket/', Ticket_List.as_view(), name="tickets"),
    path('ticket/<int:pk>/', TicketDetail.as_view(), name='tickets_details'),
    path('ticket/add/', Ticket_Create.as_view(), name="tickets_add"),
    path('ticket/<int:pk>/update', Ticket_Update.as_view(), name='tickets_update'),
    path('ticket/<int:pk>/delete/', Ticket_Delete.as_view(), name='tickets_delete'),
    
    #Coments
    path('coment/', Coment_List.as_view(), name="coments"),
    path('coment/<int:pk>/', Coment_Detail.as_view(), name='coments_details'),
    #path('coment/add/', ComentarioFormView.as_view(), name="coments_add"),
    path('coment/<int:pk>/delete/', Coment_Delete.as_view(), name='coments_delete'),
    
    #Company
    path('company/<int:pk>/', Company_Detail.as_view(), name='company_details'),
    path('company/<int:pk>/update', Company_Update.as_view(), name='company_update'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
