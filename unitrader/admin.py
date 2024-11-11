from django.contrib import admin
from .models import Item, Profile, Message
from .models import Media, Category, Landing, Navigation, Product, Review

# Register your models here
admin.site.register(Media)
admin.site.register(Category)
admin.site.register(Landing)
# admin.site.register(Navigation)
admin.site.register(Product)
admin.site.register(Review)
# Register the Profile model
admin.site.register(Profile)
admin.site.register(Item)
admin.site.register(Message)
