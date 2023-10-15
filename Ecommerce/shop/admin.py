from django.contrib import admin

# Register your models here.
from .models import ProductCategory, Product, ProdcutImage , Review , Cart

admin.site.register(ProductCategory)
admin.site.register(Product)
admin.site.register(ProdcutImage)
admin.site.register(Review)
admin.site.register(Cart)


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

class CartAdmin(admin.ModelAdmin):
    list_display = ( 'user_id' , 'product_id', 'quantity', 'created_date', 'updated_date', 'status')
    list_filter = ('user_id', 'product_id', 'created_date', 'updated_date', 'status')
    search_fields = ('product_id',)


