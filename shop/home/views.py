#--: home/views.py
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


def selectLanguage(request):
	if request.method == "POST": # check post 
		cur_language = translation.get_language()
		lasturl = request.META.get('HTTP_EFERER')
		lang = request.POST['Language']
		translation.activate(lang)
		request.session[translation.LANGUAGE_SESSION_KEY] = lang 
		#return httpResponse(lang)
		return HttpResponseRedirect("/"+lang)

def aboutus(request):
	# category = categoryTree(0, '', currentlang)
	defaultLang = setting.LANGUAGE_CODE[0:2]
	currentLang = request.LANGUAGE_CODE[0:2]
	setting = Setting.objects.get(pk=1)
	if defaultLang != currentLang:
		setting = SettingLang.objects.get(lang=currentLang)

	context = {'setting':setting}
	return render(request, 'about.html', context)

def contactus(request):
	currentLang = request.LANGUAGE_CODE[0:2]
	# category = categoryTree(0, '', currentLang)
	if request.method == 'POST':
		form = ContactForm(request.POST)
		if form.is_valid():
			data = ContactMessage() # create reltion with model 
			data.name = form.cleaned_data['name'] # get form input data 
			data.email = form.cleaned_data['email']
			data.subject = form.cleaned_data['subject']
			data.message = form.cleaned_data['message']
			data.ip = request.META.get('REMOTE_ADDR')
			data.save() # save the data to table 
			messages.success(request, "your message has benn sent, thank you for your message")
			return HttpResponseRedirect('/contact')
	defaultLang = settings.LANGUAGE_CODE[0:2]
	currentLang = request.LANGUAGE_CODE[0:2]
	setting = Setting.objects.get(pk=1)
	if defaultLang != currentLang:
		setting = SettingLang.objects.get(lang=currentLang)

	form = ContactForm
	context = {'setting':setting, 'form':form }
	return render(request, 'contactus.html', context)

def category_product(request, id, slug):
	defaultLang = setting.LANGUAGE_CODE[0:2]
	currentLang = request.LANGUAGE_CODE[0:2]
	catdata = Category.objects.get(pk=id)
	products = Product.objects.filter(category_id=id) # default language.
	if defaultLang != currentLang:
		try:
			products = Product.objects.raw(
				'SELECT p.id, p.price, p.amount, p.image, p.variant, l.title, l.keyword, l.description, l.slug, l.detail '
				'FROM product_product as p '
				'LEFT JOIN product_productlang as l '
				'ON p.id = l.product_id '
				'WHERE p.category_id=%s and l.lang=%s', [id, currentLang]
		)
		except:
			pass 
		catdata = CategoryLang.objects.get(category_id=id, lang=currentLang)
	context= {'products': products,
		# category: category 
		'catdata':catdata
	}
	return rende(request, 'category_products.html', context)

def search(request):
	if request.method == "POST":
		form = SearchForm(request.POST)
		if form.is_valid():
			query = form.cleaned_data['query'] 
			catid = form.cleaned_data['id']
			if catid ==0:
				products=Products.objects.filter(title_icontains=query)
			else:
				products = Product.objects.filter(title_icontains=query, category_id=catid)
			category = Category.objects.all()
			context = {'products': products, 'query': query, 'category': category }
			return render(request, 'search_products.html', context)

	return HttpResponseRedirect('/')


def search_auto(request):
	if request.is_ajax():
		q = request.GET.get('term', '')
		products = Product.objects.filter(title_icontains)

		results = []
		for rs in products:
			product_json = {}
			product_json = rs.title + ' > ' + rs.category.title
			result.append(products_json)
		data = json.dumps(results)
	else: 
		data = 'fail'
		mimetype = 'application/json'
	return HttpResponse(data, mimetype)

def product_detail(request, id, slug):
	query = request.GET.get('q')
	# multiple languages 
	defaultLang = setting.LANGUAGE_CODE[0:2]
	category = Category.objects.all()

	products = Product.objects.get(pk=id)

	if defaultLang != currentLang:
		try:
			prolang = Product.objects.raw('SELECT p.id, p.price, amount.image, p.variant, l.title, l.keyword, l.description, l.slug, l.detail '
				'FROM product_product as p '
				'INNER JOIN product_productlang as l '
				'ON p.id = l.product_id '
				'WHERE p.id=%s and l.lang=%s', [id, currentLang])
			product=prolang[0]
		except:
			pass 
	images = Images.objects.filter(product_id=id)
	comments = Comment.objects.filter(product_id=id, status='True')
	context = {'product': product, 'category': category,
			'images': images, 'comments': comments,
			}
	if product.Variants != 'None':
		if request.method == 'POST':
			variant_id = request.POST.get('Variantid')
			variant = Variants.objects.get(id=variant_id) # select object by clicking color radio
			#variant = Variants.objects.filter(product_id=id, size_id=variant.size_id )
			colors = Variants.objects.filter(product_id=id, size_id=variant.size_id )
			sizes = Variants.objects.raw('SELECT * FROM product_variants WHERE product_id=%s GROUP BY size size_id', [id])
			query += variant.title+'Size:' +str(variant.size) + 'Color:'+str(variant.color)
		else:
			variants = Variants.objects.filter(product_id=id)
			colors = Variants.objects.filter(product_id=id, size_id=variants[0].size_id )
			sizes = Variants.objects.raw('SELECT * FROM product_variants WHERE product_id=%s GROUP By size_id',[id])
			variant = Variants.objects.get(id=variants[0].id)
		context.update({'sizes':sizes, 'colors':color,
				'variant': variant, 'query': context
			})
	return render(request, 'product_detail.html', context)

def ajaxcolor(request):
	data = {}
	if request.POST.get('action') == "post":
		size_id = request.POST.get('size')
		productid = request.POST.get('productid')
		colors = Variants.objects.filter(product_id=productid, size_id=size_id)
		context = {
			'size_id': size_id,
			'productid': productid,
			'colors': colors,
		}
		data = {'rendered_table': render_to_string('color_list.html', context=context)}
		return JsonResponse(data)
	return JsonResponse(data)

def faq(request):
	defaultLang = settings.LANGUAGE_CODE[0:2]
	currentLang = request.LANGUAGE_CODE[0:2]

	if defaultLang == currentLang:
		faq = FAQ.objects.filter(status='True', lang=defaultLang).oder_by('ordernumber')
	else:
		faq = FAQ.objects.filter(status='True', lang=currentLang).oder_by('ordernumber')

	context = {
		'faq': faq,
	}
	return render(request, 'faq.html', context)

def selectcurrency(request):
	lasturl = request.META.get('HTTP_EFERER')
	if request.method =='POST':
		request.session['currency'] = request.POST['currency']
	return HttpResponseRedirect(lasturl)

@login_required(login_url='login')
def savelangcur(request):
	lasturl = request.META.get('HTTP_EFERER')
	current_user = request.user
	Language=Language.objects.get(code=request.LANGUAGE_CODE[0:2])
	# save the user profile to db 
	data = UserProfile.objects.get(user_id=current_user.id)
	data.Language_id =Language.id 
	data.currency_id = request.session['currency']
	data.save()
	return HttpResponseRedirect(lasturl)