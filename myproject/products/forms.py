from django import forms
from django.utils.translation import ugettext_lazy as _
from .models import Category,Products

class CategoryForm(forms.ModelForm):
    class Meta:
        model   = Category
        fields  =  '__all__'
    name = forms.CharField(required=True,help_text="Required. name for categories")
    def save(self, commit=True):
        categories = super(CategoryForm, self).save(commit)
        categories.save()
        return categories

class ProductsForm(forms.ModelForm):
    class Meta:
        model   = Products
        fields  = ('code','name','photo','description','categories','price','stock')
    
    photo       = forms.ImageField(required=False)
    name        = forms.CharField(required=True)
    code        = forms.CharField(required=True)
    description = forms.CharField(required=True)
    categories  = forms.ModelChoiceField(queryset=Category.objects.all(),required=True)
    price       = forms.CharField(required=True)
    stock       = forms.CharField(required=True)
