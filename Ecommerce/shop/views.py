from django.shortcuts import render , HttpResponse , redirect
from django.contrib.auth.models import User
from django.contrib.auth import  login  , authenticate , logout
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Product , ProductCategory , ProdcutImage 


# Create your views here.

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

