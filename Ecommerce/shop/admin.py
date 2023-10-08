from django.contrib import admin

# Register your models here.
from .models import ProductCategory, Product, ProdcutImage , Review

admin.site.register(ProductCategory)
admin.site.register(Product)
admin.site.register(ProdcutImage)
admin.site.register(Review)


class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'category_id', 'price', 'pub_date', 'description')
    list_filter = ('category_id', 'pub_date')
    search_fields = ('product_name'),
    date_hierarchy = 'pub_date'

class ProductImagesAdmin(admin.ModelAdmin):
    list_display = ('product_id', 'image')
    list_filter = ('product_id',)

class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ('category_name',)
    search_fields = ('category_name'),

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product_id', 'rating', 'comment')
    list_filter = ('product_id', 'rating')
    search_fields = ('product_id',)

