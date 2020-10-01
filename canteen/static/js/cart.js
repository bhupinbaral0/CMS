var updateBtns = document.getElementsByClassName('update-cart')

for (i = 0; i < updateBtns.length; i++) {
	updateBtns[i].addEventListener('click', function(){
		var productId = this.dataset.product
		var action = this.dataset.action
		console.log('productId:', productId, 'Action:', action)
		console.log('USER:', user)

		if (user == 'AnonymousUser'){
			console.log(" unknown user")
		}else{
			updateUserOrder(productId, action)
		}
	})
}

function updateUserOrder(productId, action){
	console.log('User is authenticated, sending data...')

		var url = '/update_item/'

		fetch(url, {
			method:'POST',
			headers:{
				'Content-Type':'application/json',
				'X-CSRFToken':csrftoken,
			}, 
			body:JSON.stringify({'productId':productId, 'action':action})
		})
		.then((response) => {
		   return response.json();
		})
		.then((data) => {
			
		    location.reload()
		});
}



var updateButtons = document.getElementsByClassName('item-prepare')

for (i = 0; i < updateButtons.length; i++) {
	updateButtons[i].addEventListener('click', function(){
		var order_item_id = this.dataset.id
		var action = this.dataset.action
		console.log('OrderItemID:', order_item_id, 'Action:', action)
		

		
		var url = '/staff/update_order_item/'

		fetch(url, {
			method:'POST',
			headers:{
				'Content-Type':'application/json',
				'X-CSRFToken':csrftoken,
			}, 
			body:JSON.stringify({'order_item_id':order_item_id, 'action':action})
		})
		.then((response) => {
		   return response.json();
		})
		.then((data) => {
			
		    location.reload()
		});
	
	})
}





var deliverButton = document.getElementsByClassName('item-deliver')

for (i = 0; i < deliverButton.length; i++) {
	deliverButton[i].addEventListener('click', function(){
		var order_item_id = this.dataset.id
		var action = this.dataset.action
		console.log('OrderItemID:', order_item_id, 'Action:', action)
		

		
		var url = '/staff/update_deliver/'

		fetch(url, {
			method:'POST',
			headers:{
				'Content-Type':'application/json',
				'X-CSRFToken':csrftoken,
			}, 
			body:JSON.stringify({'order_item_id':order_item_id, 'action':action})
		})
		.then((response) => {
		   return response.json();
		})
		.then((data) => {
			
		    location.reload()
		});
	
	})
}



var productButton = document.getElementsByClassName('product-available')

for (i = 0; i < productButton.length; i++) {
	productButton[i].addEventListener('click', function(){
		var product_id = this.dataset.id
		var action = this.dataset.action
		console.log('ProductID:', product_id, 'Action:', action)
		

		
		var url = '/staff/update_product_available/'

		fetch(url, {
			method:'POST',
			headers:{
				'Content-Type':'application/json',
				'X-CSRFToken':csrftoken,
			}, 
			body:JSON.stringify({'product_id':product_id, 'action':action})
		})
		.then((response) => {
		   return response.json();
		})
		.then((data) => {
			
		    location.reload()
		});
	
	})
}