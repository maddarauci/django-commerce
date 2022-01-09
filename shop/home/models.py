#: home/models.py
from django.db import models
from ckeditor_uploader.fields import RichTextUpLoadingField

# Create your models here.
from django.forms import ModelForm, TextInput, Textarea
frim django.http import request
from django.utils.safestring import mark_safe

class Language(models.Model):
	name = models.CharField(max_length=20)
	code = models.CharField(max_length=5)
	status = models.BooleanField()
	create_at = models.DateTimeField(auto_now_add=True)
	update_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return name 


llist = Language.objects.filter(status=True)
list1 = []
for rs in llist:
	list1.append((rs.code, rs.name))
langList = (list1)

class Setting(models.Model):
	STATUS = (
		('True', 'True'),
		('False', 'False'),
	)

	title = models.CharField(max_length=150)
	keywords = models.CharField(max_length=255)
	description = models.CharField(max_length=255)
	company = models.CharField(max_length=50)
	address = models.CharField(blank=True, max_length=100)
	phone = models.CharField(blank=True, max_length=15)
	#fax = models
	email = models.CharField(blank=True, max_length=50)

	create_at = models.DateTimeField(auto_now_add=True)
	update_at = models.DateTimeField(auto_now=True)

	icon = models.ImageField(blank=True, upload_to='images/')

	def __str__(self):
		return self.title


class SettingLang(models.Model):
	setting = models.ForeignKey(Setting, on_delete=models.CASCADE) # m2m relationship
	lang = models.CharField(max_length=6, choices=langList)
	title = models.CharField(max_length=150)
	keywords = models.CharField(max_length=255)
	aboutus = RichTextUpLoadingField(blank=True)
	contact = RichTextUpLoadingField(blank=True)

	def __str__(self):
		return self.title


class ContactMessage(models.Model):
	STATUS = (
		('New', 'New'),
		('Read', 'Read'),
		('Closed', 'Closed'),
	)

	name = models.CharField(blank=True, max_length=20)
	email = models.CharField(blank=True, max_length=50)
	message = models.TextField(blank=True, max_length=255)
	status = models.CharField(max_length=10, choices=STATUS, default='New')
	ip = models.CharField(blank=True, max_length=100)
	note = models.CharField(blank=True, max_length=100)
	create_at = models.DateTimeField(auto_now_add=True)
	update_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.name

class ContactForm(ModelForm):
	class Meta:
		model = ContactMessage
		fields = ['name', 'email', 'subject', 'message']
		widgets = {
		'name' : TextInput(attrs={'class': 'input', 'placholder': 'Nmae & Surname'}),
		'subject': TextInput(attrs{'class': 'input', 'placholder': 'Subject'}),
		'email': TextInput(attrs{'class': 'input', 'placholder': 'Email address'}),
		'subject': TextInput(attrs{'class': 'input', 'placholder': 'Your Message', 'rows':'5'}),
		}

class FAQ(models.Model):
	STATUS = (
		('True', 'True'),
		('False', 'False'),
	)

	lang = models.CharField(max_length=6, choices=langList, blank=True, null=True)
	ordernumber = models.IntegerField()
	question = models.CharField(max_length=200)
	answer = RichTextUpLoadingField()
	status = models.CharField(max_length=10, choices=STATUS)
	create_at = models.DateTimeField(auto_now_add=True)
	update_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.question
