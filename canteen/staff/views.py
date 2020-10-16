from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth 
from django.contrib import messages
from store.models import *
from django.utils import timezone
from django.http import JsonResponse
import json
import serial
import time
from django.core.mail import send_mail
from django.conf import settings
# Create your views here.

def current_demands(request):
    if request.user.is_superuser:
        print("is super user")
        order_id=Order.objects.filter(deliver=False,complete=True)
        orderitem=OrderItem.objects.filter(order_id__in=order_id,prepare=False,deliver=False)
        product=Product.objects.all()

        class Item_details:
            id=0
            quantity=0
            date=0
            name=""

            def __init__(self, id, name):
                self.id = id
                self.quantity=int(0)
                self.name=name
        

        item_detail=[Item_details(row.id,row.name) for row in product]
        
        for item in item_detail:
            for row in orderitem:
                if row.product_id==item.id:
                    if item.quantity==0:
                         item.date=row.date_added 
                    
                    item.quantity+=row.quantity
                   

            print("name=",item.name)
            print("quantity",item.quantity)
            print("#"*20)
            
        for item in orderitem:
            item.product_id=Product.objects.get(id=item.product_id).name

        return render(request,"current_demands.html",{"orderitem":orderitem,"item_detail":item_detail})
    else:
        print("is not super user")
        return redirect("/")


def update_order_item(request):

    
    data=json.loads(request.body)
    
    orderItemId=data["order_item_id"]
    action=data["action"]

    print(orderItemId)
    print(action)
    
    orderItem= OrderItem.objects.get(id=orderItemId,prepare=False,deliver=False)
    orderItem.prepare=True
    orderItem.save()
    order=Order.objects.get(id=orderItem.order_id)

    try:
        ser = serial.Serial('COM8', 9600)
        if ser.isOpen():
            print(ser.name + ' is open.. while mark preparing')
            txid= order.transaction_id
            txid=str(",")+str(txid)
            print("txid is",txid)
            ser.write(txid.encode())
            
            
    except:
        print("Error writing on serial port com8")

    finally:
        customer_email=User.objects.get(username=Customer.objects.get(id=Order.objects.get(id=orderItem.order_id).customer_id).user).email
        try:
            subject = 'Thank you for registering to our site'
            message = ' it  means a world to us '
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [customer_email]
            send_mail( subject, message, email_from, recipient_list )
            print("mail sent to",customer_email)
        except:
            print("sending message fail")
        finally:   
            return JsonResponse("order item is updated",safe=False)   


def pending_deliver(request):
    if request.user.is_superuser:
        print("is super user")
        order_id=Order.objects.filter(deliver=False,complete=True)
        orderitem=OrderItem.objects.filter(order_id__in=order_id,prepare=True,deliver=False)
        product=Product.objects.all()
        
        for item in orderitem:
            item.product_id=Product.objects.get(id=item.product_id).name

        class Transaction:
            transaction_id=0
            verification_code=0
            message=0
            order_id=0

            def __init__(self, order_id, transaction_id, verification_code, message):
                self.transaction_id=transaction_id
                self.verification_code=verification_code
                self.message=message
                self.order_id=order_id

        transaction_list=[Transaction(item.id,item.transaction_id,item.verification_code,item.message) for item in order_id]

        for item in orderitem:
            for transaction in transaction_list:
                if transaction.order_id==item.order_id:
                    print(transaction.order_id)
                    print(transaction.message)
                    print(transaction.verification_code)
                    print(transaction.transaction_id)



        # class Item_details:
        #     id=0
        #     quantity=0
        #     date=0
        #     name=""

        #     def __init__(self, id, name):
        #         self.id = id
        #         self.quantity=int(0)
        #         self.name=name
        

        # item_detail=[Item_details(row.id,row.name) for row in product]
        
        # for item in item_detail:
        #     for row in orderitem:
        #         if row.product_id==item.id:
        #             if item.quantity==0:
        #                  item.date=row.date_added 
                    
        #             item.quantity+=row.quantity
                   

        #     print("name=",item.name)
        #     print("quantity",item.quantity)
        #     print("#"*20)
            
        return render(request,"pending_deliver.html",{"orderitem":orderitem,"transaction_list":transaction_list})
    

def order_completed(request):
    if request.user.is_superuser:
        print("is super user")
        order_id=Order.objects.filter(deliver=False,complete=True)
        orderitem=OrderItem.objects.filter(order_id__in=order_id,prepare=True,deliver=True)
        product=Product.objects.all()
        
        for item in orderitem:
            item.product_id=Product.objects.get(id=item.product_id).name

        # class Item_details:
        #     id=0
        #     quantity=0
        #     date=0
        #     name=""

        #     def __init__(self, id, name):
        #         self.id = id
        #         self.quantity=int(0)
        #         self.name=name
        

        # item_detail=[Item_details(row.id,row.name) for row in product]
        
        # for item in item_detail:
        #     for row in orderitem:
        #         if row.product_id==item.id:
        #             if item.quantity==0:
        #                  item.date=row.date_added 
                    
        #             item.quantity+=row.quantity
                   

        #     print("name=",item.name)
        #     print("quantity",item.quantity)
        #     print("#"*20)
            
        return render(request,"order_completed.html",{"orderitem":orderitem})


def update_deliver(request):

    data=json.loads(request.body)
    
    orderItemId=data["order_item_id"]
    action=data["action"]

    print(orderItemId)
    print(action)
    
    orderItem= OrderItem.objects.get(id=orderItemId,prepare=True,deliver=False)
    orderItem.deliver=True
    orderItem.save()








   
    return JsonResponse(" order item is delivered",safe=False)  

def product_details(request):
    if request.user.is_superuser:
        product=Product.objects.all()

      

        try:
            ser = serial.Serial('COM3', 9600)
            if ser.isOpen():
                print(ser.name + ' is open.. in product details')
                i=int(0)
                
                for item in product:
                    if item.available:
                        if i==0:
                            length=0
                            product_string=str("@")+str(item.id)+str(" ")+str(item.name)+str(" ")+str(item.price)+str("#")
                            i=i+1
                            
                        else:
                            product_string=str(item.id)+str(" ")+str(item.name)+str(" ")+str(item.price)+str("#")
                            i=i+1
                            
                        
                        
                        length+=len(product_string)
                                     
                        if(length>40):
                            time.sleep(14)
                            length=0
                        
                        ser.write(product_string.encode())


                       
            

        except :
            print("ERROR connecting to port")
            print("Error on sending data")
            
        finally:
            return render(request,"product_details.html",{"product":product})

def update_product_available(request):
    data=json.loads(request.body)
    
    product_id=data["product_id"]
    action=data["action"]

    product=Product.objects.get(id=product_id)

    if product.available==True:
        print(product.available)
        product.available=False
        print(product.available)
        print("changed to false")
        product.save()
    elif product.available==False:
        print(product.available)
        product.available=True
        print(product.available)
        print("changed to True")
        product.save()
    else:
        print("do nothing")
        input()







    return JsonResponse(" product status is changed",safe=False)  
