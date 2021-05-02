from .models import Category,Products
from .forms import CategoryForm,ProductsForm
from django.views.generic import CreateView, DeleteView, UpdateView,ListView,FormView
from django.shortcuts import render_to_response
from django.urls import reverse,reverse_lazy
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import PermissionRequiredMixin

class CategoriesViews(PermissionRequiredMixin,SuccessMessageMixin, FormView):
    permission_required = ('products.add_category', 'products.view_category','products.change_category')
    success_url         = 'list_categories'
    form_class          = CategoryForm
    model               = Category
    success_message     = "Categories %(name)s  was created successfully"

    def handle_no_permission(self):
        # add custom message
        messages.error(self.request, 'You have no permission')
        return HttpResponseRedirect('/dashboard/')


    def get_context_data(self, **kwargs):
        kwargs['data_categories']   = Category.objects.all()
        kwargs['heading_title']      = "Management Products"
        kwargs['breadcrumb']        = {'content':'Categories','class':'active'}
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        return context

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests: instantiate a form instance with the passed
        POST variables and then check if it's valid.
        """
        form = self.get_form()
        method = self.request.POST.get('_method', '').lower()
        if method == 'put':
            categories_update = Category.objects.get(id=request.POST['id_categories'])
            self.success_message =  "Categories %(name)s was updated successfully"
            form = CategoryForm(request.POST or None,instance=categories_update)
        if method == 'delete':
            return self.request.POST.get('_method','')
    
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
    def form_valid(self, form):
        """If the form is valid, redirect to the supplied URL."""
        self.object = form.save()
        messages.success(self.request, self.success_message % dict(name=self.request.POST['name'],
        ))
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        """Return the URL to redirect to after processing a valid form."""
        if not self.success_url:
            raise ImproperlyConfigured("No URL to redirect to. Provide a success_url.")
        return reverse(self.success_url)  # success_url may be lazy

class DeleteCategories(PermissionRequiredMixin,SuccessMessageMixin,DeleteView):
    permission_required = ('products.delete_category')
    model = Category
    pk_url_kwarg = 'pk'
    success_url = 'list_categories'
    success_message = "Categories %(name)s was deleted successfully."
    def handle_no_permission(self):
        # add custom message
        messages.error(self.request, 'You have no permission')
        return HttpResponseRedirect('/dashboard/')
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)    
    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        messages.success(self.request, self.success_message % obj.__dict__ )
        return super(DeleteCategories, self).delete(request, *args, **kwargs)
    def get_success_url(self):
        if self.success_url:
            return reverse_lazy(self.success_url.format(**self.object.__dict__))
        else:
            raise ImproperlyConfigured(
                "No URL to redirect to. Provide a success_url.")

class ProductsViews(PermissionRequiredMixin,ListView):
    model = Products
    permission_required = ('products.view_products')
    def handle_no_permission(self):
        # add custom message
        messages.error(self.request, 'You have no permission')
        return HttpResponseRedirect('/dashboard/')
    def get_context_data(self, **kwargs):
        kwargs['heading_title'] = "Management Products"
        kwargs['breadcrumb']        = {'content':'Products','class':'active'}
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        return context

class CreateProduct(PermissionRequiredMixin,CreateView):
    form_class = ProductsForm
    permission_required = ('products.add_products')
    success_url = 'list_products'
    def handle_no_permission(self):
        # add custom message
        messages.error(self.request, 'You have no permission')
        return HttpResponseRedirect('/dashboard/')
    def get_context_data(self, **kwargs):
        kwargs['form']               = self.get_form()
        kwargs['heading_title']      = "Management Products"
        kwargs['breadcrumb']         = {'content':'Products','url':'list_products'}
        kwargs['breadcrumb2']        = {'content':'Add Product','class':'active'}
        kwargs['list_categories']    = Category.objects.all()
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        return context
    def get_success_url(self):
        """Return the URL to redirect to after processing a valid form."""
        if not self.success_url:
            raise ImproperlyConfigured("No URL to redirect to. Provide a success_url.")
        return reverse_lazy(self.success_url)  # success_url may be lazy
    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        self.object = form.save()
        return super().form_valid(form)
        
    def form_invalid(self, form):
        """If the form is invalid, render the invalid form."""
        return self.render_to_response(self.get_context_data())

class UpdateProduct(PermissionRequiredMixin,UpdateView):
    permission_required = ('products.change_products')
    form_class = ProductsForm
    model = Products
    success_url     = 'list_products'
    def handle_no_permission(self):
        # add custom message
        messages.error(self.request, 'You have no permission')
        return HttpResponseRedirect('/dashboard/')
    def get_context_data(self, **kwargs):
        """Insert the form into the context dict."""
        product_update = self.model.objects.get(pk=self.kwargs['pk'])
        kwargs['heading_title']     = "Management Products"
        kwargs['breadcrumb']        = "Update Product"
        kwargs['form']              = self.get_form()
        kwargs['list_categories']   = Category.objects.all()
        kwargs['product']           = product_update
        return super().get_context_data(**kwargs)
    
    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        self.object = form.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        """If the form is invalid, render the invalid form."""
        return self.render_to_response(self.get_context_data())
    def get_success_url(self):
        """Return the URL to redirect to after processing a valid form."""
        if not self.success_url:
            raise ImproperlyConfigured("No URL to redirect to. Provide a success_url.")
        return reverse_lazy(self.success_url)  # success_url may be lazy

class DeleteProduct(PermissionRequiredMixin,SuccessMessageMixin,DeleteView):
    permission_required = ('products.delete_products')
    model = Products
    pk_url_kwarg = 'pk'
    success_url = 'list_products'
    success_message = "Product %(name)s was deleted successfully."
    def handle_no_permission(self):
        # add custom message
        messages.error(self.request, 'You have no permission')
        return HttpResponseRedirect('/dashboard/')
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)    
    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        messages.success(self.request, self.success_message % obj.__dict__ )
        return super(DeleteProduct, self).delete(request, *args, **kwargs)
    def get_success_url(self):
        if self.success_url:
            return reverse_lazy(self.success_url.format(**self.object.__dict__))
        else:
            raise ImproperlyConfigured(
                "No URL to redirect to. Provide a success_url.")