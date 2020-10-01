from django.shortcuts import render,redirect
from django.http import JsonResponse
from .models import *
import json
import datetime
from django.utils import timezone
from random import randint
from django.db import models

# Create your views here.
def store(request):
    cartItems=0
    if request.user.is_authenticated:
        customer=request.user.customer
        order, created= Order.objects.get_or_create(customer=customer,complete=False)
        items=order.orderitem_set.all()
        cartItems=order.get_cart_items
        products = Product.objects.all()
        balance=Customer.objects.get(user=request.user).balance   
        return render(request,"store.html",{"products":products,"cartItems":cartItems,"balance":balance})
  
    products = Product.objects.all()
    return render(request,"store.html",{"products":products,"cartItems":cartItems})

def cart(request):
    if request.user.is_authenticated:
        customer=request.user.customer
        order, created= Order.objects.get_or_create(customer=customer,complete=False)
        items=order.orderitem_set.all()
        cartItems=order.get_cart_items
        balance=Customer.objects.get(user=request.user).balance

    return render(request,"cart.html",{"items":items, "order":order,"cartItems":cartItems,"balance":balance})

def checkout(request):
    if request.user.is_authenticated:
        customer=request.user.customer
        order, created= Order.objects.get_or_create(customer=customer,complete=False)
        items=order.orderitem_set.all()
        cartItems=order.get_cart_items
        balance=Customer.objects.get(user=request.user).balance
        

    return render(request,"checkout.html",{"items":items, "order":order,"cartItems":cartItems,"balance":balance})

def updateItem(request):
    data=json.loads(request.body)
    
    productId=data["productId"]
    action=data["action"]

    print(productId)
    print(action)
    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)
    orderItem.date_added=timezone.now()
    orderItem.save()
    
    if orderItem.quantity <= 0:
	    orderItem.delete()
    return JsonResponse("item is added",safe=False)

def processOrder(request):
    print("data:",request.body)
    transaction_id = datetime.datetime.now().timestamp()
    
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer=request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        total=float(data['form']['total'])
        
        print(total,order.get_cart_total)

        if total == order.get_cart_total:
            order.complete = True
            order.message= data['form']['message']
            order.transaction_id=int(transaction_id)
            order.verification_code= randint(0,1000)
            order.date_ordered=timezone.now()

            cust=Customer.objects.get(user=request.user)
            cust.balance-=total
            cust.save()

    order.save()         
    return JsonResponse("process order",safe=False)