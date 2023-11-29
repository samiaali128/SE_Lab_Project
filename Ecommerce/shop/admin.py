from django.contrib import admin

# Register your models here.
from .models import ProductCategory, Product, Cart , ProductImage , ShippingAddress , Deliveries , ProductInDelivery , WeeklyOffers , Wishlist , Auditloginfo , CartsAudit , WishlistAudit

admin.site.register(ProductCategory)
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(ProductImage)
admin.site.register(ShippingAddress)
admin.site.register(ProductInDelivery)
admin.site.register(Deliveries)
admin.site.register(WeeklyOffers)
admin.site.register(Wishlist)
admin.site.register(Auditloginfo)
admin.site.register(CartsAudit)
admin.site.register(WishlistAudit)





class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'product_id', 'user', 'quantity', 'created_at', 'updated_at', 'status')
    list_filter = ('id', 'product_id', 'user', 'quantity', 'created_at', 'updated_at', 'status')
    search_fields = ('id', 'product_id', 'user', 'quantity', 'created_at', 'updated_at', 'status')
    ordering = ('id', 'product_id', 'user', 'quantity', 'created_at', 'updated_at', 'status')


class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'product_name', 'category', 'price', 'pub_date', 'quantity', 'description', 'created_at', 'updated_at', 'status')
    list_filter = ('id', 'product_name', 'category', 'price', 'pub_date', 'quantity', 'description', 'created_at', 'updated_at', 'status')
    search_fields = ('id', 'product_name', 'category', 'price', 'pub_date', 'quantity', 'description', 'created_at', 'updated_at', 'status')
    ordering = ('id', 'product_name', 'category', 'price', 'pub_date', 'quantity', 'description', 'created_at', 'updated_at', 'status')


class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'category_name', 'created_at', 'updated_at', 'status')
    list_filter = ('id', 'category_name', 'created_at', 'updated_at', 'status')
    search_fields = ('id', 'category_name', 'created_at', 'updated_at', 'status')
    ordering = ('id', 'category_name', 'created_at', 'updated_at', 'status')


class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'product_id', 'image', 'side_image', 'back_image', 'front_image', 'created_at', 'updated_at', 'status')
    list_filter = ('id', 'product_id', 'image', 'side_image', 'back_image', 'front_image', 'created_at', 'updated_at', 'status')
    search_fields = ('id', 'product_id', 'image', 'side_image', 'back_image', 'front_image', 'created_at', 'updated_at', 'status')
    ordering = ('id', 'product_id', 'image', 'side_image', 'back_image', 'front_image', 'created_at', 'updated_at', 'status')


class ShippingAddressAdmin(admin.ModelAdmin):
    list_display = ('id', 'dilivery_id', 'first_name', 'last_name', 'email', 'address', 'country', 'state', 'zip_code', 'created_at', 'updated_at', 'status')
    list_filter = ('id', 'dilivery_id', 'first_name', 'last_name', 'email', 'address', 'country', 'state', 'zip_code', 'created_at', 'updated_at', 'status')
    search_fields = ('id', 'dilivery_id', 'first_name', 'last_name', 'email', 'address', 'country', 'state', 'zip_code', 'created_at', 'updated_at', 'status')
    ordering = ('id', 'dilivery_id', 'first_name', 'last_name', 'email', 'address', 'country', 'state', 'zip_code', 'created_at', 'updated_at', 'status')


class DeliveriesAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'product_id', 'quantity', 'created_at', 'updated_at', 'status')
    list_filter = ('id', 'user', 'product_id', 'quantity', 'created_at', 'updated_at', 'status')
    search_fields = ('id', 'user', 'product_id', 'quantity', 'created_at', 'updated_at', 'status')
    ordering = ('id', 'user', 'product_id', 'quantity', 'created_at', 'updated_at', 'status')


class ProductInDeliveryAdmin(admin.ModelAdmin):
    list_display = ('id', 'delivery_id', 'product', 'quantity', 'created_at', 'updated_at', 'status')
    list_filter = ('id', 'delivery_id', 'product', 'quantity', 'created_at', 'updated_at', 'status')
    search_fields = ('id', 'delivery_id', 'product', 'quantity', 'created_at', 'updated_at', 'status')
    ordering = ('id', 'delivery_id', 'product', 'quantity', 'created_at', 'updated_at', 'status')


class WeeklyOffersAdmin(admin.ModelAdmin):
    list_display = ('id', 'product_id', 'offer_price', 'created_at', 'updated_at', 'status')
    list_filter = ('id', 'product_id', 'offer_price', 'created_at', 'updated_at', 'status')
    search_fields = ('id', 'product_id', 'offer_price', 'created_at', 'updated_at', 'status')
    ordering = ('id', 'product_id', 'offer_price', 'created_at', 'updated_at', 'status')


class WishlistAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'product_id', 'created_at', 'updated_at', 'status')
    list_filter = ('id', 'user', 'product_id', 'created_at', 'updated_at', 'status')
    search_fields = ('id', 'user', 'product_id', 'created_at', 'updated_at', 'status')
    ordering = ('id', 'user', 'product_id', 'created_at', 'updated_at', 'status')


class AuditloginfoAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'column_name', 'old_value', 'new_value', 'created_at', 'updated_at', 'status')
    list_filter = ('id', 'user', 'old_password', 'new_password', 'created_at', 'updated_at', 'status')
    search_fields = ('id', 'user', 'old_password','new_password',  'created_at', 'updated_at', 'status')
    ordering = ('id', 'user', 'old_password', 'new_password',  'created_at', 'updated_at', 'status')

class CartsAuditAdmin(admin.ModelAdmin):
    list_display = ('id', 'cart_id', 'action_type', 'timestamp', 'user', 'product_id',  'status')
    list_filter = ('id', 'user', 'product_id', 'quantity', 'created_at', 'updated_at', 'status')
    search_fields = ('id', 'user', 'product_id', 'quantity', 'created_at', 'updated_at', 'status')
    ordering = ('id', 'user', 'product_id', 'quantity', 'created_at', 'updated_at', 'status')


class WishlistAuditAdmin(admin.ModelAdmin):
    list_display = ('id', 'wishlist_id', 'action_type', 'timestamp', 'user', 'product_id',  'column_name' , 'old_value' , 'new_value' )
    list_filter = ('id', 'wishlist_id', 'action_type', 'timestamp', 'user', 'product_id',  'column_name' , 'old_value' , 'new_value' )
    search_fields = ('id', 'wishlist_id', 'action_type', 'timestamp', 'user', 'product_id',  'column_name' , 'old_value' , 'new_value' )
    ordering =('id', 'wishlist_id', 'action_type', 'timestamp', 'user', 'product_id',  'column_name' , 'old_value' , 'new_value' )