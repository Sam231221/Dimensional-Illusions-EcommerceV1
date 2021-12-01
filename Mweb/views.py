from django.shortcuts import render
from Ehub.models import *
from Mweb.models import *
from django.contrib import messages
from django.http import JsonResponse,HttpResponse
import json                              # data = json.loads(request.body) 

from django.contrib.auth.decorators import login_required  #Restriciton ofp Pages (For not to display pages for anonymous user(but only logged in users))
from Ehub import *

# Create your views here.
#VFX SECTION   
def webtemplates(request):
	if request.user.is_authenticated:
			getfreewebtemplates=FreeWebTemplate.objects.all()       
			getpaidwebtemplates=PaidWebTemplate.objects.all()  

			getprofile = request.user.profile
			order, created = Order.objects.get_or_create(profile=getprofile, complete=False)
			purchase, created = PurchasedProduct.objects.get_or_create(profile=getprofile, complete=False)

	else:
			order={}
	
			getfreewebtemplates=FreeWebTemplate.objects.all()       
			getpaidwebtemplates=PaidWebTemplate.objects.all()  

	context={ 
             'order':order,
			 'getfreevfxproducts':getfreevfxproducts,
			 'getpaidvfxproducts':getpaidvfxproducts,
			 }
	return render(request, 'VFX/Electricity.html',context)

def updatepaidwebtemplates(request):
		print('Vfx(s) loaded to the API..')
		data = json.loads(request.body) # We are recieving  data(item was added) importing from json as a string and we need to parse it so for that we need .loads an we r sending back using request.body
		productName = data['productName'] 
		publisherId=data['publisherId']
		puid=data['poid']

		action = data['action']
		print('action:', action) 
		print('productName:', productName)  

		getprofile = request.user.profile

		getpaidvfxproduct=PaidVfxProduct.objects.get(name=productName)
		order, created = Order.objects.get_or_create(profile=getprofile, complete=False)
		purchase, created = PurchasedProduct.objects.get_or_create(profile=getprofile, complete=False)
		orderpaidvfxproduct, created = OrderPaidVfxProduct.objects.get_or_create(profile=getprofile, order=order, addtoDpage=purchase, product=getpaidvfxproduct,published_by=publisherId,complete=False)
	

		#INCREASING OR DECREASING QUANTITY OF ORDER ITEM
		if action == 'adpdt':
			if orderpaidvfxproduct.quantity==0:
				orderpaidvfxproduct.quantity = (orderpaidvfxproduct.quantity + 1)
			elif orderpaidvfxproduct.quantity==1:
				orderpaidvfxproduct.quantity =orderpaidvfxproduct.quantity 
		
		if action == 'rmvpdt':
			orderpaidvfxproduct.quantity = (orderpaidvfxproduct.quantity - 1)

		orderpaidvfxproduct.save()

		if orderpaidvfxproduct.quantity <=0: 
			orderpaidvfxproduct.delete()

		return JsonResponse('Item was added', safe=False)


			

