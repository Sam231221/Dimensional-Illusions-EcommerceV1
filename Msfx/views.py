from django.shortcuts import render
from Ehub.models import *
from Mvfx.models import *
from Msfx.models import *
from django.contrib import messages
from django.http import JsonResponse,HttpResponse
import json                              # data = json.loads(request.body) 

from django.contrib.auth.decorators import login_required  #Restriciton ofp Pages (For not to display pages for anonymous user(but only logged in users))
from Ehub import *

# Create your views here.
#VFX SECTION   
def sfxproducts(request):
	if request.user.is_authenticated:
			getfreesfxproducts=FreeSfxProduct.objects.all()       
			getpaidsfxproducts=PaidSfxProduct.objects.all()  

			getprofile = request.user.profile
			order, created = Order.objects.get_or_create(profile=getprofile, complete=False)
			purchase, created = PurchasedProduct.objects.get_or_create(profile=getprofile, complete=False)

	else:
			order={}
	
			getfreesfxproducts=FreeSfxProduct.objects.all()   
			getpaidsfxproducts=PaidSfxProduct.objects.all()  

		 
	context={ 
             'order':order,
			 'getfreesfxproducts':getfreesfxproducts,
			 'getpaidsfxproducts':getpaidsfxproducts,
			 }
	return render(request, 'SFX/sfxdetail.html',context)

def updatepaidsfxproducts(request):
		print('Vfx(s) loaded to the API..')
		data = json.loads(request.body) # We are recieving  data(item was added) importing from json as a string and we need to parse it so for that we need .loads an we r sending back using request.body
		productName = data['productName'] 
		publisherId=data['publisherId']


		action = data['action']
		print('action:', action) 
		print('productName:', productName)  

		getprofile = request.user.profile

		getpaidsfxproduct=PaidSfxProduct.objects.get(name=productName)
		order, created = Order.objects.get_or_create(profile=getprofile, complete=False)
		purchase, created = PurchasedProduct.objects.get_or_create(profile=getprofile, complete=False)
		orderpaidsfxproduct, created = OrderPaidSfxProduct.objects.get_or_create(profile=getprofile, order=order, addtoDpage=purchase, product=getpaidsfxproduct,published_by=publisherId,complete=False)
	
		if action == 'adpdt':
			if orderpaidsfxproduct.quantity==0:
				orderpaidsfxproduct.quantity = (orderpaidsfxproduct.quantity + 1)
			elif orderpaidsfxproduct.quantity==1:
				orderpaidsfxproduct.quantity =orderpaidsfxproduct.quantity 
		
		if action == 'rmvpdt':
			orderpaidsfxproduct.quantity = (orderpaidsfxproduct.quantity - 1)

		orderpaidsfxproduct.save()

		if orderpaidsfxproduct.quantity <=0: 
			orderpaidsfxproduct.delete()

		return JsonResponse('Product was added', safe=False)


			

