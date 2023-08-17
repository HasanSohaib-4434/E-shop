from django.contrib import admin

from store.models import Product
from store.models import Category
from store.models import Customer
from store.models import Order

class AdminProduct(admin.ModelAdmin):
    list_display=['name','price','category']


class AdminCategory(admin.ModelAdmin):
    list_display=['name']


admin.site.register(Product,AdminProduct)
admin.site.register(Category,AdminCategory)
admin.site.register(Customer)
admin.site.register(Order)
# Register your models here.
