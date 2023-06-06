from django.shortcuts import render
from nebenet_app.models import *
from django.views.generic import DetailView
from django.views.generic.edit import FormView
from django.views.generic import ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.contrib.auth import login, authenticate
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import UserPassesTestMixin
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.core.exceptions import PermissionDenied
from .forms import *
from django.http import HttpResponseForbidden
from django.views.generic.detail import SingleObjectMixin
from django.views import View
from django.contrib.auth.forms import PasswordResetForm
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.core.exceptions import ValidationError
from django.http import JsonResponse

def index (request):
    return render(request, 'nebenet_app/index.html')

#User register
class FormUser(CreateView):
    model = User
    form_class = UserForm
    template_name = "./nebenet_app/user_form.html"
    
class Update_User(UserPassesTestMixin, LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserEdit
    template_name = "./nebenet_app/user_update_form.html"
    def test_func(self):
        try:
            return User.objects.get(pk=self.request.user.pk)==User.objects.get(pk=self.kwargs.get("pk"))
        except:
            return False

#User
class search(UserPassesTestMixin,LoginRequiredMixin,ListView):
    model = User
    template_name="photanic_app/search.html"
    def get_queryset(self):
        query = self.request.GET.get("q")
        object_list=User.objects.filter(Q(username__icontains=query))
        return object_list
    def test_func(self):
        user = self.request.user
        return self.request.user.is_staff or user.groups.filter(name='dependiente').exists()

class User_List(UserPassesTestMixin,LoginRequiredMixin, ListView):
    model = User
    template_name = "./nebenet_app/user_list.html"
    def test_func(self):
        user = self.request.user
        return self.request.user.is_staff or user.groups.filter(name='dependiente').exists()

class User_Detail(UserPassesTestMixin,LoginRequiredMixin, DetailView):
    model = User
    def get_context_data(self, **kwargs):
        queryset = User.objects.all()
        context_object_name = 'user'
        context = super().get_context_data(**kwargs)
        context['tickets']=Ticket.objects.filter(ti_user=self.kwargs.get("pk"))
        return context
    def test_func(self):
        if self.request.user.is_superuser:
            return True
        else:
            try:
                return User.objects.get(pk=self.request.user.pk)==User.objects.get(pk=self.kwargs.get("pk"))
            except:
                return False

    
# Brand
class Brand_List(ListView):
    model = Brand

class Brand_Detail(UserPassesTestMixin,DetailView):
    model = Brand
    def test_func(self):
        user = self.request.user
        return self.request.user.is_staff or user.groups.filter(name='dependiente').exists()

class Brand_Create(UserPassesTestMixin,LoginRequiredMixin, CreateView):
    model = Brand
    fields = ['bra_name','bra_img','bra_contact']
    success_url = reverse_lazy('brands')
    def test_func(self):
        user = self.request.user
        return self.request.user.is_staff or user.groups.filter(name='dependiente').exists()

class Brand_Update(UserPassesTestMixin, LoginRequiredMixin, UpdateView):
    model = Brand
    fields = ['bra_name','bra_img','bra_contact']
    success_url = reverse_lazy('brands')
    def test_func(self):
        user = self.request.user
        return self.request.user.is_staff or user.groups.filter(name='dependiente').exists()

class Brand_Delete(UserPassesTestMixin, LoginRequiredMixin, DeleteView):
    model = Brand
    success_url='/brand/'
    def test_func(self):
        user = self.request.user
        return self.request.user.is_staff or user.groups.filter(name='dependiente').exists()
    
# Products
class searchproduct(UserPassesTestMixin,LoginRequiredMixin,ListView):
    model = Product
    template_name="photanic_app/searchproducts.html"
    def get_queryset(self):
        query = self.request.GET.get("q")
        object_list=Product.objects.filter(Q(pro_name__icontains=query))
        return object_list
    def test_func(self):
        user = self.request.user
        return self.request.user.is_staff or user.groups.filter(name='dependiente').exists()
    
class Product_Detail(DetailView):
    model = Product

class Product_Admin_List(UserPassesTestMixin,LoginRequiredMixin,ListView):
    model = Product
    def test_func(self):
        user = self.request.user
        return self.request.user.is_staff or user.groups.filter(name='dependiente').exists()


class Product_Create(UserPassesTestMixin,LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('products_admin_list')
    def test_func(self):
        user = self.request.user
        return self.request.user.is_staff or user.groups.filter(name='dependiente').exists()

class Product_Update(UserPassesTestMixin, LoginRequiredMixin, UpdateView):
    model = Product
    fields = ['pro_name','pro_price','pro_description','pro_characteristics','pro_brand','pro_img']
    success_url = reverse_lazy('products_admin_list')
    def test_func(self):
        user = self.request.user
        return self.request.user.is_staff or user.groups.filter(name='dependiente').exists()

class Product_Update_Sale(UserPassesTestMixin, LoginRequiredMixin, UpdateView):
    model = Product
    form_class = SaleForm
    success_url = reverse_lazy('products_admin_list')

    def form_valid(self,form):
        sale = form.save(commit=False)
        url=self.request.get_full_path()
        urlcad=url.split("/")
        obj=Product.objects.get(pk=int(urlcad[2]))
        if sale.pro_sale == True:
            obj.pro_sale = sale.pro_sale
            obj.pro_salenumber = sale.pro_salenumber
            a = obj.pro_price
            b = sale.pro_salenumber
            obj.pro_price_after = a-((a/100)*b)
            obj.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            obj.pro_sale = sale.pro_sale
            obj.pro_salenumber = sale.pro_salenumber
            obj.pro_price_after = obj.pro_price
            obj.save()
            return HttpResponseRedirect(self.get_success_url())

    def test_func(self):
        user = self.request.user
        return self.request.user.is_staff or user.groups.filter(name='dependiente').exists()


class Product_Delete(UserPassesTestMixin, LoginRequiredMixin, DeleteView):
    model = Product
    success_url='/product/'
    def test_func(self):
        user = self.request.user
        return self.request.user.is_staff or user.groups.filter(name='dependiente').exists()

#Company

class Company_Detail(DetailView):
    model = Company

class Company_Update(UserPassesTestMixin, LoginRequiredMixin, UpdateView):
    model = Company
    fields = ['co_name','co_city','co_ubi','co_tlf','co_mail']
    success_url = reverse_lazy('index')
    def test_func(self):
        user = self.request.user
        return self.request.user.is_staff or user.groups.filter(name='dependiente').exists()
#Tickets

class searchticket(UserPassesTestMixin, LoginRequiredMixin,ListView):
    model = Ticket
    template_name="photanic_app/searchtickets.html"
    def get_queryset(self):
        query = self.request.GET.get("q")
        object_list=Ticket.objects.filter(Q(ti_title__icontains=query))
        return object_list
    def test_func(self):
        user = self.request.user
        return self.request.user.is_staff or user.groups.filter(name='dependiente').exists()
    
class Ticket_List(ListView):
    model = Ticket
    def get_queryset(self):
        user = self.request.user
        if self.request.user.is_staff or user.groups.filter(name='dependiente').exists(): 
            resultado=Ticket.objects.all()
        else:
            resultado=Ticket.objects.filter(ti_user=self.request.user)
        return resultado
###################################################################################SOlucionar problemas de seguirdad
class TicketDetail(UserPassesTestMixin, LoginRequiredMixin, DetailView):
    template_name = 'nebenet_app/ticket_detail.html'
    model = Ticket

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        connected_coments = Coment.objects.filter(co_ticket=self.get_object())
        number_of_coments = connected_coments.count()
        data['coments'] = connected_coments
        data['no_of_coments'] = number_of_coments
        data['coment_form'] = ComentForm()
        return data

    def post(self, request, *args, **kwargs):
        if self.request.method == 'POST':
            coment_form = ComentForm(self.request.POST)
            if coment_form.is_valid():
                co_text = coment_form.cleaned_data['co_text']
                new_coment = Coment(co_text=co_text, co_user=self.request.user, co_ticket=self.get_object())
                new_coment.save()
        return self.get_comments()

    def get_comments(self):
        connected_coments = Coment.objects.filter(co_ticket=self.get_object())
        comments_data = []
        for comment in connected_coments:
            comment_data = {
                'co_user': comment.co_user.username,
                'co_text': comment.co_text,
                'ti_time': comment.ti_time.strftime('%Y-%m-%d %H:%M:%S')
            }
            comments_data.append(comment_data)
        return JsonResponse(comments_data, safe=False)

    def test_func(self):
        if self.request.user.is_superuser:
            return True
        else:
            try:
                return User.objects.get(pk=self.request.user.pk) == Ticket.objects.get(
                    pk=self.kwargs.get("pk")).ti_user
            except:
                return False
#####################################################################
class Ticket_Create(LoginRequiredMixin, CreateView):
    model = Ticket
    form_class = TicketForm

    def form_valid(self, form):
        obj = form.save(commit=False)
        if obj.ti_personal == True:
            obj.ti_user = self.request.user
            obj.ti_mail = self.request.user.email
            obj.save()
            return HttpResponseRedirect(reverse_lazy('tickets'))
        else:
            raise ValidationError("Acepta")


class Ticket_Update(UserPassesTestMixin, LoginRequiredMixin, UpdateView):
    model = Ticket
    fields = ['ti_title','Problema','ti_img']
    success_url = reverse_lazy('tickets')
    def test_func(self):
        try:
            return User.objects.get(pk=self.request.user.pk)==Ticket.objects.get(pk=self.kwargs.get("pk")).ti_user
        except:
            return False

class Ticket_Delete(UserPassesTestMixin, LoginRequiredMixin, DeleteView):
    model = Ticket
    success_url='/ticket/'
    def test_func(self):
        user = self.request.user
        return self.request.user.is_staff or user.groups.filter(name='dependiente').exists()
    
#Company
class Company_Detail(DetailView):
    model = Company

class Company_Update(UserPassesTestMixin, LoginRequiredMixin, UpdateView):
    model = Company
    fields = ['co_name','co_city','co_ubi','co_tlf','co_mail']
    success_url = reverse_lazy('index')
    def test_func(self):
        user = self.request.user
        return self.request.user.is_staff or user.groups.filter(name='dependiente').exists()

#Coment
class Coment_List(UserPassesTestMixin, LoginRequiredMixin,ListView):
    model = Coment
    def test_func(self):
        user = self.request.user
        return self.request.user.is_staff or user.groups.filter(name='dependiente').exists()

class Coment_Detail(UserPassesTestMixin, LoginRequiredMixin,DetailView):
    model = Coment


class Coment_Delete(UserPassesTestMixin, LoginRequiredMixin, DeleteView):
    model = Coment
    success_url='/tickets/'
    def test_func(self):
        user = self.request.user
        return self.request.user.is_staff or user.groups.filter(name='dependiente').exists()
    
#Password reset
def password_reset_request(request):
	if request.method == "POST":
		password_reset_form = PasswordResetForm(request.POST)
		if password_reset_form.is_valid():
			data = password_reset_form.cleaned_data['email']
			associated_users = User.objects.filter(Q(email=data))
			if associated_users.exists():
				for user in associated_users:
					subject = "Password Reset Requested"
					email_template_name = "password/password_reset_email.txt"
					c = {
					"email":user.email,
					'domain':'127.0.0.1:8000',
					'site_name': 'Nebenet',
					"uid": urlsafe_base64_encode(force_bytes(user.pk)),
					"user": user,
					'token': default_token_generator.make_token(user),
					'protocol': 'http',
					}
					email = render_to_string(email_template_name, c)
					try:
						send_mail(subject, email, 'admin@example.com' , [user.email], fail_silently=False)
					except BadHeaderError:
						return HttpResponse('Invalid header found.')
					return redirect ("/password_reset/done/")
	password_reset_form = PasswordResetForm()
	return render(request=request, template_name="password/password_reset.html", context={"password_reset_form":password_reset_form})

#E-comerce

class vitrina(View):
    def post(self, request):
        product_id = request.POST.get('product')
        remove = request.POST.get('remove')
        cart = request.session.get('cart', {})
        
        quantity = cart.get(product_id, 0)
        
        if remove:
            if quantity <= 1:
                cart.pop(product_id, None)
            else:
                cart[product_id] = quantity - 1
        else:
            cart[product_id] = quantity + 1
        
        request.session['cart'] = cart
        
        data = {
            'cart_quantity': cart.get(product_id, 0)
        }
        
        return JsonResponse(data)

    def get(self, request):
        cart = request.session.get('cart', {})
        categories = Category.get_all_categories()
        category_id = request.GET.get('category')
        
        if category_id:
            products = Product.get_all_products_by_categoryid(category_id)
        else:
            products = Product.get_all_products()
        
        data = {
            'products': products,
            'categories': categories,
            'cart': cart,
            'cart_quantities': list(cart.values())
        }
        
        return render(request, 'vitrina.html', data)

class searchvitrina(ListView):
    model = Product
    template_name="photanic_app/searchvitrina.html"
    def get_queryset(self):
        query = self.request.GET.get("q")
        object_list=Product.objects.filter(Q(pro_name__icontains=query))
        return object_list

    def post(self, request):
        product_id = request.POST.get('product')
        remove = request.POST.get('remove')
        cart = request.session.get('cart', {})
        
        quantity = cart.get(product_id, 0)
        
        if remove:
            if quantity <= 1:
                cart.pop(product_id, None)
            else:
                cart[product_id] = quantity - 1
        else:
            cart[product_id] = quantity + 1
        
        request.session['cart'] = cart
        
        data = {
            'cart_quantity': cart.get(product_id, 0)
        }
        
        return JsonResponse(data)

    def get(self, request):
        query = self.request.GET.get("q")
        cart = request.session.get('cart', {})
        categories = Category.get_all_categories()
        category_id = request.GET.get('category')
        
        if category_id:
            products = Product.get_all_products_by_categoryid(category_id)
        else:
            products = Product.objects.filter(Q(pro_name__icontains=query))
        
        data = {    
            'products': products,
            'categories': categories,
            'cart': cart,
            'cart_quantities': list(cart.values())
        }
        
        return render(request, 'vitrina.html', data)

def store(request):
    cart = request.session.get('cart')
    if not cart:
        cart = {}
        request.session['cart'] = cart

    products = None
    categories = Category.get_all_categories()
    categoryID = request.GET.get('category')
    if categoryID:
        products = Product.get_all_products_by_categoryid(categoryID)
    else:
        products = Product.get_all_products()

    data = {}
    data['products'] = products
    data['categories'] = categories
    data['cart'] = cart  # Agregar el carrito al diccionario de datos
    return render(request, 'vitrina.html', data)


class Cart(LoginRequiredMixin,View):
    def get(self , request):
        ids = list(request.session.get('cart').keys())
        products = Product.get_products_by_id(ids)
        return render(request , 'cart.html' , {'products' : products})
    
class OrderView(LoginRequiredMixin,View):

    def get(self , request ):
        customer = request.user.id
        orders = Order.get_orders_by_customer(customer)
        return render(request , 'orders.html'  , {'orders' : orders})

    
class CheckOut(LoginRequiredMixin, View):
    def post(self, request):
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        user = request.user.id
        cart = request.session.get('cart')
        products = Product.get_products_by_id(list(cart.keys()))
        for product in products:
            if product.pro_sale:
                order = Order(customer=User(id=user),
                              product=product,
                              price=product.pro_price_after,
                              address=address,
                              phone=phone,
                              quantity=cart.get(str(product.id)))
            else:
                order = Order(customer=User(id=user),
                              product=product,
                              price=product.pro_price,
                              address=address,
                              phone=phone,
                              quantity=cart.get(str(product.id)))
            order.save()
        request.session['cart'] = {}
        return redirect('orders')

class Order_List(UserPassesTestMixin,ListView):
    model = Order
    def test_func(self):
        user = self.request.user
        return self.request.user.is_staff or user.groups.filter(name='dependiente').exists()

class Order_Update(UserPassesTestMixin, LoginRequiredMixin, UpdateView):
    model = Order
    fields = ['status']
    success_url = reverse_lazy('orders_list')
    def test_func(self):
        user = self.request.user
        return self.request.user.is_staff or user.groups.filter(name='dependiente').exists()