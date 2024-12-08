from django.shortcuts import get_object_or_404, redirect, render
from .models import Orders, Product, Contact,Category, Review
from math import ceil
from django.contrib.auth.models import User 
from django.http import JsonResponse
# Create your views here.
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login, authenticate,logout
from django.contrib import messages
import tkinter as tk
from django.db.models import Avg, Count  # Import Avg and Coun
from tkinter import messagebox
from django.db.models import Q
from django.http import HttpResponseRedirect 
from shop import models

from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
import time
def custom_login_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            # messages.success(request, "Login First!")  # Display the message
            # We add a slight delay before redirecting using a redirect with delay
            return redirect('login')  # Pass delay in URL
        return view_func(request, *args, **kwargs)
    return wrapper
def register(request):
    if request.method == 'POST':    
        uname = request.POST.get('username')
        email = request.POST.get('email')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')

        # Check if username already exists
        if User.objects.filter(username=uname).exists():
            messages.error(request, 'Username already exists!')
            return render(request, 'shop/relo.html')

        # Check if email already exists
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered!')
            return render(request, 'shop/relo.html')

        # Check if passwords match
        if pass1 != pass2:
            messages.error(request, 'Your password and confirm password do not match!')
            return render(request, 'shop/relo.html')

        # Validate password using Django's built-in validator
        try:
            validate_password(pass1)
        except ValidationError as e:
            for error in e:
                messages.error(request, error)  # Display each validation error
            return render(request, 'shop/relo.html')

        # Create user and login
        my_user = User.objects.create_user(uname, email, pass1)
        my_user.save()
        messages.success(request, 'Account created successfully!')
        auth_login(request, my_user)  # Logs the user in
        return redirect('ShopHome')

    return render(request, 'shop/relo.html')


def login(request):
    if request.method == 'POST':
        username = request.POST.get('email')  # Assuming 'Email' is the field name in your form
        password = request.POST.get('password')  # Corrected to match the form field name
        print(username, password)

        # Attempt to authenticate the user
        user = authenticate(request, username=username, password=password)

        # If the user is authenticated successfully
        if user is not None:
            auth_login(request, user)  # Log the user in
            messages.success(request, "You are now logged in!")
            return redirect('ShopHome')  # Redirect to the home page after successful login
        else:
            # If authentication fails, show an error message
            messages.error(request, "Username or password is incorrect. Please try again.")
            return redirect('login')  # Stay on the login page to allow retry

    # Render the login page if it's a GET request
    return render(request, 'shop/relo.html')
@custom_login_required
def user_logout(request):
    
    logout(request)
    
    messages.success(request, "Logout SuccessFully.")
    return redirect('ShopHome')  # Redirect to the homepage or login page
def index(request):
    categories = Category.objects.all()
    products = Product.objects.all()
    # all_category_product = Product.filter()
    category_product = {}
    for category in categories:
        category_product[category.Category_name] = products.filter(category=category)
        # from django.contrib import messages
    # messages.success(request,        "Your message here")

    params = {'category_product': category_product}
    return render(request, 'shop/index.html', params)
def about(request):
    return render(request, 'shop/about.html')

@custom_login_required
def contact(request):
    if request.method == "POST":
        print(request)
        name = request.POST.get('name','')
        email = request.POST.get('email','')
        phone = request.POST.get('phone','')
        desc = request.POST.get('desc','')
        print(name,email,phone,desc)

        contact = Contact(name=name,email=email,phone=phone,desc=desc)
        contact.save()
        messages.success(request, "Contact Send Successfully!")
            
        return redirect('ShopHome')
    return render(request, 'shop/contact.html')


def tracker(request):
    return render(request, 'shop/tracker.html')

def search_api(request):
    query = request.GET.get('q', '').strip()
    if query:
        results = Product.objects.filter(
            product_name__icontains=query  # Change 'description' to 'product_name' or 'desc'
        ).values('id', 'product_name', 'desc', 'price', 'image')  # Include valid fields
    else:
        results = Product.objects.none()

    response_data = {
        'results': list(results)
    }
    return JsonResponse(response_data)
def search(request):
    query = request.GET.get('query', '').strip()
    products = []

    if query:
        # Search in product_name, desc, and related category name
        products = Product.objects.filter(
            Q(product_name__icontains=query) |
            Q(desc__icontains=query) |
            Q(category__Category_name__icontains=query)  # Corrected this line
        ).distinct()

    context = {
        'products': products,
        'query': query
    }
    return render(request, 'shop/search.html', context)

from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Product, Review
def products(request, myid):
    # Get the product
    product = get_object_or_404(Product, id=myid)

    # Query all reviews for this product
    reviews = Review.objects.filter(product=product)

    # Calculate total reviews and average rating
    total_reviews = reviews.count()
    average_rating = reviews.aggregate(Avg('rating'))['rating__avg'] or 0

    # Calculate the percentage for each rating (1 to 5 stars)
    rating_counts = (
        reviews.values('rating')
        .annotate(count=Count('rating'))
        .order_by('-rating')
    )

    # Create a list of tuples for rating counts and percentages
    rating_counts_list = [(i, {'count': 0, 'percentage': 0}) for i in range(1, 6)]  # Initialize all ratings to 0

    for entry in rating_counts:
        rating = entry['rating']
        count = entry['count']
        percentage = (count / total_reviews) * 100 if total_reviews > 0 else 0
        rating_counts_list[rating - 1] = (rating, {'count': count, 'percentage': percentage})

    if request.method == "POST":
        # Handle form submission manually
        title = request.POST.get('title')
        comment = request.POST.get('comment')
        rating = request.POST.get('rating')

        if title and comment and rating:
            # Check if the user has already submitted a review for this product
            existing_review = Review.objects.filter(product=product, user=request.user).first()

            if existing_review:
                # Update the existing review
                existing_review.title = title
                existing_review.comment = comment
                existing_review.rating = int(rating)
                existing_review.save()
                messages.success(request, "Your review has been updated!")
                return redirect('Products', myid=product.id)
                
            else:
                # Create a new review if not already submitted
                Review.objects.create(
                    product=product,
                    user=request.user,  # Assuming the user is logged in
                    rating=int(rating),
                    title=title,
                    comment=comment,
                )
                messages.success(request, "Your review has been submitted!")

            return redirect('Products', myid=product.id)
        else:
            messages.error(request, "Please fill in all fields.")

    # Context for the template
    context = {
        'product': product,
        'reviews': reviews,
        'total_reviews': total_reviews,
        'average_rating': average_rating,
        'rating_counts': rating_counts_list,
        'rating_range': range(1, 6)  # Passing range to the template
    }

    return render(request, 'shop/prodView.html', context)

def allproducts(request):
    products = Product.objects.all()
    return render(request, 'shop/allprods.html',{'products':products})

@custom_login_required
def checkout(request):
    if 'cart' not in request.session or not request.session['cart']:
        # If the cart is empty, display an error message and redirect to the home page
        print("ERROR: Cart is empty or not found in session!")
        messages.error(request, "Your cart is empty. Add items to the cart before proceeding to checkout.")
        return redirect('ShopHome')  # Redirect to the homepage if the cart is empty
    cart = request.session['cart']
    product_details = []
    total_price = 0
    for item_id, quantity in cart.items():
        product = get_object_or_404(Product, id=item_id)
        product_total = product.price * quantity
        total_price += product_total

        product_details.append({
            'product_id': product.id,
            'product_name': product.product_name,
            'quantity': quantity,
            'price':f"RS: {product.price}",
            'total':f"RS: {product_total}",
        })
    product_details.append(total_price) 
    print(product_details)
    if request.method == 'POST':  
        fname = request.POST.get('fname','')
        lname = request.POST.get('lname','')
        cn = request.POST.get('fname','')
        houseadd = request.POST.get('houseadd','')
        apartment = request.POST.get('apartment','')
        city = request.POST.get('city','')
        state = request.POST.get('state','')
        zip = request.POST.get('zip','')
        phone = request.POST.get('fname','')
        email = request.POST.get('email','')
        orders = Orders(price=f"RS: {total_price}",products = product_details ,user=request.user,fname=fname,lname=lname,cn=cn,houseadd=houseadd,apartment=apartment,city=city,state=state,zip=zip,phone=phone,email=email)
        orders.save()
        messages.success(request, "Order placed successfully!Track your order in your Profile's Order History!")
        
        return redirect('ShopHome')
    product = []
    total_price = 0
    for item_id,quantity in cart.items():
        product1 = get_object_or_404(Product,id=item_id)
 
        product_total = product1.price * quantity
        total_price = total_price + product_total

        product.append({
            'product': product,
            'quantity': quantity, 
            'total': product_total 
        })
    quantity1 = len(cart)
    context = {
        'products': products,
        'total_price': total_price,
        'quantity1': quantity1,
        'shipping': 'Free shipping' if total_price > 50 else 'Standard shipping'
    }

    return render(request, 'shop/checkout.html',context)

def cart(request):
    if request.method == 'POST' :
        product_id = request.POST.get('product_id', '')
        action = request.POST.get('action', '') 
        quantity = int(request.POST.get('quantity', 1))
        product_id_remove = request.POST.get('product_id_remove', '') 
        # Check if the cart exists in the session
        print(product_id_remove )
        if 'cart' not in request.session:
            request.session['cart'] = {}

        cart = request.session['cart']

        if action == "add":
            messages.success(request, "Added SuccessFully")
            cart[product_id] = cart.get(product_id, 0) + 1

        elif action == "increase":
            messages.success(request, "Increased SuccessFully")
           
            cart[product_id] = cart.get(product_id, 0) + 1

        elif action == "decrease":
            messages.success(request, "Decreased SuccessFully")
            if cart.get(product_id, 0) > 1:
                cart[product_id] -= 1
        if product_id_remove:
    # Remove the product from the cart if it exists
            cart.pop(product_id_remove, None)  # `None` ensures no error if the key does not exist
            
            messages.success(request, "Remmoved SuccessFully")
            return redirect('ShopHome')
    # Save the updated cart to the session
            # request.session['cart'] = cart
        request.session['cart'] = cart
        print(f"Cart updated: {cart}") 

    cart_items = []
    for product_id, quantity in request.session.get('cart', {}).items():
        product = get_object_or_404(Product, id=product_id)
        item_total = product.price * quantity
        cart_items.append({
            'id': product.id,
            'name': product.product_name,
            'image_url': product.image.url,
            'price': product.price,
            'quantity': quantity,
            'total': item_total,
        })

    total_price = sum(item['total'] for item in cart_items)
    shipping_cost = 5.00
    grand_total = total_price + shipping_cost

    return render(request, 'shop/cart.html', {
        'cart_items': cart_items,
        'total_price': total_price,
        'shipping_cost': shipping_cost,
        'grand_total': grand_total
    })
def favorites_storage(request):
   if request.method == 'POST':
    product_id = request.POST.get('product_id')
    favorites = request.session.get('favorites', [])
    if product_id not in favorites:
        favorites.append(product_id)  # Add product ID to the list
    request.session['favorites'] = favorites
    print(request.session['favorites'])

    print("Favorites:", request.session['favorites'])
    return redirect('favorites')
def favorites(request):
    # Retrieve the list of favorite product IDs from the session
    favorite_ids = request.session.get('favorites', [])

    if favorite_ids:
        products = Product.objects.filter(id__in=favorite_ids)
    else:
        products = [] 

    return render(request, 'shop/favorites.html', {'favorites': products})

def user_orders(request):
    if request.user.is_authenticated:
        # Fetch all orders for the logged-in user
        user_orders = Orders.objects.filter(user=request.user)

        # Categorize orders by status
        pending_orders = user_orders.filter(status="Pending")
        shipped_orders = user_orders.filter(status="Shipped")
        delivered_orders = user_orders.filter(status="Delivered")

        context = {
            'pending_orders': pending_orders,
            'shipped_orders': shipped_orders,
            'delivered_orders': delivered_orders,
            'user_orders': user_orders,  # Optional: All orders in one list
        }
        print(user_orders)
        return render(request, 'shop/allorders.html', context)
    else:
        # Redirect to login page if user is not authenticated
        return redirect('login')