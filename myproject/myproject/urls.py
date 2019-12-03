from django.urls import path,include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',views.index),
    path('dashboard/',views.dashboard,name="dashboard"),
    path('accounts/',include('accounts.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('products/',include('products.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
