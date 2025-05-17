from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from django.contrib.auth import logout
from django.shortcuts import redirect
from .models import CartItem, OrderDetails, Product
from django.contrib.auth.decorators import login_required
from .models import Order
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model
from django.contrib import messages

# Create your views here.
def home(request):
    """Renders the homepage"""
    return render(request, 'home/index.html')

def index(request):
    return HttpResponse("Welcome to Sole Haven!")
# def cart_view(request):
#     return render(request, 'home/cart.html')
from django.shortcuts import render

# def cart_view(request):
#     # Dummy example: Get cart items from session
#     cart_items = request.session.get('cart', [])
    
#     # Calculate total price
#     total_price = sum(item['price'] * item['quantity'] for item in cart_items)

#     return render(request, 'home/cart.html', {
#         'cart_items': cart_items,
#         'total_price': total_price
#     })
from .models import Cart
# def cart_view(request):
#     cart = Cart.objects.filter(user=request.user, is_active=True).first()
#     return render(request, 'home/cart.html', {'cart': cart})
# shop/views.py

# def cart_view(request):
#     # Get the cart from the session
#     cart = request.session.get('cart', {})

#     # Get product details for each product in the cart
#     cart_items = []
#     for product_id, quantity in cart.items():
#         product = get_object_or_404(Product, id=int(product_id))
#         cart_items.append({
#             'product': product,
#             'quantity': quantity,
#             'subtotal': product.current_price * quantity,
#         })

#     # Total price of all products in the cart
#     total_price = sum(item['subtotal'] for item in cart_items)

#     # Render the cart page with the cart items
#     return render(request, 'home/cart.html', {'cart_items': cart_items, 'total_price': total_price})
from django.shortcuts import render, redirect, get_object_or_404

# def view_cart(request):
#     # Check if user is a customer (from Code 2)
#     if request.session.get('user_type') != 'customer':
#         return redirect('home')

#     cust_id = request.session.get('user_id')
#     cart_items = []
#     total_price = 0

#     # Fetch cart items from DB (modified to match Code 1's structure)
#     connection = create_connection()
#     if connection:
#         cursor = connection.cursor()
#         cursor.execute("""
#             SELECT sc.product_id, p.name, sc.quantity, p.price, (sc.quantity * p.price) as subtotal
#             FROM shopping_cart sc
#             JOIN products p ON sc.product_id = p.product_id
#             WHERE sc.cust_id = %s
#         """, (cust_id,))
        
#         # Convert SQL results into a list of dicts (like Code 1)
#         for item in cursor.fetchall():
#             cart_items.append({
#                 'product': {
#                     'id': item[0],
#                     'name': item[1],
#                     'price': item[3],
#                 },
#                 'quantity': item[2],
#                 'subtotal': item[4],
#             })
        
#         total_price = sum(item['subtotal'] for item in cart_items)
#         cursor.close()
#         connection.close()

#     # Render with the same structure as Code 1
#     return render(request, 'store/view_cart.html', {
#         'cart_items': cart_items,
#         'total_price': total_price,
#     })
from django.shortcuts import render, redirect, get_object_or_404
from .models import Cart, Product  # Import your models

# 
@login_required
def view_cart(request):
    if not request.user.is_customer:
        return redirect('home')
    
    cart_items = request.user.cart_items.select_related('product')
    total_price = sum(item.product.current_price * item.quantity for item in cart_items)
    
    return render(request, 'home/cart.html', {
        'cart_items': cart_items,
        'total_price': total_price,
    })
def logout_view(request):
    logout(request)  # Django's built-in logout
    return redirect('home')
# def checkout_view(request):
#     return render(request, 'home/checkout.html')m

from django.shortcuts import render, redirect
from .models import Product, Order

# def checkout_view(request):
#     # Get the cart from session
#     cart = request.session.get('cart', {})

#     # If the cart is empty, redirect to the luxury gallery or cart page
#     if not cart:
#         return redirect('luxury-gallery')  # or 'cart' if you have a cart view

#     # Prepare the list of cart items and calculate the total price
#     cart_items = []
#     total_price = 0
#     for product_id, quantity in cart.items():
#         try:
#             product = Product.objects.get(id=product_id)
#             subtotal = product.current_price * quantity
#             cart_items.append({
#                 'product': product,
#                 'quantity': quantity,
#                 'subtotal': subtotal
#             })
#             total_price += subtotal
#         except Product.DoesNotExist:
#             continue  # Skip any invalid product ids in the cart

#     # Prepare context for the template
#     context = {
#         'cart_items': cart_items,
#         'total_price': total_price,
#     }

#     # If the user is submitting the checkout form
#     if request.method == 'POST':
#         # Save the checkout details to the database (example: saving order data)
#         Order.objects.create(
#             user=request.user,  # Use `request.user` if the user is logged in
#             total_price=total_price
#         )

#         # Clear the cart after checkout
#         request.session['cart'] = {}

#         # Redirect to home page after checkout
#         return redirect('home')

#     # Render checkout page with the cart context
#     return render(request, 'home/checkout.html', context)
@login_required
def order_detail(request, order_id):
    try:
        order = Order.objects.get(id=order_id, user=request.user)
        order_details = order.orderdetails_set.all().select_related('product')
        
        return render(request, 'home/order_detail.html', {
            'order': order,
            'order_details': order_details
        })
        
    except Order.DoesNotExist:
        messages.error(request, "Order not found or you don't have permission")
        return redirect('order_history')
@login_required
def order_confirmation(request, order_id):
    try:
        order = Order.objects.get(id=order_id, user=request.user)
        order_details = order.orderdetails_set.all().select_related('product')
        
        return render(request, 'home/order_confirmation.html', {
            'order': order,
            'order_details': order_details
        })
        
    except Order.DoesNotExist:
        messages.error(request, "Order not found or you don't have permission")
        return redirect('order_history')
@login_required
def checkout_view(request):
    try:
        cart = Cart.objects.get(user=request.user, is_active=True)
    except Cart.DoesNotExist:
        messages.warning(request, "Your cart is empty")
        return redirect('luxury-gallery')

    cart_items = CartItem.objects.filter(cart=cart)
    if not cart_items:
        messages.warning(request, "Your cart is empty")
        return redirect('luxury-gallery')

    total_price = sum(item.product.current_price * item.quantity for item in cart_items)

    if request.method == 'POST':
        address = request.POST.get('address', '').strip()
        if not address:
            messages.error(request, "Please enter a shipping address")
            return render(request, 'home/checkout.html', {
                'cart_items': cart_items,
                'total_price': total_price
            })

        try:
            order = Order.objects.create(
                user=request.user,
                total_price=total_price,
                shipping_address=address,
                payment_status='Paid',
                order_status='Processing'
            )

            for item in cart_items:
                OrderDetails.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.product.current_price
                )

                item.product.stock -= item.quantity
                item.product.save()

            # Mark cart as inactive
            cart.is_active = False
            cart.save()

            # Optionally delete cart items
            cart_items.delete()

            messages.success(request, "Order placed successfully!")
            # return redirect('order_confirmation', order_id=order.id)
            return redirect('give_feedback', order_id=order.id)

        except Exception as e:
            messages.error(request, f"Checkout failed: {str(e)}")

    return render(request, 'home/checkout.html', {
        'cart_items': cart_items,
        'total_price': total_price
    })

# @login_required
# def order_history(request):
#     orders = Order.objects.filter(user=request.user).order_by('-date')
#     return render(request, 'shoeshop/history.html', {'orders': orders})
# @login_required
# def order_history(request):
#     orders = Order.objects.filter(user=request.user).order_by('-order_date')
#     return render(request, 'shoeshop/history.html', {'orders': orders})
# 
# views.py
def order_history(request):
        # Check if the user is authenticated
    if not request.user.is_authenticated:
        messages.error(request, "You must be logged in to view your order history.")
        return redirect('login')
    user = request.user
    orders = Order.objects.filter(user=user)
    history_data = []

    for order in orders:
        items = OrderDetails.objects.filter(order=order)
        history_data.append({
            'order': order,
            'items': items
        })

    context = {'history_data': history_data}
    return render(request, 'shoeshop/history.html', context)


# def login_view(request):
#     return render(request, 'registration/login.html')
# User = get_user_model()
# def login_view(request):
#     if request.method == 'POST':
#         form = AuthenticationForm(data=request.POST)
#         if form.is_valid():
#             username = form.cleaned_data.get('username')
#             password = form.cleaned_data.get('password')
#             user = authenticate(username=username, password=password)
#             if user is not None:
#                 login(request, user)
#                 return redirect('home')  # Redirect to home after login
#     else:
#         form = AuthenticationForm()
# #     return render(request, 'registration/login.html', {'form': form})
# def login_view(request):
#     if request.method == 'POST':
#         form = AuthenticationForm(data=request.POST)
#         if form.is_valid():
#             username = form.cleaned_data.get('username')
#             password = form.cleaned_data.get('password')
#             user = authenticate(username=username, password=password)
#             if user is not None and user.is_customer:  # Ensure it's a customer login
#                 login(request, user)
#                 return redirect('home')  # Redirect to home after login
#             else:
#                 form.add_error(None, 'Invalid credentials or not a valid customer.')  # Handle invalid login
#     else:
#         form = AuthenticationForm()
#     return render(request, 'registration/login.html', {'form': form})

# def register_view(request):
#     return render(request, 'registration/register.html')
# def register_view(request):
#     if request.method == 'POST':
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             login(request, user)  # Log the user in after registration
#             return redirect('home')  # Redirect to home or any other page after registration
#     else:
#         form = UserCreationForm()
#     return render(request, 'registration/register.html', {'form': form})
# from django.shortcuts import render, redirect
# from accounts.forms import UserRegisterForm  # ✅ Your custom form
# from django.contrib.auth import get_user_model

# User = get_user_model()

# def register_view(request):
#     if request.method == 'POST':
#         form = UserRegisterForm(request.POST)
#         if form.is_valid():
#             user = form.save(commit=False)
#             user.set_password(form.cleaned_data['password'])  # ✅ securely hash password
#             user.save()
#             return redirect('login')
#     else:
#         form = UserRegisterForm()
#     return render(request, 'registration/register.html', {'form': form})
# def register_view(request):
#     if request.method == 'POST':
#         form = UserRegisterForm(request.POST)
#         if form.is_valid():
#             user = form.save(commit=False)
#             user.set_password(form.cleaned_data['password'])  # Securely hash password
#             user.is_customer = True  # Ensure user is marked as a customer
#             user.save()
#             return redirect('login')  # Redirect to login page after registration
#     else:
#         form = UserRegisterForm()
#     return render(request, 'registration/register.html', {'form': form})



def luxury_gallery(request):
    products = Product.objects.all()  # Get all products
    return render(request, 'shoeshop/luxury_gallery.html', {'products': products})
def product_list(request):
    products = Product.objects.all()
    return render(request, 'shop/product_list.html', {'products': products})
def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'shoeshop/product_detail.html', {'product': product})

# def add_to_cart(request, product_id):
#     product = get_object_or_404(Product, id=product_id)

#     if product.stock <= 0:
#         messages.error(request, 'This product is out of stock.')
#         return redirect('product_detail', product_id=product.id)

#     cart = request.session.get('cart', {})
#     cart[str(product_id)] = cart.get(str(product_id), 0) + 1
#     request.session['cart'] = cart

#     product.stock -= 1
#     product.save()

#     messages.success(request, f'{product.name} added to cart.')
#     return redirect('product_detail', product_id=product.id)
# from .models import Cart, CartItem
# @login_required
# def add_to_cart(request, product_id):
#     product = get_object_or_404(Product, id=product_id)

#     if product.stock <= 0:
#         messages.error(request, 'This product is out of stock.')
#         return redirect('product_detail', product_id=product.id)

#     # Get or create a cart for the current user
#     cart, created = Cart.objects.get_or_create(user=request.user, is_active=True)

#     # Get or create the CartItem
#     cart_item, created = CartItem.objects.get_or_create(
#         cart=cart,
#         product=product,
#         defaults={'quantity': 1, 'price_at_add': product.current_price}
#     )

#     if not created:
#         cart_item.quantity += 1
#         cart_item.save()

#     # Optional: Reduce stock only after checkout
#     product.stock -= 1
#     product.save()

#     messages.success(request, f'{product.name} added to your cart.')
#     return redirect('product_detail', product_id=product.id)
# shop/views.py


# from .models import Product

# def add_to_cart(request, product_id):
#     product = get_object_or_404(Product, id=product_id)

#     if product.stock <= 0:
#         messages.error(request, 'This product is out of stock.')
#         return redirect('product_detail', product_id=product.id)

#     # ✅ SESSION-BASED CART STORAGE
#     cart = request.session.get('cart', {})
#     product_id = str(product_id)
#     cart[(product_id)] = cart.get((product_id), 0) + 1
#     request.session['cart'] = cart

#     # ✅ Optional: reduce stock immediately
#     product.stock -= 1
#     product.save()

#     messages.success(request, f'{product.name} added to cart.')
#     return redirect('cart')  # or redirect back to product detail
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from .models import Product, Cart

# def add_to_cart(request, product_id):
#     if request.session.get('user_type') != 'customer':
#         return redirect('home')
    
#     if request.method == 'POST':
#         product = get_object_or_404(Product, product_id=product_id)
#         quantity = int(request.POST['quantity'])
#         cust_id = request.session.get('user_id')
        
#         # Check product availability
#         if product.quantity >= quantity:
#             # Check if product already in cart
#             cart_item, created = Cart.objects.get_or_create(
#                 cust_id=cust_id,
#                 product_id=product_id,
#                 defaults={
#                     'quantity': quantity,
#                     'total_price': product.price * quantity
#                 }
#             )
            
#             if not created:
#                 # Update existing item
#                 cart_item.quantity += quantity
#                 cart_item.total_price = product.price * cart_item.quantity
#                 cart_item.save()
            
#             messages.success(request, 'Product added to cart!')
#         else:
#             messages.error(request, 'Not enough stock available.')
    
#     return redirect('view_products')
# def remove_from_cart(request, product_id):
#     if request.session.get('user_type') != 'customer':
#         return redirect('home')
    
#     if request.method == 'POST':
#         quantity = int(request.POST.get('quantity', 1))
#         cust_id = request.session.get('user_id')
#         product = get_object_or_404(Product, product_id=product_id)
        
#         try:
#             cart_item = Cart.objects.get(
#                 cust_id=cust_id,
#                 product_id=product_id
#             )
            
#             if quantity >= cart_item.quantity:
#                 # Remove entire item
#                 cart_item.delete()
#             else:
#                 # Update quantity
#                 cart_item.quantity -= quantity
#                 cart_item.total_price = product.price * cart_item.quantity
#                 cart_item.save()
            
#             messages.success(request, 'Cart updated successfully!')
#         except Cart.DoesNotExist:
#             messages.error(request, 'Item not found in cart.')
    
#     return redirect('view_cart')
# 
@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        
        # Get or create active cart for user
        cart, _ = Cart.objects.get_or_create(
            user=request.user,
            is_active=True
        )
        
        # Get or create cart item
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={
                'quantity': quantity,
                'price_at_add': product.current_price,
                'user': request.user  # If your model requires this
            }
        )
        
        if not created:
            cart_item.quantity += quantity
            cart_item.save()
        
        messages.success(request, f"Added {product.name} to cart")
        return redirect('luxury-gallery')
    
    return redirect('product_detail', product_id=product_id)
@login_required
def remove_from_cart(request, product_id):
    if not request.user.is_customer:
        return redirect('home')
    
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        
        try:
            cart_item = request.user.cart_items.get(product_id=product_id)
            if quantity >= cart_item.quantity:
                cart_item.delete()
                messages.success(request, "Item removed from cart")
            else:
                cart_item.quantity -= quantity
                cart_item.save()
                messages.success(request, "Quantity updated")
        except CartItem.DoesNotExist:
            messages.error(request, "Item not found in cart")
    
    return redirect('cart')
# from django.shortcuts import render, redirect, get_object_or_404
# from .models import Order, Feedback
# from .forms import FeedbackForm

# def give_feedback(request, order_id):
#     order = get_object_or_404(Order, id=order_id, user=request.user)
    
#     if Feedback.objects.filter(order=order).exists():
#         messages.info(request, "You’ve already given feedback for this order.")
#         return redirect('order_history')
    
#     if request.method == 'POST':
#         form = FeedbackForm(request.POST)
#         if form.is_valid():
#             feedback = form.save(commit=False)
#             feedback.user = request.user
#             feedback.order = order
#             feedback.save()
#             messages.success(request, "Thanks for your feedback!")
#             return redirect('order_confirmation', order_id=order.id)
#     else:
#         form = FeedbackForm()

#     return render(request, 'shoeshop/give_feedback.html', {'form': form, 'order': order})
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Feedback, Order
from .forms import FeedbackForm

def give_feedback(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    if Feedback.objects.filter(order=order).exists():
        messages.info(request, "You've already given feedback for this order.")
        return redirect('order_history')
    
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        print("Raw POST data:", request.POST) #debug
        if form.is_valid():
            print("Cleaned data:", form.cleaned_data) #debug
            feedback = form.save(commit=False)
            feedback.user = request.user
            feedback.order = order
            feedback.save()
            messages.success(request, "Thanks for your rating!")
            return redirect('order_confirmation', order_id=order.id)
    else:
        form = FeedbackForm()

    return render(request, 'shoeshop/give_feedback.html', {
        'form': form,
        'order': order,
        'title': 'Rate Your Product(s)'
    })