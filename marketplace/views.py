from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from .models import Listing
from .forms import CustomUserCreationForm

# 首页视图
def index(request):
    recent_listings = Listing.objects.filter(status='Available').order_by('-created')
    return render(request, 'marketplace/index.html', {'listings': recent_listings})

# 1. 注册视图
def register_user(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            # 核心需求 M1：强制校验大学邮箱
            if not (user.email.endswith('.edu') or user.email.endswith('.ac.uk')):
                messages.error(request, "Access denied. You must use a university email (.edu or .ac.uk).")
                return render(request, 'marketplace/register.html', {'form': form})
            
            user.save()
            login(request, user) # 注册成功后自动登录
            messages.success(request, f"Welcome to UniCycle, {user.email}!")
            return redirect('marketplace:index')
    else:
        form = CustomUserCreationForm()
    return render(request, 'marketplace/register.html', {'form': form})

# 2. 登录视图
def login_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "You are now logged in.")
            return redirect('marketplace:index')
    else:
        form = AuthenticationForm()
    return render(request, 'marketplace/login.html', {'form': form})

# 3. 登出视图
def logout_user(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect('marketplace:index')