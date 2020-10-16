from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth 
from django.contrib import messages
from store.models import Customer,Order,OrderItem
from plyer import notification
# Create your views here.

def login(request):
    if request.method == 'POST':
        username= request.POST['username']
        password= request.POST['password']
        
        user=auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            return redirect("/")
        else:
            messages.info(request,"Either username or passsord is wrong")
            return redirect("login")
    else:
        return render(request,"login.html")

def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name=request.POST['last_name']
        username=request.POST['username']
        email=request.POST['email']
        password1=request.POST['password1']
        password2=request.POST['password2']

        if(password1==password2):
            if User.objects.filter(username=username).exists():
                messages.info(request,"Username already exists")
                return redirect("register")
            elif User.objects.filter(email=email).exists():
                messages.info(request,"email already exists")
                return redirect("register")
            else:
                user=User.objects.create_user(username=username,email=email,password=password1,first_name=first_name,last_name=last_name)
                user.save()
                print("user created")
                return redirect("/")
        else:
            messages.info(request,"Password didnt matched")
            return redirect("register")

    else:
        return render(request,"register.html")



def logout(request):
    auth.logout(request)
    return redirect("/")

def profile(request):
    cust_id = Customer.objects.get(user=request.user)
    balance =cust_id.balance
   
    remaining_orders=Order.objects.filter(customer_id=cust_id,complete=True,deliver=False)
    remaining_orderitems=OrderItem.objects.filter(order_id__in=remaining_orders,deliver=False)

    completed_orders=Order.objects.filter(customer_id=cust_id,complete=True)
    completed_orderitems=OrderItem.objects.filter(order_id__in=completed_orders,deliver=True)

    if OrderItem.objects.filter(order_id__in=remaining_orders,deliver=False,prepare=True):
        notification.notify(
            title="item prepared",
            message="your notification message here",
            timeout=10
        )



    return render(request,"profile.html",{"remaining_orderitems":remaining_orderitems,"completed_orderitems":completed_orderitems,"balance":balance,"orders":remaining_orders})

