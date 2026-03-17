from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from .models import Listing, ListingImage, Category
from .forms import CustomUserCreationForm
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, ListingForm

# 首页视图
def index(request):
    query = request.GET.get('q')
    category_id = request.GET.get('category')
    
    listings = Listing.objects.all().order_by('-created')
    categories = Category.objects.all()
    
    if query:
        listings = listings.filter(
            Q(title__icontains=query) | 
            Q(description__icontains=query)
        )
        
    selected_category = None
    if category_id and category_id.isdigit():
        selected_category = int(category_id)
        listings = listings.filter(category_id=selected_category)
        
    return render(request, 'marketplace/index.html', {
        'listings': listings,
        'search_query': query,
        'categories': categories, 
        'selected_category': selected_category
    })

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

# 4. 商品详情视图
def listing_detail(request, listing_id):
    # 根据传入的 listing_id 去数据库查找，找不到就返回 404 页面
    listing = get_object_or_404(Listing, pk=listing_id)
    return render(request, 'marketplace/listing_detail.html', {'listing': listing})

# 5. 发布物品视图 (没登录的人会被赶去登录页)
@login_required(login_url='marketplace:login')
def post_item(request):
    if request.method == 'POST':
        form = ListingForm(request.POST, request.FILES)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.seller = request.user
            listing.save()
            
            images = request.FILES.getlist('images')
            for img in images:
                ListingImage.objects.create(listing=listing, image=img)
                
            messages.success(request, "🎉 Item posted successfully with images!")
            return redirect('marketplace:index')
    else:
        form = ListingForm()
        
    return render(request, 'marketplace/post_item.html', {'form': form})