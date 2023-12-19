from itertools import product
from django.utils import timezone
from django.shortcuts import redirect, render
from deliveryApp.forms import CheckoutForm, Food_items_form
from django.contrib import messages
from deliveryApp.models import *
from django.shortcuts import get_object_or_404

# Create your views here.

def index(request):
    fooditems=food_items.objects.all()
    return render(request,'main/index.html',{'fooditems':fooditems})

def orderlist(request):
    if Order.objects.filter(user=request.user,ordered=False).exists():
        order = Order.objects.get(user=request.user,ordered=False)
        return render(request,'main/orderlist.html',{'order':order})
    return render(request,'main/orderlist.html',{'message':"Your cart is empty!"})  

def add_food_item(request):
    if request.method == 'POST':
        form = Food_items_form(request.POST,request.FILES)
        if form.is_valid():
            print("Added!!")
            form.save()
            messages.success(request,"Product added successfully !!")
            return redirect('/')
        else:
            print("Something went wrong")
            messages.info(request,"Product is not added , try again")
    else :
        form = Food_items_form()
    return render(request,'main/add_food_item.html',{'form':form})


def item_desc(request,pk):
    item = food_items.objects.get(pk=pk)
    return render(request,'main/item_desc.html',{'item':item})

def add_to_cart(request,pk):
    item = food_items.objects.get(pk=pk)
    
    order_item, created = OrderItem.objects.get_or_create(
        product = item,
        user = request.user,
        ordered = False,
    )

    order_qs = Order.objects.filter(user=request.user,ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(product__pk = pk).exists():
            order_item.quantity +=  1
            order_item.save()
            messages.info(request,"Added Quantity Item") 
            return redirect("item_desc",pk=pk)
        else:
            order.items.add(order_item)
            messages.info(request,"Item added to cart")
            return redirect("item_desc",pk=pk) 
    else :
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user,ordered_date = ordered_date)
        order.items.add(order_item)
        messages.info(request,"Item added to cart")
        return redirect("item_desc",pk=pk)

def add_item(request,pk):
    item = food_items.objects.get(pk=pk)
    
    order_item, created = OrderItem.objects.get_or_create(
        product = item,
        user = request.user,
        ordered = False,
    )

    order_qs = Order.objects.filter(user=request.user,ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(product__pk = pk).exists():
            if order_item.quantity < item.item_available_count:
                order_item.quantity +=  1
                order_item.save()
                messages.info(request,"Added Quantity Item") 
                return redirect("orderlist")
            else:
                messages.info(request,"Sorry! Item is out of stock")
                return redirect("orderlist")
        else:
            order.items.add(order_item)
            messages.info(request,"Item added to cart")
            return redirect("item_desc",pk=pk) 
    else :
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user,ordered_date = ordered_date)
        order.items.add(order_item)
        messages.info(request,"Item added to cart")
        return redirect("item_desc",pk=pk)

def remove_item(request,pk):
    item = get_object_or_404(food_items,pk=pk)
    order_qs = Order.objects.filter(
        user = request.user,
        ordered = False,
    )
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(product__pk=pk).exists():
            order_item = OrderItem.objects.filter(
                product = item,
                user = request.user,
                ordered = False,
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order_item.delete()
            messages.info(request,"Item quantity was updated")
            return redirect("orderlist")
        else:
            messages.info(request,"This item is not in your cart")
            return redirect("orderlist")
    else:
        messages.info(request,"You do not have any order!")
        return redirect("orderlist")

def checkout(request):
    if CheckoutAddress.objects.filter(user=request.user).exists():
        return render(request,'main/checkout.html',{'payment_allow':"allow"})
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        try:
            if form.is_valid():
                addressline1 = form.cleaned_data.get('addressline1')
                addressline2 = form.cleaned_data.get('addressline2')
                state = form.cleaned_data.get('state')
                zip_code = form.cleaned_data.get('zip_code')

                checkout_address = CheckoutAddress(
                    user=request.user,
                    addressline1=addressline1,
                    addressline2=addressline2,
                    state=state,
                    zip_code=zip_code
                )
                checkout_address.save()
                print("It should render the summary page")
                return render(request,'main/checkout.html',{'payment_allow':"allow"})
        except Exception as e:
            messages.warning(request,"Failed Checkout")
            return redirect('checkout')
    
    else:
        form = CheckoutForm()
        return render(request,'main/checkout.html',{'form':form})



