from django.contrib import admin
from .models import Category, Product

# Регистрация моделей в админке
admin.site.register(Category)
admin.site.register(Product)