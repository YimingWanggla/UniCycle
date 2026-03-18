from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from .models import Listing, ListingImage, Category
from .forms import CustomUserCreationForm
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, ListingForm

# Home Page View
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

# 1. Registration View
def register_user(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            # Core Requirement M1: Mandatory verification of university email addresses
            if not (user.email.endswith('.edu') or user.email.endswith('.ac.uk')):
                messages.error(request, "Access denied. You must use a university email (.edu or .ac.uk).")
                return render(request, 'marketplace/register.html', {'form': form})
            
            user.save()
            login(request, user) # You will be automatically logged in after successful registration.
            messages.success(request, f"Welcome to UniCycle, {user.email}!")
            return redirect('marketplace:index')
    else:
        form = CustomUserCreationForm()
    return render(request, 'marketplace/register.html', {'form': form})

# 2. Login View
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

# 3. Logout View
def logout_user(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect('marketplace:index')

# 4. Product Details Page
def listing_detail(request, listing_id):
    # Search the database using the provided listing_id; if it is not found, return a 404 page.
    listing = get_object_or_404(Listing, pk=listing_id)
    return render(request, 'marketplace/listing_detail.html', {'listing': listing})

# 5. View Listings (Users who are not logged in will be redirected to the login page)
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