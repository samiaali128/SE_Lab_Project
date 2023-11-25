from django.urls import path , include

from . import views
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views

urlpatterns = [
    
    path("", views.index, name="index"),
    path("register/", views.register, name="register"),
    path("signup/" , views.signup , name="signup"),
    path("login/" , views.logins , name="logins"),
    path("clothing/" , views.clothing , name="clothing"),
    path("logout/" , auth_views.LogoutView.as_view(), name='logout'),
    path('shop/productDetails/<int:id>/', views.productDetails, name='productDetails'),

    path("clothing/shop/" , views.shop , name="shop"),
    path("clothing/cart" , views.cart , name="cart"),
    path("clothing/remove_item_view" , views.remove_item_view , name="remove_item_view"),
    path("add_to_cart/" , views.add_to_cart , name="add_to_cart"),
    path("add_to_wishlist/" , views.add_to_wishlist , name="add_to_wishlist"),
    path("clothing/checkout/" , views.checkout , name="checkout"),
    path("clothing/update_cart" ,  views.update_cart , name="update_cart"),
    path("clothing/your_checkout_view " , views.your_checkout_view , name="your_checkout_view"),
    path("clothing/wishlist", views.wishlist, name="wishlist"),
    path("clothing/remove_from_wishlist", views.remove_from_wishlist, name="remove_from_wishlist"),
    path("clothing/order_history", views.order_history, name="order_history"),
    path("available_products", views.available_products, name="available_products"),
    path("on_sale_products" , views.on_sale_products , name="on_sale_products"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
