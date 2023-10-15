from django.db import models

# Create your models here.

    

class ProductCategory(models.Model):
    category_id = models.AutoField
    category_name = models.CharField(max_length=100)
    
    
    def __str__(self):
        return self.category_name
    
class Product(models.Model):
    product_id = models.AutoField
    product_name = models.CharField(max_length=100)
    category_id = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    price = models.IntegerField(default=0)
    pub_date = models.DateField()
    quantity = models.IntegerField(default=0)
    description = models.CharField(max_length=3000)
    
    
    def __str__(self):
        return self.product_name
    
    def getReview(self):
        return self.review_set.all()
    
    
class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    comment = models.TextField()

    def __str__(self):
        return f"Review for {self.product.product_name} - Rating: {self.rating}"

    
class Cart(models.Model):
    cart_id = models.AutoField
    user_id = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    created_date = models.DateField(auto_now_add=True)
    updated_date = models.DateField(auto_now=True)
    status = models.CharField(max_length=50, default="Active")

    def __str__(self):
        return self.product_id.product_name
    
class ProdcutImage(models.Model):
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="shop/images", default="" , null=True, blank=True)
    side_image = models.ImageField(upload_to="shop/images", default="" , null=True, blank=True)
    back_image = models.ImageField(upload_to="shop/images", default="" , null=True, blank=True)
    front_image = models.ImageField(upload_to="shop/images", default="" , null=True, blank=True)

    
    def __str__(self):
       
        return self.image.name 
