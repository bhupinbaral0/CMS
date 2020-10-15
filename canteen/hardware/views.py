from django.shortcuts import render
from store.models import *
import serial
import time
from django.contrib.auth.models import User, auth
import datetime
from django.utils import timezone
from random import randint
# Create your views here.


def order(request):
    
    ser = serial.Serial('COM6', 9600)
    for i in range(5):
        
        if ser.isOpen():
            print(ser.name + ' is open..')
            
            username=ser.readline().decode("utf-8")
            password=ser.readline().decode("utf-8")
            
          
            username=int(username)
            password=int(password)
            
           
            
            user=auth.authenticate(username=str(username),password=str(password))

            if user is not None:
                auth.login(request,user)
                print("logged in")
                var1="1"
            else:
                print("login failed")
                var1="2"

            
            print(var1)
            ser.write(var1.encode())
            
            if var1=="1":
            
                productid=ser.readline().decode("utf-8")
                
                productid=int(productid)
                cust_id = Customer.objects.get(user=request.user)
                
                try:
                    product= Product.objects.get(id=productid)
                   
                    if product.available:
                        print("product is available")
                        print("balance",cust_id.balance)
                    
                        order, created= Order.objects.get_or_create(customer=cust_id,complete=False)
                        orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

                        
                        orderItem.date_added=timezone.now()
                        orderItem.quantity=1
                        orderItem.prepare=False
                        orderItem.deliver=False
                        

                        order.message="order from hardware device"
                        txid=int(datetime.datetime.now().timestamp())
                        order.transaction_id=txid
                        verify=randint(0,1000)
                        order.deliver=False
                        order.verification_code=verify
                        order.complete=True
                        order.date_ordered=timezone.now()

                        if product.price<=cust_id.balance:
                            order.save()
                            orderItem.save()
                            cust_id.balance-=product.price
                            cust_id.save()
                            print("sucessfully ordered")
                            var3="1"
                            ser.write(var3.encode())
                            txid=str(txid)+str(" ")
                            ser.write(str(txid).encode())
                            ser.write(str(verify).encode())
                            
                        else:
                            var3="2"
                            ser.write(var3.encode())

                        
                        
                    
                    else:
                        var3="2"
                        ser.write(var3.encode())


                except:
                    print("product doesnt exists or sending data failled")
                    var3="2"
                    ser.write(var3.encode())
                
        
                finally:
                    auth.logout(request)

    return render(request,"viewproduct.html")

