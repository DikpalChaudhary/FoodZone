from django.shortcuts import render,HttpResponse,redirect
from myApp.models import Add_Item,Cart,CartItem,Order,OrderView,OrderItem
import matplotlib.pyplot as plt
import io
from django.contrib import messages 
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import User



# Create your views here.
def admin_view(request):
    
    return render(request,"my_admin/base.html")
def Add_item(request):
    if request.method == "POST":
        name=request.POST.get('name')
        details=request.POST.get('details')
        price=request.POST.get('price')
        image=request.FILES.get('image')

        add=Add_Item(
        name=name,
        details=details,
        price=price,
        image=image
        )
        
        add.save()
        return redirect("home")
    return render(request,'my_admin/Add_item.html')

def menuITem(request):
    menuItem=Add_Item.objects.all()
    return render(request,"my_admin/menu.html",{"menuItem":menuItem})


def monthly_sales_chart(request):
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
              'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    sales = [1500, 2700, 1000, 2800, 3200, 3500, 
             1700, 2600, 3300, 2100, 2900, 3400]
    colors=['Red','yellow','pink','blue','orange','purple','teal']
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(months, sales, color=colors)
    ax.set_title('Monthly Sales for the Year', fontsize=16)
    ax.set_xlabel('Month', fontsize=14)
    ax.set_ylabel('Sales NPR', fontsize=14)

    for i, value in enumerate(sales):
        ax.text(i, value + 50, str(value), ha='center', fontsize=10)

    # Save plot to a bytes buffer
    buffer = io.BytesIO()
    plt.tight_layout()
    fig.savefig(buffer, format='png')
    plt.close(fig)
    buffer.seek(0)

    return HttpResponse(buffer.getvalue(), content_type='image/png')

def chart_view(request):
    labels = ['Pizza', 'MoMo', 'Burger', 'Noodels', 'Paratha', 'Fish', 'Biryani', 'Crabs', 'Samosa']
    sizes = [10, 15, 15, 10, 10, 10, 10, 10, 10]
    colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99', 'blue', 'green', 'yellow', 'red', 'teal']
    
    # Exploding only the first slice (Pizza)
    explode = [0.1] + [0] * (len(labels) - 1)

    fig, ax = plt.subplots(figsize=(6, 6))
    ax.pie(sizes, labels=labels, colors=colors, explode=explode,
           autopct='%1.1f%%', startangle=90, shadow=True)
    ax.axis('equal')  # Equal aspect ratio ensures the pie is drawn as a circle.

    buffer = io.BytesIO()
    plt.tight_layout()
    fig.savefig(buffer, format='png')
    plt.close(fig)
    buffer.seek(0)

    return HttpResponse(buffer.getvalue(), content_type='image/png')



def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()

        if not username or not password:
            messages.error(request, 'Both fields are required.')
            return render(request, 'my_admin/Admin_login.html')

        # Step 1: Check if user exists
        try:
            user_obj = User.objects.get(username=username)
        except User.DoesNotExist:
            messages.error(request, 'Username does not exist')
            return render(request, 'my_admin/Admin_login.html')

        # Step 2: Authenticate
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_superuser:
            auth_login(request, user)
            messages.success(request, f'Welcome, {user.username}!')
            return redirect('admin_home')  # ✅ ensure this URL is defined
        else:
            messages.error(request, 'Incorrect password or not an admin.')
            return render(request, 'my_admin/Admin_login.html')

    # GET request
    return render(request, 'my_admin/Admin_login.html')


# def is_admin(user):
#     return user.is_superuser

def order_list(request):
    if request.user.is_superuser:
        order=OrderItem.objects.all()
        print(order)
        return render(request,'my_admin/orderlist.html',{"order":order})

    else:
        messages.error(request,'invalid admin')
        return redirect('admin_login') 

def admin_register(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # Check password match
        if password != confirm_password:
            messages.error(request, 'Passwords do not match')
            return render(request, 'my_admin/Admin_register.html')

        # Check if username exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return render(request, 'my_admin/Admin_register.html')

        # Create superuser (only if above validations passed)
        user = User.objects.create_superuser(
            username=username,
            email=email,
            password=password
        )
        messages.success(request, "Admin registered successfully")
        return redirect('admin_login')

    # GET request
    return render(request, 'my_admin/Admin_register.html')