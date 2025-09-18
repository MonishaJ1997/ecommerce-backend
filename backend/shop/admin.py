from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Category, Product, Order, OrderItem

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id","name")

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id","name","category","price")
    list_filter = ("category",)
    search_fields = ("name","description")

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    readonly_fields = ("product","quantity")
    can_delete = False
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id","user","created_at")
    inlines = [OrderItemInline]
