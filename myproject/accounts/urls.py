from django.urls import path,re_path,include
from django.contrib.auth.views import LoginView,LogoutView
from django.contrib.auth.decorators import login_required, permission_required
from .views import *
urlpatterns = [
    # path('signup/', SignUp.as_view(template_name="auth/signup.html"), name='signup'),
    path('login/', LoginView.as_view(template_name='auth/login.html',redirect_authenticated_user=True),name="login_url"),
    path('logout/', LogoutView.as_view(next_page='login_url'),name="logout_url"),
    path('list', login_required(UsersView.as_view(template_name="accounts/list_users.html")), name="users_list"),
    path('profile/<int:pk>', login_required(ProfileView.as_view(template_name="accounts/profile.html")), name="profile_url"),
    path('add', login_required(CreateUser.as_view(template_name="accounts/add_edit.html")), name="add_user"),
    path('update/<int:pk>', login_required(UpdateUser.as_view(template_name="accounts/add_edit.html")), name="update_user"),
    path('delete/<int:pk>', login_required(DeleteUser.as_view()), name="delete_user"),
    path('groups/', login_required(GroupsPermissions.as_view(template_name='accounts/groups.html')),name='groups_list'),
    path('groups/delete/<int:pk>', login_required(DeleteGroup.as_view()), name="delete_group"),
    path('permissions-groups/', login_required(PermissionsGroups.as_view(template_name='accounts/groups_permissions.html')), name="permissions_groups"),
]
