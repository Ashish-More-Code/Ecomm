from django.contrib import admin
from estoreapp.models import products
# Register your models here.


class productadmin(admin.ModelAdmin):
    list_display=['name','price','pdetails','cat','is_active']
    list_filter=['cat','is_active','price']
    
admin.site.register(products,productadmin)