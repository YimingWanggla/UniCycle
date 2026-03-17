from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

# 1. 自定义用户模型 (对应 ER 图的 User 表)
class User(AbstractUser):
    # 覆盖默认配置，强制要求 Email，并将 Email 作为登录账号
    email = models.EmailField(unique=True, max_length=255)
    display_name = models.CharField(max_length=128, blank=True, null=True)
    # 不需要显式写 password，AbstractUser 已经自带了安全加密的 password 字段
    # 不需要显式写 created，AbstractUser 自带 date_joined
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username'] # 创建超级用户时除了email外还需要填的字段

    def __str__(self):
        return self.email

# 2. 分类模型 (对应 ER 图的 Category 表)
class Category(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name

# 3. 物品列表模型 (对应 ER 图的 Listing 表)
class Listing(models.Model):
    STATUS_CHOICES = [
        ('Available', 'Available'),
        ('Reserved', 'Reserved'),
        ('Sold', 'Sold'),
    ]

    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='listings')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='listings')
    title = models.CharField(max_length=64)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=16, choices=STATUS_CHOICES, default='Available')
    pickup_location = models.CharField(max_length=128)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

# 4. 物品图片模型 (对应 ER 图的 ListingImage 表)
class ListingImage(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='listing_images/') # 注意：这里用 ImageField 替代了简单的 Char URL

    def __str__(self):
        return f"Image for {self.listing.title}"

# 5. 消息模型 (对应 ER 图的 Message 表)
class Message(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.sender.email} about {self.listing.title}"

# 6. 收藏夹模型 (对应 ER 图的 Favourite 表)
class Favourite(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='favourites')
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='favourited_by')
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'listing') # 确保一个用户只能收藏一个物品一次

# 7. 举报模型 (对应 ER 图的 Report 表)
class Report(models.Model):
    reporter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reports_made')
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='reports_received')
    reason = models.TextField()
    created = models.DateTimeField(auto_now_add=True)