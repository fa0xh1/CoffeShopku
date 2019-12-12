from django import template
from django.contrib.humanize.templatetags.humanize import intcomma

register = template.Library()

def currency(dollars):
    if(dollars):
        dollars = round(float(dollars), 2)
        return "IDR %s%s" % (intcomma(int(dollars)), ("K"))
def subamount(qty,price):
    return qty * price
def changepaid(total,paid):
    return paid - total
register.filter('currency', currency)
register.filter('subamount', subamount)
register.filter('changepaid', changepaid)