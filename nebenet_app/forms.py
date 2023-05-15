from django import forms
from nebenet_app.models import *
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.http import HttpResponseForbidden
from django.urls import reverse
from django.views.generic import FormView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic import DetailView
from django.utils.translation import gettext_lazy as _

class UserForm(UserCreationForm):
	class Meta:
		model = User
		fields = ('username','password1','password2','email')
		help_texts = {k:"" for k in fields}
	
class UserEdit(UserChangeForm):
	class Meta:
		model = User
		fields = ('username','image','email')


class ProductForm(forms.ModelForm):
	error_css_class = 'error-field'
	required_css_class = 'required-field'
	pro_description = forms.CharField(widget=forms.Textarea(attrs={"rows": 3}))
	pro_characteristics = forms.CharField(widget=forms.Textarea(attrs={"rows": 3}))
	class Meta:
		model =  Product
		fields = ('pro_name','pro_price','category','pro_description','pro_characteristics','pro_brand','pro_img','pro_sale','pro_salenumber')

class SaleForm(forms.ModelForm):
	error_css_class = 'error-field'
	required_css_class = 'required-field'
	class Meta:
		model =  Product
		fields = ('pro_sale','pro_salenumber')

class TicketForm(forms.ModelForm):
	error_css_class = 'error-field'
	required_css_class = 'required-field'
	Problema = forms.CharField(widget=forms.Textarea(attrs={"rows": 3}))
	class Meta:
		model =  Ticket
		fields = ('ti_title','Problema','ti_img','ti_personal')


class ComentForm(forms.ModelForm):
    class Meta:
        model = Coment
        fields = ['co_text']