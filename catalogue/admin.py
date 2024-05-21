from django.contrib import admin

# Register your models here.
from .models import Category, Tool, ToolInstance

admin.site.register(Tool)
admin.site.register(ToolInstance)
admin.site.register(Category)
