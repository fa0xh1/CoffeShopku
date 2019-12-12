
from products.models import Products,Category
from .models import Customers
from django.views.generic import CreateView, DeleteView,UpdateView,ListView,FormView,View,DetailView
from .forms import *
from django.contrib.auth import get_user_model
from django.db.models import Q
from cart.cart import Cart
from cart.models import Item
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from django.urls import reverse,reverse_lazy
from django.shortcuts import render_to_response,redirect
from django.db.models import F
from django.contrib import messages
from django.db.models import Sum,Count
from django.views.generic import View
import datetime
from django.core.files.storage import FileSystemStorage
from django.template.loader import render_to_string


def add_to_cart(request):
    quantity = int(request.POST.getlist('quantity')[0])
    if(quantity !=0):
        product_id = request.POST['product_id']
        product = Products.objects.get(id=product_id)
        cart = Cart(request)
        cart.add(product, product.price, quantity)
        return HttpResponseRedirect(reverse('order_list_products'))
    else:
        messages.error(request,"Order fail Qty can't null")
        return HttpResponseRedirect(reverse('order_list_products'))

def remove_from_cart(request, product_id):
    product = Products.objects.get(id=product_id)
    cart = Cart(request)
    cart.remove(product)
    return HttpResponseRedirect(reverse('order_list_products'))

def generateInvoice():
    order = Orders.objects.only('created_at').order_by('-created_at')
    if order.count() > 0:
        order   = order.first()
        explode = order.invoice.split('-')
        count   = str(int(explode[1]) + 1)
        return 'INV-'+count
    return 'INV-1'
def get_cart(request):
    return render(request, 'orders/products/cart.html', {'cart': Cart(request)})
    
class ProductsViews(FormView):
    form_class = OrdersForm
    success_url = 'order_list_products'
    def get(self, request, *args, **kwargs):
        """Handle GET requests: instantiate a blank version of the form."""
        if request.method == 'GET' and 'search' in request.GET:
            if request.GET['search'] != '':
                kwargs['products']          = Products.objects.filter(Q(name=request.GET['search']) | Q(code=request.GET['search']))
            else:
                kwargs['products']          = Products.objects.all()
        elif request.method == 'GET' and 'categories' in request.GET:
            if request.GET['categories'] != '':
                kwargs['products']          = Products.objects.filter(Q(categories=request.GET['categories']))
            else:
                kwargs['products']          = Products.objects.all()
        else:
                kwargs['products']          = Products.objects.all()
        kwargs['cart']                      = Cart(request)
        return self.render_to_response(self.get_context_data(**kwargs))
    def get_context_data(self, **kwargs):
        kwargs['heading_title']     = "Order Transaction"
        kwargs['list_categories']   = Category.objects.all()
        kwargs['breadcrumb']        = {'content':'Order Product','class':'active'}
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        return context
    
    def get_success_url(self):
        """Return the URL to redirect to after processing a valid form."""
        if not self.success_url:
            raise ImproperlyConfigured("No URL to redirect to. Provide a success_url.")
        return reverse_lazy(self.success_url)  # success_url may be lazy

class Checkout(CreateView):
    model = Orders
    form_class = OrdersForm
    success_url = 'ordes_list'
    def get(self, request, *args, **kwargs):
        """Handle GET requests: instantiate a blank version of the form."""
        self.object = None
        User = get_user_model()
        kwargs['cart']                   = Cart(request)
        kwargs['customers']              = Customers.objects.all()
        kwargs['barista']                = User.objects.all().filter(groups__name='Barista')
        return self.render_to_response(self.get_context_data(**kwargs))
    def get_context_data(self, **kwargs):
        kwargs['heading_title']     = "Order Transaction"
        kwargs['card_title']        = "Customers data"
        kwargs['breadcrumb']        = {'content':'Order Product','url':'order_list_products'}
        kwargs['breadcrumb2']       = {'content':'Checkout','class':'active'}
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        return context
    def post(self, request, *args, **kwargs):
        """
        Handle POST requests: instantiate a form instance with the passed
        POST variables and then check if it's valid.
        """
        self.object = None # assign the object to the view
        User = get_user_model()
        method = self.request.POST['customer']
        cart   = Cart(request)
        if(method):
            try:
                qty = []
                product = []
                orders = True
                for x in Item.objects.all():
                    product.append(x.object_id)
                    qty.append(x.quantity)
                queryset = Products.objects.filter(id__in=product).values('stock')
                for i in range(len(queryset)):
                    if queryset[i]['stock']<=qty[i]:
                        orders = False
                if request.POST['payment'] == None:
                    orders = False

                name = None
                if(request.POST['name'] == "others"):
                    name = request.POST['name_input']
                else:
                    name = request.POST['name']

                if name == None:
                    orders = False
                if request.POST['barista'] == None:
                    orders = False
                
                if orders:    
                    barista  = User.objects.get(id=request.POST['barista']).id
                    customer = Customers.objects.filter(name=name).first()
                    if not customer:
                        customer = Customers.objects.create(
                            name=name,
                            email=request.POST['email'],
                            address=request.POST['address'],
                            phone=request.POST['phone'],
                            payment=request.POST['payment'],
                            barista_id=barista,
                        )

                    order = Orders(
                        invoice=generateInvoice(),
                        total=cart.summary(),
                        user_id=request.user.id,
                        customer_id=customer.id)
                    order.save()
                    if(order):
                        for x in Item.objects.all():
                            orderdetail = OrderDetails(
                                order_id = order.id,
                                product_id = x.object_id,
                                qty = x.quantity,
                                price = x.unit_price
                            )
                            orderdetail.save()
                            if(orderdetail):
                                product = Products.objects.get(id=x.object_id)
                                product.stock = F('stock') - x.quantity
                                product.save()
                                cart.clear()
                    return HttpResponseRedirect(self.get_success_url())
                else:
                    messages.error(request,'Order fail out of stock or form important null')
                    return redirect(reverse('check_out_product'))
            except Exception as e:
                messages.error(request,'Error! Code: {c}, Message, {m}'.format(c = type(e).__name__, m = str(e)))
                return redirect(reverse('check_out_product'))
    def get_success_url(self):
        """Return the URL to redirect to after processing a valid form."""
        if not self.success_url:
            raise ImproperlyConfigured("No URL to redirect to. Provide a success_url.")
        return reverse_lazy(self.success_url)  # success_url may be lazy

class OrdersView(FormView):
    form_class = OrdersForm
    success_url = 'order_list'
    def get(self, request, *args, **kwargs):
        """Handle GET requests: instantiate a blank version of the form."""
        total_order_details  = OrderDetails.objects.aggregate(total_item=Sum('qty'))
        total_order          = Orders.objects.aggregate(total_omset=Sum('total'))
        total_customers      = Customers.objects.all().count()
        kwargs['total_item']      = total_order_details['total_item']
        kwargs['total_omset']     = total_order['total_omset']
        kwargs['total_customers'] = total_customers
        kwargs['orders']          = Orders.objects.all().order_by('-created_at')
        return self.render_to_response(self.get_context_data(**kwargs))
        
    def get_context_data(self, **kwargs):
        kwargs['heading_title']     = "Order List"
        kwargs['breadcrumb']        = {'content':'Order List','class':'active'}
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        return context

class GenerateInvoicePrint(DetailView):
    def get(self, request, *args, **kwargs):
        """Handle GET requests: instantiate a blank version of the form."""
        self.object = None
        kwargs['totalPrice']           = OrderDetails.objects.filter(order_id=self.kwargs['pk']).aggregate(totalPrice=Sum('price'))
        kwargs['totalQty']             = OrderDetails.objects.filter(order_id=self.kwargs['pk']).aggregate(totalQty=Sum('qty'))
        kwargs['total']                = OrderDetails.objects.filter(order_id=self.kwargs['pk']).aggregate(total=Sum(F('qty') * F('price')))
        kwargs['order']                = OrderDetails.objects.all().filter(order_id=self.kwargs['pk'])
        kwargs['orders']               = Orders.objects.all().get(pk=self.kwargs['pk'])
        kwargs['date_order']           = Orders.objects.get(pk=self.kwargs['pk']).created_at
        return self.render_to_response(self.get_context_data(**kwargs))
        
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        return context

#def GenerateInvoicePDF(request,pk):

#     orders = Orders.objects.filter(id=pk)
#     html_string = render_to_string('invoice/invoice_pdf.html', {'orders': orders})

    # html = HTML(string=html_string)
    # html.write_pdf(target='/tmp/mypdf.pdf');

    # fs = FileSystemStorage('/tmp')
    # with fs.open('mypdf.pdf') as pdf:
    #     response = HttpResponse(pdf, content_type='application/pdf')
    #     response['Content-Disposition'] = 'attachment; filename="mypdf.pdf"'
    #     return response

    # return response