from django import forms
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from django.contrib.auth import get_user_model,password_validation
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import Group,User,Permission

class AddUserForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = get_user_model()
        fields = ('username','email', 'password1', 'password2','user_permissions','groups','first_name','last_name')
    
    def save(self, commit=True):
        user = super(AddUserForm, self).save(commit)
        user.save()
        user.groups.set(self.cleaned_data.get('groups'))
        user.user_permissions.set(self.cleaned_data.get('user_permissions'))
        return user

class UpdateUserForm(UserChangeForm):
    # Feel free to add the password validation field as on UserCreationForm
    class Meta:
        model = get_user_model()
        # Add all the fields you want a user to change
        fields = ('username','email', 'password1', 'password2','user_permissions','groups','first_name','last_name')
    
    error_messages = {
        'password_mismatch': _('The two password fields didn’t match.'),
    }

    password1 = forms.CharField(
        label=_("Password"),
        strip=False,required=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label=_("Password confirmation"),required=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        strip=False,
        help_text=_("Enter the same password as before, for verification."),
    )

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def save(self, commit=True):
        user = super(UpdateUserForm, self).save(commit=False)
        password = self.clean_password2()
        if password:
            user.set_password(password)
        if commit:
            user.save()
            user.user_permissions.set(self.cleaned_data.get('user_permissions'))
            user.groups.set(self.cleaned_data.get('groups'))
        return user

class ProfileUserForm(UserChangeForm):
    # Feel free to add the password validation field as on UserCreationForm
    class Meta:
        model = get_user_model()
        # Add all the fields you want a user to change
        fields = ('username','email', 'password1', 'password2','first_name','last_name','avatar')
    
    error_messages = {
        'password_mismatch': _('The two password fields didn’t match.'),
    }

    password1 = forms.CharField(
        label=_("Password"),
        strip=False,required=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label=_("Password confirmation"),required=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        strip=False,
        help_text=_("Enter the same password as before, for verification."),
    )
    avatar       = forms.ImageField(required=False)
    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def save(self, commit=True):
        user = super(ProfileUserForm, self).save(commit=False)
        password = self.clean_password2()
        if password:
            user.set_password(password)
        if commit:
            user.save()
        return user


class GroupsForm(forms.ModelForm):

    class Meta:  
        model = Group  
        fields = "__all__"
    
    def save(self, commit=True):
        group = super(GroupsForm, self).save(commit)
        group.save()
        return group

class PermissionsForm(forms.ModelForm):

    codename    = forms.CharField(max_length=15,required=True)
    name        = forms.CharField(max_length=30,required=True)
    class Meta:
        model   = Permission
        fields  = "__all__"