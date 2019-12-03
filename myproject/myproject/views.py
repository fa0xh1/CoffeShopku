from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings

def index(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    return render(request,'index.html')
def dashboard(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    return render(request,'dashboard.html')