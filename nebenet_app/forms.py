from django import forms
from nebenet_app.models import *
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.http import HttpResponseForbidden
from django.urls import reverse
from django.views.generic import FormView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic import DetailView
from django.utils.translation import gettext_lazy as _
from django.forms import inlineformset_factory

class UserForm(UserCreationForm):
	class Meta:
		model = User
		fields = ('username','password1','password2','email')
		error_messages = {
    'password_mismatch': _("The two password fields didn't match."),
	}
	username = forms.CharField(
	    label=_("Username"),
	    strip=False,
	    widget=forms.PasswordInput,
	    # help_text=password_validation.password_validators_help_text_html(),
	)
	password1 = forms.CharField(
	    label=_("Password"),
	    strip=False,
	    widget=forms.PasswordInput,
	    # help_text=password_validation.password_validators_help_text_html(),
	)
	password2 = forms.CharField(
	    label=_("Password confirmation"),
	    widget=forms.PasswordInput,
	    strip=False,
	    help_text=_(""),
	)


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
	
class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['status']
