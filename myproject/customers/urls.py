from django.urls import path,re_path,include
from django.contrib.auth.decorators import login_required, permission_required
from .views import *

urlpatterns = [
    path('products/list',login_required(ProductsViews.as_view(template_name='orders/products/index.html')),name="order_list_products"),
    path('products/checkout', login_required(Checkout.as_view(template_name='orders/products/checkout.html')),name='check_out_product'),
    path('products/add-cart',login_required(add_to_cart),name='add_to_cart'),
    path('products/remove-cart/<int:product_id>',login_required(remove_from_cart), name='remove_from_cart'),
    path('list/',login_required(OrdersView.as_view(template_name='orders/orders.html')),name='ordes_list'),
    path('invoice_print/<int:pk>',login_required(GenerateInvoicePrint.as_view(template_name='invoice/invoice_print.html')),name='invoice_print'),
]