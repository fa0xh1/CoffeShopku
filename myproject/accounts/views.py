from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import User
from .forms import UpdateUserForm,AddUserForm,GroupsForm,PermissionsForm,ProfileUserForm
from django.views.generic import CreateView, DeleteView, UpdateView,ListView
from django.shortcuts import render_to_response
from django.urls import reverse,reverse_lazy
from django.http import HttpResponseRedirect,Http404
from django.utils.translation import ugettext_lazy as _
from django.views import generic
from django.views.generic import TemplateView
from django.contrib import messages
from django.contrib.auth.models import Permission,Group
from django.contrib.contenttypes.models import ContentType
from django.views.generic import FormView
from django.contrib.auth.mixins import PermissionRequiredMixin


class UsersView(PermissionRequiredMixin,ListView):
# Create your views here.
    model = User
    permission_required = ('accounts.view_user')
    def handle_no_permission(self):
        # add custom message
        messages.error(self.request, 'You have no permission')
        return HttpResponseRedirect('/dashboard/')

    def get_context_data(self, **kwargs):
        kwargs['heading_title']        = "Management Users"
        kwargs['breadcrumb']           = {'content':'Users','class':'active'}
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        return context

class CreateUser(PermissionRequiredMixin,CreateView):

    form_class = AddUserForm
    success_url = 'users_list'
    permission_required = ('accounts.add_user')
    def handle_no_permission(self):
        # add custom message
        messages.error(self.request, 'You have no permission')
        return HttpResponseRedirect('/dashboard/')
    def get_context_data(self, **kwargs):
        """Insert the form into the context dict."""
        kwargs = {
            'groups'              : Group.objects.all(),
            'card_title'          : 'Add User',
            'heading_title'       : 'Management Users',
            'breadcrumb'          : {'content':'Users','url':'users_list'},
            'breadcrumb2'          : {'content':'Add user','class':'active'},
            'user_permissions'    : Permission.objects.all(),
        }
        if 'form' not in kwargs:
            kwargs['form']          = self.get_form()
        
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        self.object = form.save()
        return super().form_valid(form)
        
    def form_invalid(self, form):
        """If the form is invalid, render the invalid form."""
        return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        """Return the URL to redirect to after processing a valid form."""
        if self.success_url:
            url = self.success_url.format(**self.object.__dict__)
        else:
            try:
                url = self.object.get_absolute_url()
            except AttributeError:
                raise ImproperlyConfigured(
                    "No URL to redirect to.  Either provide a url or define"
                    " a get_absolute_url method on the Model.")
        return reverse(url)

class ProfileView(UpdateView):
    form_class      = ProfileUserForm
    model           = User
    success_url     = 'profile_url'
    def setup(self, request, *args, **kwargs):
        """Initialize attributes shared by all view methods."""
        self.request = request
        self.args = args
        self.kwargs = kwargs
    def get_object(self, queryset=None):
        """
        Return the object the view is displaying.
        Require `self.queryset` and a `pk` or `slug` argument in the URLconf.
        Subclasses can override this to return any object.
        """
        # Use a custom queryset if provided; this is required for subclasses
        # like DateDetailView
        if queryset is None:
            queryset = self.get_queryset()
        # Next, try looking up by primary key.
        pk = self.request.user.id
        slug = self.kwargs.get(self.slug_url_kwarg)
        if pk is not None:
            queryset = queryset.filter(pk=pk)
        # Next, try looking up by slug.
        if slug is not None and (pk is None or self.query_pk_and_slug):
            slug_field = self.get_slug_field()
            queryset = queryset.filter(**{slug_field: slug})
        # If none of those are defined, it's an error.
        if pk is None and slug is None:
            raise AttributeError(
                "Generic detail view %s must be called with either an object "
                "pk or a slug in the URLconf." % self.__class__.__name__
            )
        try:
            # Get the single item from the filtered queryset
            obj = queryset.get()
        except queryset.model.DoesNotExist:
            raise Http404(_("No %(verbose_name)s found matching the query") %
                        {'verbose_name': queryset.model._meta.verbose_name})
        return obj
        
    def get(self, request, *args, **kwargs):
        """Handle GET requests: instantiate a blank version of the form."""
        self.object = self.get_object() # assign the object to the viewuse
        user_id     = request.user.id
        if(self.kwargs['pk'] == user_id):
            return self.render_to_response(self.get_context_data())
        else:
            return HttpResponseRedirect(reverse('profile_url',kwargs={'pk':user_id}))
            
    def get_context_data(self,**kwargs):
        user_update = User.objects.get(pk=self.kwargs['pk'])
        kwargs      = super().get_context_data(**kwargs)
        kwargs = {
            "user"               : user_update,
        }
        if 'form' not in kwargs:
            kwargs['form'] = self.get_form()
        kwargs['heading_title']    = "Profile"
        kwargs['breadcrumb']      = {'content':'Profile','class':'active'}
        
        return super().get_context_data(**kwargs)

    def get_success_url(self):
        """Return the URL to redirect to after processing a valid form."""
        if self.success_url:
            url = self.success_url.format(**self.object.__dict__)
        else:
            try:
                url = self.object.get_absolute_url()
            except AttributeError:
                raise ImproperlyConfigured(
                    "No URL to redirect to.  Either provide a url or define"
                    " a get_absolute_url method on the Model.")
        return reverse(url,kwargs={'pk': self.object.id})

    def form_invalid(self, form):
        """If the form is invalid, render the invalid form."""
        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        self.object = form.save()
        return super().form_valid(form)

class UpdateUser(PermissionRequiredMixin,UpdateView):
    form_class      = UpdateUserForm
    model           = User
    success_url     = 'users_list'
    permission_required = ('accounts.change_user')
    def handle_no_permission(self):
        # add custom message
        messages.error(self.request, 'You have no permission')
        return HttpResponseRedirect('/dashboard/')
    # That should be all you need. If you need to do any more custom stuff 
    # before saving the form, override the `form_valid` method, like this:
    def get_context_data(self,**kwargs):
        user_update = User.objects.get(pk=self.kwargs['pk'])
        kwargs      = super().get_context_data(**kwargs)
        if 'form' not in kwargs:
            kwargs['form'] = self.get_form()
        kwargs = {
            "card_title"          : "Edit User",
            "users"               : user_update,
            'groups'              : Group.objects.all(),
            "user_permissions"    : Permission.objects.all(),
            "curent_groups"       : [(x.id) for x in user_update.groups.all() ],
            "curent_permissions"  : [(x.id) for x in user_update.user_permissions.all()],
        }
        kwargs['heading_title']    = "Management Users"
        kwargs['breadcrumb']       = {'content':'Users','url':'users_list',}
        kwargs['breadcrumb2']      = {'content':'Edit user','class':'active'}
        
        return super().get_context_data(**kwargs)
        
    def get_success_url(self):
        """Return the URL to redirect to after processing a valid form."""
        if self.success_url:
            url = self.success_url.format(**self.object.__dict__)
        else:
            try:
                url = self.object.get_absolute_url()
            except AttributeError:
                raise ImproperlyConfigured(
                    "No URL to redirect to.  Either provide a url or define"
                    " a get_absolute_url method on the Model.")
        return reverse(url)

    def form_invalid(self, form):
        """If the form is invalid, render the invalid form."""
        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        self.object = form.save()
        return super().form_valid(form)

class DeleteUser(PermissionRequiredMixin,DeleteView):
    model           = User
    pk_url_kwarg    = 'pk'
    success_url     = 'users_list'
    permission_required = ('accounts.delete_user')
    def handle_no_permission(self):
        # add custom message
        messages.error(self.request, 'You have no permission')
        return HttpResponseRedirect('/dashboard/')
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)    

    def get_success_url(self):
        if self.success_url:
            return reverse(self.success_url.format(**self.object.__dict__))
        else:
            raise ImproperlyConfigured(
                "No URL to redirect to. Provide a success_url.")

class SignUp(generic.CreateView):
    form_class  = AddUserForm
    success_url = reverse_lazy('login_url')

class GroupsPermissions(PermissionRequiredMixin,FormView):

    template_name   = None
    form_class      = GroupsForm
    success_url     = 'groups_list'	
    permission_required = ('auth.view_group','auth.change_group','auth.add_group')
    def handle_no_permission(self):
        # add custom message
        messages.error(self.request, 'You have no permission')
        return HttpResponseRedirect('/dashboard/')
    def get_context_data(self, **kwargs):
        """Insert the form into the context dict."""
        if 'form' not in kwargs:
            kwargs['form'] = self.get_form()
        kwargs['heading_title']        = "Management Groups"
        kwargs['breadcrumb']        = {'content':'Groups','class':'active',}
        # kwargs['breadcrumb2']        = {'content':'Add user','class':'active'}
        kwargs['user_groups']      = Group.objects.all()
        return super().get_context_data(**kwargs)
    def form_valid(self, form):
        """If the form is valid, redirect to the supplied URL."""
        self.object = form.save()
        return HttpResponseRedirect(self.get_success_url())
    def get_success_url(self):
        """Return the URL to redirect to after processing a valid form."""
        if not self.success_url:
            raise ImproperlyConfigured("No URL to redirect to. Provide a success_url.")
        return reverse_lazy(self.success_url)  # success_url may be lazy
class DeleteGroup(PermissionRequiredMixin,DeleteView):
    model           = Group
    pk_url_kwarg    = 'pk'
    success_url     = 'groups_list'
    permission_required = ('auth.delete_group')
    def handle_no_permission(self):
        # add custom message
        messages.error(self.request, 'You have no permission')
        return HttpResponseRedirect('/dashboard/')
    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)

    def get_success_url(self):
        if self.success_url:
            return reverse(self.success_url.format(**self.object.__dict__))
        else:
            raise ImproperlyConfigured(
                "No URL to redirect to. Provide a success_url.")

class PermissionsGroups(PermissionRequiredMixin,FormView):
    template_name   = None
    form_class      = PermissionsForm
    success_url     = 'permissions_groups'
    permission_required = ('auth.view_group','auth.change_group','auth.add_group','auth.add_permission','auth.change_permission','auth.delete_permission')
    def handle_no_permission(self):
        # add custom message
        messages.error(self.request, 'You have no permission')
        return HttpResponseRedirect('/dashboard/')
    def get(self, request, *args, **kwargs):
        """Handle GET requests: instantiate a blank version of the form."""
        # if request.GET['groups'] != None:
        if request.method == 'GET' and 'groups' in request.GET:
            group_id = request.GET['groups']
            if group_id is not None and group_id != '':
                group_update = Group.objects.get(id=group_id)
                kwargs['user_permissions']    = Permission.objects.all()
                kwargs['curent_permissions']  = [(x.id) for x in group_update.permissions.all()]
        return self.render_to_response(self.get_context_data(**kwargs))
    def get_context_data(self, **kwargs):
        """Insert the form into the context dict."""
        if 'form' not in kwargs:
            kwargs['form'] = self.get_form()
        kwargs['user_groups']      = Group.objects.all()
        kwargs['heading_title']        = "Management Groups Permissions"
        kwargs['breadcrumb']        = {'content':'Permissions Groups','class':'active',}
        return super().get_context_data(**kwargs)
    
    def form_invalid(self, form):
        """If the form is invalid, render the invalid form."""
        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):
        """If the form is valid, redirect to the supplied URL."""
        self.object = form.save()
        return HttpResponseRedirect(self.get_success_url())
    def post(self, request, *args, **kwargs):
        """
        Handle POST requests: instantiate a form instance with the passed
        POST variables and then check if it's valid.
        """
        if request.method == 'POST' and 'manage_permission' in request.POST:
            group_id = request.GET['groups']
            request.POST.getlist('user_permissions')
            permission = [(x) for x in request.POST.getlist('user_permissions')]
            if group_id is not None and group_id != '':
                group = Group.objects.get(id=group_id)
                if len(permission) != 0:
                    group.permissions.set(permission)
                else:
                    group.permissions.clear()

        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
    def get_success_url(self):
        """Return the URL to redirect to after processing a valid form."""
        if not self.success_url:
            raise ImproperlyConfigured("No URL to redirect to. Provide a success_url.")
        return reverse_lazy(self.success_url)  # success_url may be lazy

class UsersApi(TemplateView):
    template_name = None