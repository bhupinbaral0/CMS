from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Customer(models.Model):
	user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
	name = models.CharField(max_length=200, null=True)
	balance=models.IntegerField(default=100)
	

class Product(models.Model):
	name = models.CharField(max_length=200)
	price = models.FloatField()
	available = models.BooleanField(default=False,null=False, blank=False)
	image = models.ImageField(null=True, blank=True)

class Order(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
	date_ordered = models.DateTimeField(auto_now_add=False,null=True)
	complete = models.BooleanField(default=False)
	transaction_id = models.CharField(max_length=100, null=True)
	message= models.CharField(max_length=100, null=True)
	deliver= models.BooleanField(default=False)
	verification_code = models.CharField(max_length=100,null=True)
	

	@property
	def get_cart_total(self):
		orderitems = self.orderitem_set.all()
		total = sum([item.get_total for item in orderitems])
		return total 

	@property
	def get_cart_items(self):
		orderitems = self.orderitem_set.all()
		total = sum([item.quantity for item in orderitems])
		return total 


class OrderItem(models.Model):
	product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
	order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
	quantity = models.IntegerField(default=0, null=True, blank=True)
	date_added = models.DateTimeField(auto_now_add=False, null=True)
	deliver= models.BooleanField(default=False)
	prepare= models.BooleanField(default=False)
    
	@property
	def get_total(self):
		total = self.product.price * self.quantity
		return total
