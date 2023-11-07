from django.shortcuts import render , HttpResponse , redirect
from django.contrib.auth.models import User
from django.contrib.auth import  login  , authenticate , logout
from django.http import HttpResponseRedirect
from django.urls import reverse 
from django.db.models import Q
from .models import Product , ProductCategory , ProductImage  , Cart , Deliveries , ShippingAddress , ProductInDelivery , WeeklyOffers , Wishlist  , CartsAudit , WishlistAudit
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from datetime import datetime


# function to create audit log

def create_audit_log(cart_id, action_type, user_id, product_id ,status):
    CartsAudit.objects.create(
        cart_id=cart_id,
        action_type=action_type,
        user=user_id,
        product_id=product_id,
        status= status
    )


@csrf_exempt  
def add_to_cart(request):
    if request.method == 'POST':
        # get the product id from the request
        product_id = request.POST.get('product_id')
        
        user_id = request.user.id
        product = Product.objects.get(id=product_id)
        # first check exist and status is active in cart

        if Cart.objects.filter(product_id=product_id, user_id=user_id, status='Active').exists():

            return JsonResponse({'message': 'Product already added to the cart'})
        
        # check if product quantity is available
        if product.quantity <= 0:
            return JsonResponse({'message': 'Product is out of stock'})
        
        else :
            
            # check if product is in deactive status in cart then update status to active

            if Cart.objects.filter(product_id=product_id, user_id=user_id, status='Deactive').exists():
                cart = Cart.objects.get(product_id=product_id, user_id=user_id, status='Deactive')
                cart.status = 'Active'
                cart.quantity = 0
                cart.save()

                # create audit log
                cart_action = 'UPDATE'
                create_audit_log(cart.id, cart_action, request.user, product.id , "Active")
                return JsonResponse({'message': 'Product added to the cart successfully'})
            else:
                
                # create new cart item 
                cart = Cart.objects.create(product_id=product, user_id=user_id , quantity=0)
                cart.save()

                # create audit log
                cart_action = 'INSERT'
                create_audit_log(cart.id, cart_action, request.user, product.id  , "Active")

                return JsonResponse({'message': 'Product added to the cart successfully'})


      
    return JsonResponse({'message': 'Invalid request'})


# function to create wishlist audit log
def create_wishlist_audit_log(wishlist_id, action_type, user_id, product_id ,column_name , old_value , new_value):
    WishlistAudit.objects.create(
        wishlist_id=wishlist_id,
        action_type=action_type,
        user=user_id,
        product_id=product_id,
        column_name=column_name,
        old_value=old_value,
        new_value=new_value

    )

@csrf_exempt
def add_to_wishlist(request):


    if request.method == 'POST':

        # get the product id from the request
        product_id = request.POST.get('p_id')
        user_id = request.user.id
        
        # check if product id is valid
        if not product_id or not product_id.isdigit():
            return JsonResponse({'message': 'Invalid product ID'})

        product = Product.objects.filter(id=product_id).first()

        if not product:
            return JsonResponse({'message': 'Product not found'})

        # check if product is already in the wishlist

        if Wishlist.objects.filter(product_id=product, user_id=user_id).exists():
            return JsonResponse({'message': 'Product already added to the wishlist'})
        else:
            # create new wishlist item

            wishlist = Wishlist.objects.create(product_id=product, user_id=user_id)
            wishlist.save()
            action = 'INSERT'
            # audit log
            create_wishlist_audit_log(wishlist.id, action, request.user, product.id , "New_Record" , "None" , "None")

            return JsonResponse({'message': 'Product added to the wishlist successfully'})

    return JsonResponse({'message': 'Invalid request method'})


@csrf_exempt
def available_products(requests):

    if requests.method == "GET":

        # get all products
        products = Product.objects.all()
        product_data = []

        # save product data in dict and append in list if quantity > 0

        for product in products:
            quantity = product.quantity
            if quantity > 0:
                id = product.id
                # get product image
                image = ProductImage.objects.get(product_id=id)
                product_dict = {
                    'product': product,
                    'image': image.image,
                    'side_image': image.side_image,
                    'back_image': image.back_image,
                    'front_image': image.front_image,
                }
                product_data.append(product_dict)
        context = {
            'product_data': product_data,
        }
        return render(requests, "shop/shop.html", context)
    else :
        
        return render(requests, "shop/404.html")


@csrf_exempt
def remove_from_wishlist(request):
    if request.method == "POST":
        # get the product id from the request
        product_id = request.POST.get('wishlist_product_id')

        # get the user id from the request
        user_id = request.user.id

        try:
            # first check if the wishlist item exists
            wishlist_item = Wishlist.objects.get(product_id=product_id, user_id=user_id)
            if wishlist_item:
                wishlist_action = 'DELETE'

                # audit log
                create_wishlist_audit_log(wishlist_item.id, wishlist_action, request.user, wishlist_item.product_id.id , "Status" , "Active" , "Deactive")
                wishlist_item.status = 'Deactive'
                wishlist_item.delete()

                # wishlist item deleted successfully
                return JsonResponse({'message': 'Product removed from the wishlist successfully'})
            else:
                return JsonResponse({'message': 'Wishlist item not found'})
            
        except Wishlist.DoesNotExist:
            return JsonResponse({'message': 'Wishlist not found'})
    else:
        return JsonResponse({'message': 'Invalid request'})

@csrf_exempt
def on_sale_products(request):
    if request.method == "GET":

        # get all products
        products = Product.objects.all()
        product_data = []

        # quanttiy > 0 then check weekly offer
        for product in products:
            quantity = product.quantity
            if quantity > 0:

                # check if product is in weekly offer
                weekly_offer = WeeklyOffers.objects.filter(product_id=product.id , status = "Active").first()
                if weekly_offer:
                    id = product.id

                    # get product image
                    image = ProductImage.objects.get(product_id=id)
                    product_dict = {
                        'product': product,
                         'price': weekly_offer.offer_price,
                        'image': image.image,
                        'side_image': image.side_image,
                        'back_image': image.back_image,
                        'front_image': image.front_image,
                    }

                    # append product data in list
                    product_data.append(product_dict)
        context = {
            'product_data': product_data,
        }
        return render(request, "shop/shop.html", context)
    else:
        return render(request, "shop/404.html")

    

def index(request):
    return render(request , "shop/clothing.html")

def logoutSession(request):
    logout(request)
    return redirect('index')


def productDetails(request , id):
    prod = Product.objects.get(id=id)

    # get product images
    product_images = ProductImage.objects.filter(product_id=id)
    context = {
        'product': prod,
        'product_images': product_images,
    }
    #
    #
   
    return render(request , "shop/product-details.html" , context)


def wishlist(request):

    if request.method == "GET":

        # get all wishlist items of the user
        user_id = request.user.id
        wishlist_items = Wishlist.objects.filter(user_id=user_id)
        wishlist_data = []

        # save wishlist data in dict and append in list
        for wishlist_item in wishlist_items:

            # get product image
            p = ProductImage.objects.get(product_id=wishlist_item.product_id.id)
            wishlist_dict = {
                
                'product_id': wishlist_item.product_id.id,
                'name': wishlist_item.product_id.product_name,
                'price': wishlist_item.product_id.price,
                'product_image': p.image,
            }
           
            
            # append wishlist data in list
            wishlist_data.append(wishlist_dict)
            
        context = {
            'wishlist_data': wishlist_data,
        }
       
        return render(request, "shop/wishlist.html" , context)
    
    return render(request , "shop/wishlist.html")



def clothing(request):
   
    product_data = []

    if request.method == "POST":

        # get the search product name from the request
        search_product = request.POST.get('search-product')

        # get all products that contain the search product name
        products = Product.objects.filter(Q(product_name__icontains=search_product))

        # save product data in dict and append in list
        for product in products:
            id = product.id

            # get product image
            productinfo = ProductImage.objects.get(product_id=id)
            product_dict = {
                'product': product,
                'image': productinfo.image,
                'side_image': productinfo.side_image,
                'back_image': productinfo.back_image,
                'front_image': productinfo.front_image,
            }
            product_data.append(product_dict)

    elif request.method == "GET": 
      
      # get  only 8 products
      products = Product.objects.all()[:8]
   

      for product in products:
        id = product.id

        # get product image
        productinfo = ProductImage.objects.get(product_id=id)
        product_dict = {
            'product': product,
            'image': productinfo.image,
            'side_image': productinfo.side_image,
            'back_image': productinfo.back_image,
            'front_image': productinfo.front_image,  

        }
        
        product_data.append(product_dict)
    context = {
        'product_data': product_data,
    }

    # get weekly offers
    weekly_offers = WeeklyOffers.objects.all()
    weekly_offers_data = []

    # save weekly offers data in dict and append in list
    for weekly_offer in weekly_offers:
        id = weekly_offer.product_id.id

        # get product image
        product = Product.objects.get(id=id)

        # get product image
        product_image = ProductImage.objects.get(product_id= product.id)
       

        # save weekly offers data in dict
        weekly_offer_dict = {
            'product': product,
            'offer_price': weekly_offer.offer_price,
            'product_image': product_image.image,
        }

        # append weekly offers data in list
        weekly_offers_data.append(weekly_offer_dict)


    return render(request, "shop/clothing.html", {'product_data': product_data, 'weekly_offers_data': weekly_offers_data})

    


def cart(request):
   
    user_id = request.user.id
   
    # get all cart items of the user
    cart_items = Cart.objects.filter(user_id=user_id , status='Active')
    cart_data = []
    
    # add cart items in list



    # save cart data in dict and append in list

    for cart_item in cart_items:

        # get product image
        p = ProductImage.objects.get(product_id=cart_item.product_id.id)

        # if product is in weekly offer then get offer price
        weekly_offer = WeeklyOffers.objects.filter(product_id=cart_item.product_id.id , status = "Active").first()
        if weekly_offer:
            price = weekly_offer.offer_price
        else:
            price = cart_item.product_id.price

        cart_dict = {
            'cart_id' : cart_item.id,
            'cart_item': cart_item,
            'product': cart_item.product_id,
            'name': cart_item.product_id.product_name,
            'price': price,
            'product_image': p.image,
        }

        # append cart data in list
        cart_data.append(cart_dict)
        
    context = {
        'cart_data': cart_data,
    }

    #return template
    return render(request, "shop/cart.html" , context)


def remove_item_view(request):

    if request.method == 'POST':

        # get the cart id from the request
        cart_id = request.POST.get('cart_id')
        try:
            # first check if the cart item exists
            user = request.user.id

            # get the cart item
            cart_item = Cart.objects.get(id=cart_id, user_id=user)
            if cart_item:
                cart_action = 'DELETE'

                # audit log
                # audit log
                create_audit_log(cart_item.id, cart_action, request.user, cart_item.product_id.id , "Deactive")

                # delete cart item
                cart_item.delete()

            else:
                # cart item not found
                return JsonResponse({'message': 'Cart item not found'})
            
            # cart item deleted successfully
            return JsonResponse({'message': 'Product removed from the cart successfully'})
        except Cart.DoesNotExist:

            # cart not found
            return JsonResponse({'message': 'Cart not found'})
    return JsonResponse({'message': 'Invalid request'})

    
def checkout(request):
    if request.method == "GET":
        # get all cart items of the user
        user = request.user.id

        # get all cart items of the user
        cart_items = Cart.objects.filter(user_id=user , status='Active')
        cart_data = []
        subtotal = 0

        # first check is avail in weekly offer if avail then get offer price
        for cart_item in cart_items:

            # get products from cart
            product = Product.objects.get(id=cart_item.product_id.id)

            # get weekly offer if avail

            weekly_offer = WeeklyOffers.objects.filter(product_id=product.id , status = "Active").first()
            if weekly_offer:
                product.price = weekly_offer.offer_price

            # save cart data in dict and append in list
            cart_dict = {
                'name': cart_item.product_id.product_name,
                'quantity': cart_item.quantity,
                'price': product.price,
                'total': cart_item.quantity * product.price,
            }

            # append cart data in list
            subtotal += cart_dict['total']
            cart_data.append(cart_dict)
        flat_rate = 20

        total = subtotal + flat_rate
       
    return render(request, "shop/checkout.html", {'cart_data': cart_data, 'subtotal': subtotal , 'flat_rate': flat_rate , 'total': total})

def order_history(request):
    if request.method == "GET":

        # get all deliveries of the user
        user = request.user.id

        # get all deliveries of the user
        deliveries = Deliveries.objects.filter(user_id=user)

        # save deliveries data in dict and append in list
        product_data = []
        total = 0
        subtotal = 0
        order_date = ""

        # get all products in each delivery
        for delivery in deliveries:

            # get all products in each delivery
            product_in_d = ProductInDelivery.objects.filter(delivery_id=delivery)

              # Initialize subtotal for each delivery
            for product_in_delivery in product_in_d:
                product = Product.objects.get(id=product_in_delivery.product.id)

                product_dict = {
                    'product': product,
                    'quantity': product_in_delivery.quantity,
                    'price': product.price,
                    'total': product_in_delivery.quantity * product.price,
                }

                subtotal += product_dict['total']
                product_data.append(product_dict)

            flat_rate = 20
        total += subtotal + flat_rate
        order_date = deliveries[0].created_at
 
        # save deliveries data in dict and append in list

        context = {
            'product_data': product_data,
            'subtotal': subtotal,
            'total': total,
            'order_date': order_date,
        }

        return render(request, "shop/order.html", context)


        
    return render(request, "shop/order.html")

def your_checkout_view(request):


    first_name = request.POST.get('first_name')
    last_name = request.POST.get('last_name')
    address = request.POST.get('address')
    city = request.POST.get('City')
    postal_code = request.POST.get('postal-code')
    phone = request.POST.get('Phone')
    email = request.POST.get('email')
    notes = request.POST.get('notes')
    user = request.user.id

    # check if all fields are filled
   
    if first_name != "" and last_name != "" and address != "" and city != "" and postal_code != "" and phone != "" and email != "":

        # check if cart is empty
        cart = Cart.objects.filter(user_id=user , status='Active')
        
        
        for cart_item in cart:

            # check if product quantity is available
            product = Product.objects.get(id=cart_item.product_id.id)
            if product.quantity < cart_item.quantity:
                return JsonResponse({'message': 'Quantity of product is not available'})
        if cart:

            # create new delivery instance
            delivery = Deliveries.objects.create(user_id=user)
            delivery_id = int(delivery.id)

        # Retrieve the Deliveries instance based on the ID
            delivery_instance = Deliveries.objects.get(id=delivery_id)
           
            for cart_item in cart:
              try:
                 
                 # create new product in delivery instance
                 product_in_delivery = ProductInDelivery.objects.create(
                   delivery_id=delivery_instance,
                     product=cart_item.product_id,
                     quantity=cart_item.quantityroduc
                    )
                 product_in_delivery.save()

              except Deliveries.DoesNotExist:
                    
                    # If the Deliveries instance does not exist, display an error message
                    print(f"Deliveries instance with ID {delivery_id} does not exist.")
              except Exception as e:
                        print(f"Error creating ProductInDelivery: {e}")
                    # minus quantity from product table
            for cart_item in cart:

                # get product
                product = Product.objects.get(id=cart_item.product_id.id)
                product.quantity = product.quantity - cart_item.quantity
                product.save()
            
            # deactive cart items
            for cart_item in cart:
                cart_item.status = 'Deactive'
                cart_item.save()

            # save shipping address
            shipping_address = ShippingAddress.objects.create(dilivery_id=delivery_instance, first_name=first_name, last_name=last_name, street_address=address, city=city, postal_code=postal_code, phone=phone, email=email, notes=notes)
            shipping_address.save()
        else:

            # cart is empty
            return JsonResponse({'message': 'Cart is empty'})
    else:
        return JsonResponse({'message': 'Please fill all the fields'})

    return JsonResponse("Your order has been placed successfully", safe=False)

def update_cart(request):
    if request.method == 'POST':

        # get the cart ids and quantities from the request
        cart_ids = request.POST.getlist('cart_ids[]', [])

        # get the quantities from the request
        quantities = request.POST.getlist('quantities[]', [])
        user = request.user.id
        for i in range(len(cart_ids)):

           # first check if the cart item exists
            cart_item = Cart.objects.get(id=cart_ids[i], user_id=user)
            if cart_item:

                # update cart item quantity
                cart_item.quantity = quantities[i]
                cart_action = 'UPDATE'

                # audit log
                create_audit_log(cart_item.id, cart_action, request.user, cart_item.product_id.id , "Active")
                cart_item.save()
            else:
                # cart item not found
                return JsonResponse({'message': 'Cart item not found'})
        return JsonResponse({'message': 'Cart updated successfully'})
      
    return JsonResponse({'message': 'Invalid request'})

def shop(request):

    # get all products
    products = Product.objects.all()
    product_data = []
    items_per_page = 3

    # Sorting
    sort_option = request.GET.get('sort', 'default')
    try:
        if sort_option == 'Low to High':
            products = products.order_by('price')
        elif sort_option == 'High to Low':
            products = products.order_by('-price')
    except:
        pass

    # Pagination
    
    paginator = Paginator(products, items_per_page)
    page = request.GET.get('page', 1)  # Default to page 1 if not specified
    try:
        product_dat = paginator.page(page)
        for product in product_dat:
            id = product.id

            # get product image
            image = ProductImage.objects.get(product_id=id)

            # save product data in dict and append in list
            product_dict = {
                'product': product,
                'image': image.image,
                'side_image': image.side_image,
                'back_image': image.back_image,
                'front_image': image.front_image,
            }

            # append product data in list
            product_data.append(product_dict)

        # 
        current_page = int(page)
        max_index = len(paginator.page_range)
        start_index = current_page - 2 if current_page >= 3 else 0
        end_index = current_page + 2 if current_page <= max_index - 3 else max_index
        page_range = paginator.page_range[start_index:end_index]

        context = {
        'product_data': product_data,
        'page_obj': paginator.page(current_page),
        'page_range': page_range,
     }  
    except PageNotAnInteger:
        return HttpResponse("Page not found")

    

    return render(request, "shop/shop.html", context)


def upload_product(request):

    if request.method == "POST":

        # get the product details from the request
        product_name = request.POST.get("product_name")
        price = request.POST.get("prices")
        quantity = request.POST.get("quantity")
        description = request.POST.get("description")
        category = request.POST.get("categories")
        image = request.FILES.get("image")
        side_image = request.FILES.get("sideimage")
        back_image = request.FILES.get("backimage")
        front_image = request.FILES.get("frontimage")
        
        # check if all fields are filled
        if image == None and side_image == None and back_image == None and front_image == None:

            # check if all fields are filled
            return HttpResponse("Please upload images")
        
        if image == None:
            return JsonResponse({'message': 'Please upload Front image'})
        

        
        # check if product already exists
        if product_name != None and price != None and quantity != None and description != None and category != None :
            categori = None

            # check if category already exists
            if ProductCategory.objects.filter(category_name=category).exists():
                categori = ProductCategory.objects.get(category_name=category)
                
            
            elif categori == None:

                # create new category
                categori = ProductCategory.objects.create(category_name=category)
                categori.save()
               
            # create new product
            publish_date =datetime.now().strftime('%Y-%m-%d')
            product = Product.objects.create(product_name=product_name, price=price, quantity=quantity,  pub_date  = publish_date ,     description=description, category_id=categori.id)
            product.save()

            # create new product image
            product_image = ProductImage.objects.create(product_id=product, image=image, side_image=side_image, back_image=back_image, front_image=front_image)
            product_image.save()
            return JsonResponse({'message': 'Product uploaded successfully'})

 
        else:
            return HttpResponse("Please fill all the fields")
    return render(request , "shop/file-upload.html")

def register(request):
    return render(request , "shop/register.html")


@csrf_exempt
def logins(request):
    if request.method == "POST":

        # get the email and password from the request
        email = request.POST.get("email")
        password = request.POST.get("tp_password")
       
        if email != "" and password != "":

            # check if user exists
            user = authenticate(username=email, password=password)
            if user is not None:
                # login user
                login(request, user)
                return redirect('index')
            else:
                return HttpResponse("User does not exist")
        return redirect('index')  
    return render(request, "shop/login.html")



def signup(request):
   if request.method == "POST": 

    # get the name , email and password from the request
    user = request.POST.get("name")
    email = request.POST.get("email")
    password = request.POST.get("tp_password")
    
    if user != "" and email != "" and password != "":
       

       # check if user already exists
       if User.objects.filter(username=user).exists():
             return HttpResponse("User already exists")
       
       # create new user
       userInfo = User.objects.create_user(user , email , password)
       userInfo.save()

       # login user
       login_url = reverse('logins')
       return HttpResponseRedirect(login_url)
       return render(request , "shop/index.html")

   else:
      render(request , "shop/signup.html")

