from django.shortcuts import render
from Ehub.models import *
from Mvfx.models import *
from Msfx.models import *
from Mgraphics.models import *
from django.contrib import messages
from django.http import JsonResponse,HttpResponse
import json              

from django.contrib.auth.decorators import login_required  
from Ehub import *

# Create your views here.
#VFX SECTION   
def graphicsproducts(request):
	if request.user.is_authenticated:
			getfreegraphicsproducts=FreeGraphicsProduct.objects.all()       
			getpaidgraphicsproducts=PaidGraphicsProduct.objects.all()  

			getprofile = request.user.profile
			order, created = Order.objects.get_or_create(profile=getprofile, complete=False)
			purchase, created = PurchasedProduct.objects.get_or_create(profile=getprofile, complete=False)

	else:
			order={}
	
			getfreegraphicsproducts=FreeGraphicsProduct.objects.all()   
			getpaidgraphicsproducts=PaidGraphicsProduct.objects.all()  

		 
	context={ 
			 'order':order,
			 'getfreegraphicsproducts':getfreegraphicsproducts,
			 'getpaidgraphicsproducts':getpaidgraphicsproducts,
			 }
	return render(request, 'Graphics/landscapes.html',context)

def updatepaidgraphicsproducts(request):
		print('Graphics(s) loaded to the API..')
		data = json.loads(request.body) 
		productName = data['productName'] 
		publisherId=data['publisherId']

		action = data['action']
		print('action:', action) 
		print('productName:', productName)  

		getprofile = request.user.profile

		getpaidgraphicsproduct=PaidGraphicsProduct.objects.get(name=productName)
		order, created = Order.objects.get_or_create(profile=getprofile, complete=False)
		purchase, created = PurchasedProduct.objects.get_or_create(profile=getprofile, complete=False)
		orderpaidgraphicsproduct, created = OrderPaidGraphicsProduct.objects.get_or_create(profile=getprofile, order=order, addtoDpage=purchase, product=getpaidgraphicsproduct,published_by=publisherId,complete=False)
		print('adnajdak')
		print(orderpaidgraphicsproduct)
		if action == 'adpdt':
			if orderpaidgraphicsproduct.quantity==0:
				orderpaidgraphicsproduct.quantity = (orderpaidgraphicsproduct.quantity + 1)
			elif orderpaidgraphicsproduct.quantity==1:
				orderpaidgraphicsproduct.quantity =orderpaidgraphicsproduct.quantity 
			print(orderpaidgraphicsproduct.quantity)	
   
		if action == 'rmvpdt':
			orderpaidgraphicsproduct.quantity = (orderpaidgraphicsproduct.quantity - 1)

		orderpaidgraphicsproduct.save()

		if orderpaidgraphicsproduct.quantity <=0: 
			orderpaidgraphicsproduct.delete()
   
			print(orderpaidgraphicsproduct.quantity)	   

		return JsonResponse('Product was added', safe=False)


			

