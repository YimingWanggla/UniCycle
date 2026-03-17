from django.contrib import admin
from .models import User, Category, Listing, ListingImage, Message, Favourite, Report

@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'seller', 'status', 'created')
    fields = ('title', 'category', 'seller', 'price', 'status', 'pickup_location', 'description', 'image')

admin.site.register(User)
admin.site.register(Category)
admin.site.register(ListingImage)
admin.site.register(Message)
admin.site.register(Favourite)
admin.site.register(Report)