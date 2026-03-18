from django.contrib import admin
from .models import User, Category, Listing, ListingImage, Message, Favourite, Report

class ListingImageInline(admin.TabularInline):
    model = ListingImage
    extra = 1  # By default, 1 empty image upload slot is displayed

@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'seller', 'status', 'created')
    
    fields = ('title', 'category', 'seller', 'price', 'status', 'pickup_location', 'description')
    
    inlines = [ListingImageInline]

admin.site.register(User)
admin.site.register(Category)
admin.site.register(ListingImage)
admin.site.register(Message)
admin.site.register(Favourite)
admin.site.register(Report)