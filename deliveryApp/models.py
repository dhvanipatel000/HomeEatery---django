from audioop import reverse
from distutils.command.upload import upload
from re import L
from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Customer(models.Model):

    user = models.OneToOneField(User,null=False,blank=False,on_delete = models.CASCADE)

    phone_no = models.CharField(max_length = 12,blank=False)


    def __str__(self):
        return self.user.username

class Category(models.Model):
    category_name=models.CharField(max_length=100)
    def __str__(self):
        return self.category_name


class food_items(models.Model):
    name=models.CharField(max_length = 100)
    category = models.ForeignKey('Category',on_delete = models.CASCADE)
    decs=models.TextField()
    price=models.FloatField(default=0.0)
    item_available_count = models.IntegerField(default=0)
    img = models.ImageField(upload_to='images/')

    def get_add_to_cart_url(self):
        return reverse("main:add-to-cart",kwargs={
            "pk" : self.pk
        })
    def __str__(self):
        return self.name

class OrderItem(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    product = models.ForeignKey(food_items,on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.product.name}"
    def get_total_item_price(self):
        return self.quantity * self.product.price
    def get_final_price(self):
        return self.get_total_item_price()

class Order(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)
    order_id = models.CharField(max_length=100,unique=True,default=None,blank=True,null=True)
    datetime_ofpayment =  models.DateTimeField(auto_now_add=True)
    order_delivered = models.BooleanField(default=False)
    order_received = models.BooleanField(default=False)

    def save(self,*args,**kwargs):
        if self.order_id is None and self.datetime_ofpayment and self.id:
            self.order_id = self.datetime_ofpayment.strftime('PAY2ME%Y%m%dODR') + str(self.id)

        return super().save(*args,**kwargs)

    def __str__(self):
        return self.user.username

    def get_total_price(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        return total

    def get_total_count(self):
        order = Order.objects.get(pk=self.pk)
        return order.items.count()
        
class CheckoutAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    addressline1 = models.CharField(max_length=100)
    addressline2 = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=10)

    def __str__(self):
        return self.user.username