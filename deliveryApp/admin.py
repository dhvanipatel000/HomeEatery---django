from django.contrib import admin
from deliveryApp.models import *
# Register your models here.
admin.site.register(Customer)
admin.site.register(Category)
admin.site.register(food_items)
admin.site.register(Order)
admin.site.register(OrderItem)
