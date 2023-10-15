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
    path("productDetails/<int:id>" , views.productDetails , name="productDetails"),
    path("clothing/shop/" , views.shop , name="shop"),
    path("clothing/cart" , views.cart , name="cart"),
    path("add_to_cart/" , views.add_to_cart , name="add_to_cart"),
] 

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
