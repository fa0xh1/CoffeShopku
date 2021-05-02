from django.urls import path,re_path,include
from django.contrib.auth.decorators import login_required, permission_required
from .views import *
urlpatterns = [
    path('categories/',login_required(CategoriesViews.as_view(template_name='products/categories/index.html')),name="list_categories"),
    path('categories/delete/<int:pk>', login_required(DeleteCategories.as_view()), name="delete_categories"),
    path('list/',login_required(ProductsViews.as_view(template_name='products/index.html')),name="list_products"),
    path('add/',login_required(CreateProduct.as_view(template_name='products/add_product.html')),name="add_product"),
    path('update/<int:pk>',login_required(UpdateProduct.as_view(template_name='products/edit_product.html')),name="update_product"),
    path('delete/<int:pk>',login_required(DeleteProduct.as_view()),name="delete_product"),
]
