from django import forms
from django.utils.translation import ugettext_lazy as _
from .models import Orders,OrderDetails

class OrdersForm(forms.ModelForm):
    class Meta:
        model   = Orders
        fields  =  '__all__'


    def save(self, commit=True):
        order = super(OrdersForm, self).save(commit)
        order.save()
        return order