from django.shortcuts import render ,redirect,HttpResponse
from .models import Add_Item,Cart,CartItem,OrderView,Order,OrderItem
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import User
from django.contrib import messages 
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required

# Create your views here.


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Step 1: Check if username exists
        try:
            user_obj = User.objects.get(username=username)
        except User.DoesNotExist:
            messages.error(request, 'Username does not exist')
            return render(request, 'myApp/login.html')

        # Step 2: Check if password is correct
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Incorrect password')
            return render(request, 'myApp/login.html')

    return render(request, 'myApp/login.html')

def signup(request):
    if request.method=='POST':
        UserName=request.POST.get('UserName')
        Email=request.POST.get('Email')
        Password=request.POST.get('Password')
        confirm_password = request.POST.get('Confirm_Password')

        if Password != confirm_password:
            messages.error(request, "Passwords do not match")
            return render(request, 'myApp/signup.html')
        
        if User.objects.filter(username=UserName).exists():
            messages.error(request, "Username already exists")
            return render(request, 'myApp/signup.html')
            
        user = User.objects.create_user(username=UserName, email=Email, password=Password)
        return redirect('login') 
       
    return render(request,'myApp/signup.html')

def home(request):
    items=Add_Item.objects.all()
    return render(request,'myApp/home.html',{'items':items})


def add_to_cart(request, item_no):
    item = get_object_or_404(Add_Item, pk=item_no)
    cart, _ = Cart.objects.get_or_create(user=request.user)

    cart_item, created = CartItem.objects.get_or_create(cart=cart, item=item)

    if not created:
        cart_item.quantity += 1
    else:
        cart_item.quantity = 1
    cart_item.save()

    return redirect('view_cart')

def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    cart_item.delete()
    return redirect('view_cart')

@login_required(login_url='/')
def view_cart(request):
    if not request.user.is_authenticated:
        return redirect('login')     
    cart = Cart.objects.get(user=request.user)
    cart_items = cart.items.all()
    total_sum = cart.total_price()
    return render(request, 'myApp/Add_To_Cart.html', {
        'items': cart_items,
        'total_sum': total_sum})
def checkout(request):
    
    return redirect('checkout_cart')


def checkout_cart(request):
    cart = get_object_or_404(Cart, user=request.user)
    cart_items = cart.items.all()
    total_sum = cart.total_price()
    

    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone_number = request.POST.get("PhoneNumber")
        province = request.POST.get("province")
        city = request.POST.get("city")
        street_area = request.POST.get("streetArea")
        district = request.POST.get("district")
        account_holder = request.POST.get("accountHolder")
        account_number = request.POST.get("accountNumber")
        amount = request.POST.get("ammount")  # typo fix (see below)

        if not all([name, email, phone_number, account_holder, account_number, amount]):
            messages.error(request, "Please fill all required fields.")
            return redirect("checkout")

        OrderView.objects.create(
            name=name,
            email=email,
            phone=phone_number,
            city=city,
            street_area=street_area,
            province=province,
            district=district,
            Account_holder=account_holder,
            Account_number=account_number,
            amount=amount,
        )
        order=Order.objects.create(
            user=request.user,
            status='pending'
        )

        for cart_item in cart_items:
            OrderItem.objects.create(
                order=order,
                item=cart_item.item,
                quantity=cart_item.quantity,
                total=cart_item.total_price()
            )
        cart.items.all().delete()

        messages.success(request, "Order submitted successfully.")
        return redirect("home")
       
    return render(request, 'myApp/Checkout.html', {
        'items': cart_items,
        'total_sum': total_sum
    })
