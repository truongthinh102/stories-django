from django.contrib import admin

# Register your models here.
from .models import Category, Contact, Story
admin.site.register(Category)
admin.site.register(Story)
admin.site.register(Contact)

