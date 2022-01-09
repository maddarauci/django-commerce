from django.shortcuts import render
import json 

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm 
from django.contrib.auth.models import User 
from django.db.models import Avg, Count, Q, F
from django.db.models.functions import Concat
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, request
from django.shortcuts import render

# Create your views here.
from django.template.loader import render_to_string 
from django.urls import reverse
from django.utils import translation 


from home.forms import SearchForm 
from home.models import Setting, ContactFomr, ContactMessage, FAQ, SettingLang, Language
from mysite import settings 
from product.models import Category, Product, Images, Comment, Variants, ProductLang, CategoryLang
from user.models import UserProfile 



def index(request):
	if not request.session.has_key('currency'):
		request.session['currency'] = settings.DEFAULT_CURRENCY 

	setting = Setting.objects.get(pk=1)
	products_latest = Product.objects.all().order_by('-id')[:4] # last 4 products
	defaultLang = settings.LANGUAGE_CODE[0:2]
	currentLang = request.LANGUAGE_CODE[0:2]

	if defaultLang != currentLang:
		setting = SettingLang.objects.get(lang=currentLang)
		products_latest = Product.objects.raw(
			'SELECT p.id, p.price, l.title, l.description, l.slug '
			'FROM product_product as p '
			'LEFT JOIN product_productlang as l '
			'ON p.if = l.product_id '
			'WHERE l.lang=%s ORDER BY p.id DESC LIMIT 4', [currentLang])

		product_slider = Product.objects.all().order_by('id')[:4] # first 4 products.

		product_picked = Product.objects.all().order_by('?')[:4] # random selection 4 products

		page = 'home'
		context={'setting': setting,
			'page': page,
			'product_slider': product_slider,
			'products_latest': products_latest,
			'product_picked': product_picked,
			# category:category
			}

		return render(request, 'index.html', context)

