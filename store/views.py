from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Order, OrderItem
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse
from django.db.models import Q  # <--- Search ke liye zaroori
import json

# --- PUBLIC PAGES ---
def index(request):
    products = Product.objects.all().order_by('-id')[:8]
    return render(request, 'index.html', {'products': products})

def products(request):
    all_products = Product.objects.all()
    return render(request, 'products.html', {'products': all_products})

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'product_detail.html', {'product': product})

def about(request): return render(request, 'about.html')
def contact(request): return render(request, 'contact.html')

# --- AUTH SYSTEM (LOGIN/SIGNUP) ---
def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            return redirect('index')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('index')

# --- USER DASHBOARD (Order History) ---
@login_required(login_url='login')
def my_orders(request):
    # Sirf us user ke orders dikhayenge jo login hai (PRIVACY)
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'my_orders.html', {'orders': orders})

@login_required
def cancel_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    if order.status in ['Pending', 'Accepted']:
        order.status = 'Cancelled'
        order.save()
        messages.warning(request, "Order Cancelled Successfully.")
    else:
        messages.error(request, "Shipped orders cannot be cancelled.")
    return redirect('my_orders')

# --- CHECKOUT SYSTEM ---
@login_required(login_url='login') # Bina login ke checkout nahi hoga
def checkout(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        address = request.POST.get('address')
        city = request.POST.get('city')
        pincode = request.POST.get('pincode')
        phone = request.POST.get('phone')
        
        order = Order.objects.create(
            user=request.user,
            full_name=full_name,
            address=address,
            city=city,
            pincode=pincode,
            phone=phone,
            total_amount=product.sale_price if product.is_sale else product.price
        )
        
        OrderItem.objects.create(
            order=order,
            product=product,
            price=product.sale_price if product.is_sale else product.price
        )
        
        return redirect('order_success', order_id=order.id)

    return render(request, 'checkout.html', {'product': product})

def order_success(request, order_id):
    # Sirf apna order success dekh sake
    order = get_object_or_404(Order, id=order_id)
    if request.user.is_authenticated and order.user != request.user:
        return redirect('index') # Dusre ka order nahi dikhega
    return render(request, 'order_success.html', {'order': order})

# --- ADMIN & TRACKING ---
@staff_member_required
def admin_print_label(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'admin_print_label.html', {'order': order})

def track_order(request):
    # Professional Timeline Logic Added
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        try:
            # Order ID ya AWB kisi se bhi search kare
            order = Order.objects.get(Q(order_id=order_id) | Q(awb_code=order_id))
            
            # Timeline Logic (Progress Bar ke liye)
            status_list = ['Pending', 'Accepted', 'Packed', 'Shipped', 'Delivered']
            current_status = order.status
            
            # Step calculate karna (e.g. Shipped hai to step=4)
            step = 0
            if current_status in status_list:
                step = status_list.index(current_status) + 1
            elif current_status == 'Cancelled':
                step = -1
                
            return render(request, 'track_order.html', {'order': order, 'step': step})
            
        except Order.DoesNotExist:
            messages.error(request, "Order ID not found. Please check and try again.")
            
    return render(request, 'track_order.html')

# --- SHIPROCKET AUTOMATIC UPDATE ---
@csrf_exempt
def shiprocket_webhook(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            # Shiprocket data fields
            awb = data.get('awb', None)
            current_status = data.get('current_status', '').lower()
            
            if awb:
                try:
                    order = Order.objects.get(awb_code=awb)
                    
                    # Status Update Logic
                    if 'shipped' in current_status:
                        order.status = 'Shipped'
                    elif 'delivered' in current_status:
                        order.status = 'Delivered'
                    elif 'cancelled' in current_status:
                        order.status = 'Cancelled'
                    
                    order.save()
                    print(f"WEBHOOK: Order {order.order_id} updated to {order.status}")
                    
                except Order.DoesNotExist:
                    print(f"WEBHOOK: Order not found for AWB {awb}")

            return JsonResponse({'status': 'success'})
        except Exception as e:
            print("Webhook Error:", e)
            return JsonResponse({'status': 'error'}, status=400)
            
    return JsonResponse({'status': 'invalid method'})