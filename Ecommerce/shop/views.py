from django.shortcuts import render , HttpResponse , redirect
from django.contrib.auth.models import User
from django.contrib.auth import  login  , authenticate , logout
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Product , ProductCategory , ProdcutImage  , Cart
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt



@csrf_exempt  
def add_to_cart(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        print("Received product_id:", product_id)
        return JsonResponse({'message': 'Product added to the cart successfully'})

    return JsonResponse({'message': 'Invalid request'})

def index(request):
    return render(request , "shop/index.html")

def logoutSession(request):
    logout(request)
    return redirect('index')

def productDetails(request , id):
    prod = Product.objects.get(id=id)
    product_images = ProdcutImage.objects.filter(product_id=id)
    context = {
        'product': prod,
        'product_images': product_images,
    }
   
    return render(request , "shop/product-details.html" , context)

def clothing(request):
    products = Product.objects.all()
    product_data = []

    for product in products:
        id = product.id
        image = ProdcutImage.objects.get(product_id=id)
        
        product_dict = {
            'product': product,
            'image': image,
            'side_image': image.side_image,
            'back_image': image.back_image,
            'front_image': image.front_image,  

        }
        
        product_data.append(product_dict)

    context = {
        'product_data': product_data,
    }

    return render(request, "shop/clothing.html", context)


def cart(request):
   
    user_id = request.user.id
   
    cart_items = Cart.objects.filter(user_id=user_id)
    cart_data = []
    for cart_item in cart_items:
        
        cart_dict = {
            'cart_item': cart_item,
            'product': cart_item.product_id,
            'name': cart_item.product_id.product_name,
            'price': cart_item.product_id.price,
            'product_image': ProdcutImage.objects.get(product_id=cart_item.product_id.id),
        }
        cart_data.append(cart_dict)
        print(cart_dict)
    context = {
        'cart_data': cart_data,
    }
    return render(request, "shop/cart.html" , context)


def shop(request):
    products = Product.objects.all()
    product_data = []
    try:
        sort_option = request.GET.get('sort', 'default')
        if sort_option == 'Low to Hight':
            products = Product.objects.order_by('price')
        elif sort_option == 'High to Low':
            products  = Product.objects.order_by('-price')
            print(products)
    except:
        pass
    for product in products:
        id = product.id
        image = ProdcutImage.objects.get(product_id=id)
        
        product_dict = {
            'product': product,
            'image': image,
            'side_image': image.side_image,
            'back_image': image.back_image,
            'front_image': image.front_image,  

        }
        
        product_data.append(product_dict)
    context = {
        'product_data': product_data,
    }

    return render(request , "shop/shop.html" , context)

def register(request):
    return render(request , "shop/register.html")

def logins(request):

   # if request.method == "GET":
    #    if request.user.is_authenticated:
     #       return redirect('index')
      #  return render(request, "shop/login.html")
    
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("tp_password")
       
        if email != "" and password != "":
            user = authenticate(username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
            else:
                return HttpResponse("User does not exist")
        return redirect('index')  
    return render(request, "shop/login.html")



def signup(request):
   if request.method == "POST": 
    user = request.POST.get("name")
    email = request.POST.get("email")
    password = request.POST.get("tp_password")
    
    if user != "" and email != "" and password != "":
       
       if User.objects.filter(username=user).exists():
             return HttpResponse("User already exists")
       userInfo = User.objects.create_user(user , email , password)
       userInfo.save()
       login_url = reverse('logins')
       return HttpResponseRedirect(login_url)
       return render(request , "shop/index.html")

   else:
      render(request , "shop/signup.html")

