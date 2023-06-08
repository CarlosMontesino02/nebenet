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
from django.contrib.auth import views as auth_views
from nebenet_app import views

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
    #path('accounts/', include('django.contrib.auth.urls')),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='password/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="password/password_reset_confirm.html"), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password/password_reset_complete.html'), name='password_reset_complete'),
    path("password_reset", views.password_reset_request, name="password_reset"),
    path('usuarios/search', search.as_view(), name="search"),

    #Brands
    path('brand/', Brand_List.as_view(), name="brands"),
    path('brand/<int:pk>/', Brand_Detail.as_view(), name='brands_details'),
    path('brand/add/', Brand_Create.as_view(), name="brands_add"),
    path('brand/<int:pk>/update', Brand_Update.as_view(), name='brands_update'),
    path('brand/<int:pk>/delete/', Brand_Delete.as_view(), name='brands_delete'),

    #Products
    path('productadmin/', Product_Admin_List.as_view(template_name='nebenet_app/products_admin.html'), name='products_admin_list'),
    path('productadmin/search', searchproduct.as_view(template_name='nebenet_app/searchproducts.html'), name="searchpro"),
    path('product/<int:pk>/', Product_Detail.as_view(), name='products_details'),
    path('product/add/', Product_Create.as_view(), name="products_add"),
    path('product/<int:pk>/update', Product_Update.as_view(), name='products_update'),
    path('product/<int:pk>/update/sale', Product_Update_Sale.as_view(), name='products_update_sale'),
    path('product/<int:pk>/delete/', Product_Delete.as_view(), name='products_delete'),
    #Tickets
    path('ticket/', Ticket_List.as_view(), name="tickets"),
    path('ticket/<int:pk>/', TicketDetail.as_view(), name='tickets_details'),
    path('ticket/add/', Ticket_Create.as_view(), name="tickets_add"),
    path('ticket/<int:pk>/update', Ticket_Update.as_view(), name='tickets_update'),
    path('ticket/<int:pk>/delete/', Ticket_Delete.as_view(), name='tickets_delete'),
    path('ticketsadmin/', Product_ticekt_List.as_view(template_name='nebenet_app/ticket_admin.html'), name='tickets-admin'),
    path('ticketsadmins/search', searchticket.as_view(template_name='nebenet_app/searchtickets.html'), name="searchti"),

    #Coments
    path('coment/<int:pk>/delete/', Coment_Delete.as_view(), name='coments_delete'),
    
    #Company
    path('company/<int:pk>/', Company_Detail.as_view(), name='company_details'),
    path('company/<int:pk>/update', Company_Update.as_view(), name='company_update'),
    #E-comerce
    path('vitrina/', vitrina.as_view(), name='vitrina'),
    path('vitrina/search', searchvitrina.as_view(template_name='nebenet_app/searchvitrina.html'), name="searchvi"),
    path('store/', store , name='store'),
    path('cart', Cart.as_view() , name='cart'),
    path('check-out', CheckOut.as_view() , name='checkout'),
    path('orders', OrderView.as_view(), name='orders'),
    path('listorders/', Order_List.as_view(), name='orders_list'),
    path('listorders/<int:pk>/update', Order_Update.as_view(), name='orders_update'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
