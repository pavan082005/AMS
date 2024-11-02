from django.contrib import admin
from .models import Item, Profile

# Register the Profile model
admin.site.register(Profile)
admin.site.register(Item)
