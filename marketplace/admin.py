from django.contrib import admin
from .models import User, Category, Listing, ListingImage, Message, Favourite, Report

class ListingImageInline(admin.TabularInline):
    model = ListingImage
    extra = 1  # 默认显示1个空白的图片上传槽位

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