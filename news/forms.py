from django.forms import ModelForm
from .models import *
from django import forms


class StylishForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})


class AddNewsForm(StylishForm):
	class Meta:
		model = latest_news
		exclude =['slug','delete_status','date']
		
	
class CategoryForm(StylishForm):
	class Meta:
		model = Category
		exclude =['delete_status']
		
	
class MainCategoryForm(StylishForm):
	class Meta:
		model = Main_category
		exclude =['delete_status']
		
	
class VideosForm(StylishForm):
	class Meta:
		model = Videos
		fields = '__all__'
		
