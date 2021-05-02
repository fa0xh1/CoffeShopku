from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.views.generic import FormView
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from customers.forms import OrdersForm
from customers.models import Orders,OrderDetails,Customers
from products.models import Products
from django.db.models import Sum,Count
from django.db.models import F
from django.utils.safestring import mark_safe
import datetime
import xlwt

def index(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    return render(request,'index.html')

class Dashboard(FormView):
    form_class = OrdersForm
    def get(self, request, *args, **kwargs):
        """Handle GET requests: instantiate a blank version of the form."""
        total_order_details  = OrderDetails.objects.aggregate(total_item=Sum('qty'))
        total_order          = Orders.objects.aggregate(total_omset=Sum('total'))
        total_customers      = Customers.objects.all().count()
        kwargs['total_item']      = total_order_details['total_item']
        kwargs['total_omset']     = total_order['total_omset']
        kwargs['total_customers'] = total_customers
        # kwargs['orders']          = Orders.objects.all().order_by('created_at')
        a = []
        items = Orders.objects.all().extra({'created_at' : "date(created_at)"}).values('created_at').annotate(created_sum=Sum('total'))
        items = list(items)
        dates = [x.get('created_at') for x in items]
        counttotal = [x.get('created_sum') for x in items]
        for d in (datetime.date.today() - datetime.timedelta(days=x) for x in range(0,30)):
            if d not in dates:
                a.append(0)
        a += counttotal
        kwargs['saleschart']    = a
        o = OrderDetails.objects.all().values('product_id').annotate(sum_qty=Sum('qty'))
        qty = [x.get('sum_qty') for x in o]
        p_id = [i.get('product_id') for i in o]
        p = []
        for p_id in Products.objects.all():
            p.append(p_id.name)
        kwargs['labels_products'] = mark_safe(p)
        kwargs['qty_producs'] = qty
        return self.render_to_response(self.get_context_data(**kwargs))
        
    def get_context_data(self, **kwargs):
        kwargs['heading_title']     = "Dashboard"
        kwargs['breadcrumb']        = {'content':'Dashboard','class':'active'}
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        return context

class ReportExcel(FormView):
    form_class = OrdersForm
    def get(self, request, *args, **kwargs):
        """Handle GET requests: instantiate a blank version of the form."""
        User = get_user_model()
        kwargs['cashier'] = User.objects.all().filter(groups__name='Cashier')
        return self.render_to_response(self.get_context_data(**kwargs))

    def get_context_data(self, **kwargs):
        kwargs['heading_title']     = "Report"
        kwargs['breadcrumb']        = {'content':'Report','class':'active'}
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        return context
    
    def post(self, request, *args, **kwargs):
        """
        Handle POST requests: instantiate a form instance with the passed
        POST variables and then check if it's valid.
        """
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="sales.xls"'

        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('Sales')

        # Sheet header, first row
        row_num = 0

        font_style = xlwt.XFStyle()
        font_style.font.bold = True

        columns = ['Invoice', 'Cashier', 'Customers', 'Total']

        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)

        # Sheet body, remaining rows
        font_style = xlwt.XFStyle()

        if request.POST['cashier'] != "none":
            rows = Orders.objects.all().filter(created_at__range=[request.POST['start_date'], request.POST['end_date']],user_id=request.POST['cashier']).values_list('invoice', 'user__username', 'customer__name', 'total')
        else:
            rows = Orders.objects.all().filter(created_at__range=[request.POST['start_date'], request.POST['end_date']]).values_list('invoice', 'user__username', 'customer__name', 'total')
        for row in rows:
            row_num += 1
            for col_num in range(len(row)):
                ws.write(row_num, col_num, row[col_num], font_style)
        
        wb.save(response)
        return response