from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Add_Item(models.Model):
    item_no=models.AutoField(primary_key=True)
    name=models.CharField(max_length=(150))
    details=models.CharField(max_length=(150))
    price=models.IntegerField()
    image= models.ImageField(upload_to='Add_item/')
  
    def __str__(self):
     return self.name


class Cart(models.Model):
   user =models.ForeignKey(User,on_delete=models.CASCADE)
   created_at=models.DateTimeField(auto_now_add=True)

   def __str__(self):
      return f"Cart #{self.id}-{self.user.username}"
   
   
   def total_price(self):
      return sum(item.total_price() for item in self.items.all())

class CartItem(models.Model):
   cart=models.ForeignKey(Cart,related_name='items',on_delete=models.CASCADE)
   item=models.ForeignKey(Add_Item,on_delete=models.CASCADE)
   quantity =models.PositiveBigIntegerField(default=1)

   
   def total_price(self):
      return self.item.price *self.quantity
   

   
   def __str__(self):
     return f"{self.quantity} x {self.item.name}"

class OrderView(models.Model):
   name=models.CharField(max_length=100)
   email=models.EmailField()
   phone=models.CharField(max_length=20)
   province=models.CharField(max_length=100)
   city=models.CharField(max_length=100)
   street_area=models.CharField(max_length=100)
   district=models.CharField(max_length=100)
   Account_holder=models.CharField(max_length=100)
   Account_number=models.CharField(max_length=100)
   amount=models.DecimalField(max_digits=10,decimal_places=2)
   created_at=models.DateField(auto_now_add=True)

class Order(models.Model):
   user=models.ForeignKey(User, on_delete=models.CASCADE)
   order_date=models.DateField(auto_now_add=True)
   status=models.CharField(max_length=50, default='pending')


   def __str__(self):
      return f"Order #{self.id} by{self.user.username}"

class OrderItem(models.Model):
   order=models.ForeignKey(Order,related_name='items' ,on_delete=models.CASCADE)
   item = models.ForeignKey(Add_Item,on_delete=models.CASCADE)
   quantity= models.PositiveIntegerField(default=1)
   total = models.PositiveBigIntegerField(default=0)