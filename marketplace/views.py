from django.shortcuts import render
from .models import Listing

def index(request):
    # 从数据库里捞出所有状态为 'Available' 的物品，并且按时间倒序排（最新的在最上面）
    recent_listings = Listing.objects.filter(status='Available').order_by('-created')
    
    # 把捞出来的数据打包成一个字典，准备发给网页
    context = {
        'listings': recent_listings
    }
    
    # 把数据传递给 index.html
    return render(request, 'marketplace/index.html', context)