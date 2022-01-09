#--: home/forms.py 
from django import forms 

class SearchForm(forms.Form):
	query = forms.CharField(max_lenght=100)
	catid = forms.IntegerField()

