from django.contrib import admin
from django.db import models
from django.contrib.auth.models import User

class ProductCategory(models.Model):
    id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=100)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    status = models.CharField(max_length=50, default="Active")

    def __str__(self):
        return self.category_name



class Product(models.Model):
    id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=100)
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    price = models.FloatField(default=0)
    pub_date = models.DateField()
    quantity = models.IntegerField(default=0)
    description = models.CharField(max_length=3000)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    status = models.CharField(max_length=50, default="Active")

    def __str__(self):
        return self.product_name
    

class Cart(models.Model):
    id = models.AutoField(primary_key=True)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    status = models.CharField(max_length=50, default="Active")

    def __str__(self):
        return self.product_id.product_name 
    
class Deliveries(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='ProductInDelivery')
   
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    status = models.CharField(max_length=50, default="Active")
    
    def __str__(self):
        product_names = ", ".join([str(product.product_name) for product in self.products.all()])
        return f'Delivery {self.id} - Products: {product_names}'


    
class ProductInDelivery(models.Model):
    id = models.AutoField(primary_key=True)
    delivery_id = models.ForeignKey(Deliveries, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    status = models.CharField(max_length=50, default="Active")
    
    def __str__(self):
         return self.product.product_name
    

class CartsAudit(models.Model):
    id = models.AutoField(primary_key=True)
    cart_id = models.IntegerField()
    action_type = models.CharField(max_length=10)  # 'INSERT', 'UPDATE', 'DELETE'
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    product_id = models.IntegerField()
    status = models.CharField(max_length=50 , default="Active")
    #

    def __str__(self):
        return f'{self.action_type} on {self.timestamp} by {self.user}'


class ShippingAddress(models.Model):
    id = models.AutoField(primary_key=True)
    dilivery_id = models.ForeignKey(Deliveries, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    street_address = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    notes = models.CharField(max_length=100)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    status = models.CharField(max_length=50, default="Active")

    def __str__(self):
        return self.first_name + " " + self.last_name + " " + self.email

#


class ProductImage(models.Model):
    id = models.AutoField(primary_key=True)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="shop/images", default="", null=True, blank=True)
    side_image = models.ImageField(upload_to="shop/images", default="", null=True, blank=True)
    back_image = models.ImageField(upload_to="shop/images", default="", null=True, blank=True)
    front_image = models.ImageField(upload_to="shop/images", default="", null=True, blank=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    status = models.CharField(max_length=50, default="Active")

    def __str__(self):
        return self.product_id.product_name
    

class WeeklyOffers(models.Model):
    id = models.AutoField(primary_key=True)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    offer_price = models.IntegerField(default=0)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    status = models.CharField(max_length=50, default="Active")

    def __str__(self):
        return self.product_id.product_name
    
class WishlistAudit(models.Model):
    id = models.AutoField(primary_key=True)
    wishlist_id = models.IntegerField()
    action_type = models.CharField(max_length=10)  # 'INSERT', 'UPDATE', 'DELETE'
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    product_id = models.IntegerField()
    column_name = models.CharField(max_length=50)
    old_value = models.CharField(max_length=50)
    new_value = models.CharField(max_length=50)
    

    def __str__(self):
        return f'{self.action_type} on {self.timestamp} by {self.user}'
    

    
class Wishlist(models.Model):
    id = models.AutoField(primary_key=True)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    status = models.CharField(max_length=50, default="Active")

    def __str__(self):
        return self.product_id.product_name
    
class Auditloginfo(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    old_password = models.CharField(max_length=100)
    new_password = models.CharField(max_length=100)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    status = models.CharField(max_length=50, default="Active")

    def __str__(self):
        return self.user.username