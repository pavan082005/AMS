from django.contrib import admin
from .models import Item, Profile, Message

# Register the Profile model
admin.site.register(Profile)
admin.site.register(Item)
admin.site.register(Message)
