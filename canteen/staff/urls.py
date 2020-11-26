from django.urls import path
from . import views

urlpatterns = [

    path('current_demands/',views.current_demands, name="current_demands"),
    path('update_order_item/',views.update_order_item, name="update_order_item"),
    path('pending_deliver/',views.pending_deliver,name="pending_deliver"),
    path('order_completed/', views.order_completed, name="order_completed"),
    path('update_deliver/',views.update_deliver,name="update_deliver"),
    path('product_details/',views.product_details,name="product_details"),
    path('update_product_available/',views.update_product_available, name="update_product_available"),
    path('predict_orders/', views.predict_orders, name="predict_orders"),
    path('update_balance/',views.update_balance, name= "update_balance"),
    ]