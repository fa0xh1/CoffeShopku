from django.urls import path,include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required, permission_required

urlpatterns = [
    path('',login_required(views.Dashboard.as_view(template_name='dashboard.html'))),
    path('dashboard/',login_required(views.Dashboard.as_view(template_name='dashboard.html')),name="dashboard"),
    path('report/excel',login_required(views.ReportExcel.as_view(template_name='report/report_xls.html')), name="report_excel"),
    path('accounts/',include('accounts.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('products/',include('products.urls')),
    path('orders/',include('customers.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
