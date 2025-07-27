from unittest.mock import Base
from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from login.decorators import login_required_custom
from datetime import datetime
from login.models import Userdata
from .models import Contact, Product, Cart, CartItem, Order, OrderItem, TempStatus, Delivery
from django.contrib import messages
from django.utils import timezone
  
def home(request):
    cart_quantity = 0
    
    if request.session.get("user_id"):
        user = get_object_or_404(Userdata, id=request.session.get("user_id"))
        cart, created = Cart.objects.get_or_create(user=user)
        cart_quantity = sum(item.quantity for item in CartItem.objects.filter(cart=cart))

        try:
            order = Order.objects.get(user=user)
            temp_status, created = TempStatus.objects.get_or_create(user = user)

            if order.status != temp_status.status:
                if order.status == "DELIVERED" or order.status == "ACCEPTED":
                    messages.success(request, f"Your order is {order.status.capitalize()}")
                    try:
                        if order.status == "DELIVERED":
                            order_items = OrderItem.objects.filter(order=order)
                            for item in order_items:
                                Delivery.objects.create(
                                    user=user,
                                    product=item.product,
                                    quantity=item.quantity,
                                    price=item.price,
                                    total_price=order.total_price,
                                    delivered=True,
                                    delivered_time=datetime.now()
                                )
                            order.delete()
                    except Exception: pass
                elif order.status == "REJECTED": messages.error(request, f"Your Last order is {order.status}")
                temp_status.status = order.status
                temp_status.save()

        except Order.DoesNotExist: pass
    try: products = Product.objects.filter(status='AVAILABLE')[:6]
    except Exception: products = Product.objects.filter(status='AVAILABLE')
        
    time = datetime.now().strftime("%H:%M:%S")
    return render(request, 'hotel_web/home.html', {'products': products, 'cart_quantity': cart_quantity, 'user' : user, 'time' : time})

def menu(request):
    products = Product.objects.all().order_by('status')
    user = get_object_or_404(Userdata, id=request.session.get("user_id"))
    return render(request, 'hotel_web/menu.html', {'products': products, 'user' : user,})

def booking(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        peoples = request.POST.get('peoples')
        date = request.POST.get('date')
        time = request.POST.get('time')
        table = request.POST.get('table')
        
        if not (name and email and phone and peoples):
            messages.error(request, "All Fields are required !")
            return redirect("hotelapp:home")
        
        if not date:
            date = datetime.today().date()
            time = datetime.today().time()
        
        book = Contact(name = name,
                email = email,
                phone = phone,
                peoples = peoples,
                date = date,
                time = time,
                table = table)
        book.save()
        
        messages.success(request, 'You have successfully booked a table !')
        return redirect("hotelapp:home")
    
    return render(request, 'hotel_web/home.html')

@login_required_custom
def add_to_cart(request, product_id):
    user = get_object_or_404(Userdata, id=request.session.get("user_id"))
    
    try:
        product = get_object_or_404(Product, id=product_id)
        cart, created = Cart.objects.get_or_create(user=user)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

        if not created:
            cart_item.quantity += 1
            cart_item.save()
        
        messages.success(request, "Added to cart")
        return redirect('hotelapp:home')
    
    except Exception as e:
        messages.error(request, f"Error occurred: {str(e)}")
        return redirect('hotelapp:home')

@login_required_custom
def view_cart(request):
    user = get_object_or_404(Userdata, id=request.session.get("user_id"))
    
    try:
        cart, created = Cart.objects.get_or_create(user=user)
        cart_items = CartItem.objects.filter(cart=cart)

        if request.method == 'POST':
            for item in cart_items:
                quantity = request.POST.get(f'quantity_{item.product.id}')
                
                if quantity and quantity.isdigit():
                    item.quantity = int(quantity)
                    item.save()
                    
            return redirect("hotelapp:order_detail")    
        
    except Exception as e:
        messages.error(request, f"Error occurred: {str(e)}")
        cart_items = []
    
    return render(request, 'hotel_web/cart.html', {'cart_items': cart_items, 'user': user})


@login_required_custom
def order_detail(request):
    user = get_object_or_404(Userdata, id=request.session.get("user_id"))
    
    try:
        cart, created = Cart.objects.get_or_create(user=user)
        cart_items = CartItem.objects.filter(cart=cart)
        total_price = sum(item.total_price() for item in cart_items)
    
    except Exception as e:
        messages.error(request, f"Error occurred: {str(e)}")
        cart_items = []
        total_price = 0
    
    return render(request, 'hotel_web/order.html', {'cart_items': cart_items, 'total_price': total_price, 'user': user})


@login_required_custom
def place_order(request):
    user = get_object_or_404(Userdata, id=request.session.get("user_id"))
    cart, created = Cart.objects.get_or_create(user = user)
    cart_items = CartItem.objects.filter(cart = cart)
    total_price = sum(item.total_price() for item in cart_items)
    
    if not cart_items.exists():
        return redirect('view_cart')
    
    order_item = []
    for item in cart_items:
        order_item.append(f'{item.quantity} - {item.product}')
    
    order = Order.objects.create(user = user, items = order_item, total_price = total_price, status = 'PENDING')
    order.save()
    
    for item in cart_items:
        OrderItem.objects.create(
            order = order,
            product = item.product,
            quantity = item.quantity,
            price = item.product.price
        )
    
    cart_items.delete()
    messages.info(request, "Order placed successfully!")
    return redirect('hotelapp:home')