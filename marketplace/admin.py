from django.contrib import admin
from .models import User, Category, Listing, ListingImage, Message, Favourite, Report

admin.site.register(User)
admin.site.register(Category)
admin.site.register(Listing)
admin.site.register(ListingImage)
admin.site.register(Message)
admin.site.register(Favourite)
admin.site.register(Report)