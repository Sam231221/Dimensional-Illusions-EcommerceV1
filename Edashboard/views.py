from django.shortcuts import render
from Mvfx.models import *
from Msfx.models import *
from Mgraphics.models import *
from Mweb.models import *
from Ehub.decorators import *
from django.utils import timezone

from .forms import *

from django.contrib.auth.decorators import login_required 
from django.contrib import messages

# Create your views here.
@login_required(login_url='login') 
@allowed_users(allowed_roles=['Admin','Graphics Manager'])
def dashboard(request):
    context={}
    if request.user.is_authenticated:
        getprofile=request.user

        #Render Data based on name of User    
        currentlocaltime = timezone.now()
        context={
                        'currentlocaltime':currentlocaltime,
         }          
        if getprofile.groups.filter(name="Graphics Manager").exists():

         #Orders Completed
                #count all the landscape ordered  by customers which was published by Pub Id in website.
                CountCompletedOrderedGraphicsProducts=OrderPaidGraphicsProduct.objects.filter(published_by=getprofile,complete=True).count()
                OrdersCompleted=CountCompletedOrderedGraphicsProducts
                
            #Orders Pending    
                CountInCompletedOrderedGraphicsProducts=OrderPaidGraphicsProduct.objects.filter(published_by=getprofile,complete=False).count()
                OrdersPending=CountInCompletedOrderedGraphicsProducts
                
                print(OrdersPending)
              
            #Your Orders    
                GraphicsOrders=OrderPaidGraphicsProduct.objects.filter(published_by=getprofile)
  
            #Earnings Setup
                TotalLandscapePrice=0
                for x in OrderPaidGraphicsProduct.objects.filter(published_by=getprofile,complete=True):
                    pprice=x.product.price
                    chargedprice=float(pprice)-10/100*float(pprice) #10%charge from me
                    TotalLandscapePrice=TotalLandscapePrice+chargedprice
                print(TotalLandscapePrice)      

                TotalCharacterPrice=0
                for x in OrderPaidGraphicsProduct.objects.filter(published_by=getprofile,complete=True):
                    pprice=x.product.price
                    chargedprice=float(pprice)-10/100*float(pprice) #10%charge from me
                    TotalCharacterPrice=TotalCharacterPrice+chargedprice
                print(TotalCharacterPrice)      				
                    
                MyEarnings=TotalLandscapePrice+TotalCharacterPrice
                print(MyEarnings)
                
                context = {
                    'currentlocaltime':currentlocaltime,
                    'OrdersCompleted':OrdersCompleted,
                    'OrdersPending': OrdersPending,        
                    'GraphicsOrders':GraphicsOrders,
                    'MyEarnings':MyEarnings,
                    'profile':getprofile,
                    }   
                
    else:
         context={
         }
            
    return render(request,'dashboard/dashbase.html',context)

@login_required(login_url='login') 
@allowed_users(allowed_roles=['Admin','Graphics Manager'])
def profileinfo(request,pk):
    if request.user.is_authenticated:
        currentlocaltime = timezone.now()
        
        profileinfo=Profile.objects.get(id=pk)
        profileid=profileinfo.id

        profileform=ProfileForm(instance=profileinfo)
     
        if request.method=="POST":
            profileform=ProfileForm(request.POST,request.FILES,instance=profileinfo)
            if profileform.is_valid():
                profileform.save()
                return redirect('/account/dashboard/profiledetail/'+pk)        
            
        context = {
            'profileform':profileform,
            'profileid':profileid,
            'currentlocaltime':currentlocaltime,

            }   
    
    else:
         context={}
            
    return render(request,'dashboard/profileinfo.html',context)
 
@login_required(login_url='login') 
@allowed_users(allowed_roles=['Admin']) 
def energy(request):
    if request.user.is_authenticated:
        customer=request.user.customer
        user=request.user
        currentlocaltime = timezone.now()
        #check if user falls under the graphics manager grant his products
        if user.groups.filter(name="Admin").exists():
           getenergies=EnergyVfx.objects.filter(publisher=customer)
           getelectricites=LightiningVfx.objects.filter(publisher=customer)
           context={
                          'getenergies':getenergies,
                          'getelectricites':getelectricites,
                          'currentlocaltime':currentlocaltime,
           }
    return render(request,'dashboard/energy/energy.html',context) 
 
@login_required(login_url='login') 
@allowed_users(allowed_roles=['Admin']) 
def addenergy(request):
    energyform=EnergyVfxForm()
    getpublisher=request.user.customer
    print(getpublisher)
    currentlocaltime = timezone.now()
    if request.method=="POST":
            energyform=EnergyVfxForm(request.POST,request.FILES)
            if energyform.is_valid():
                newform=energyform.save()
                newform.publisher=getpublisher
                print(newform)
                newform.save()
                return redirect('energy')

    context={
            'energyform':energyform,
            'currentlocaltime':currentlocaltime,
    }
    return render(request,'dashboard/energy/addenergy.html',context) 

@login_required(login_url='login') 
@allowed_users(allowed_roles=['Admin']) 
def updateenergy(request,pk):
    energyvfx=EnergyVfx.objects.get(id=pk)
    energyform=EnergyVfxForm(instance=energyvfx)
    currentlocaltime = timezone.now()

    if request.method=="POST":
            energyform=EnergyVfxForm(request.POST,request.FILES,instance=energyvfx)
            if energyform.is_valid():
                energyform.save()
                return redirect('energy')

    context={
            'energyform':energyform,
            'currentlocaltime':currentlocaltime,
        
    }
    return render(request,'dashboard/energy/updateenergy.html',context) 

@login_required(login_url='login') 
@allowed_users(allowed_roles=['Admin']) 
def deleteenergy(request,pk):
    energyvfx=EnergyVfx.objects.get(id=pk)
    currentlocaltime = timezone.now()
    if request.method=="POST":
       energyvfx.delete()
       return redirect('energy')
    context={
            'item':energyvfx,
            'currentlocaltime':currentlocaltime,
        
    }
    return render(request,'dashboard/energy/deleteenergy.html',context) 

#LANDSCAPE CRUD
@login_required(login_url='login') 
@allowed_users(allowed_roles=['Graphics Manager']) 
def graphics(request):
    if request.user.is_authenticated:
        currentlocaltime = timezone.now()
     #note everytime we create a user customer is also created with same name
        getprofile = request.user.profile

        getgraphics=PaidGraphicsProduct.objects.filter(publisher=getprofile)
        context={
                        'getgraphics':getgraphics,
                        'currentlocaltime':currentlocaltime,
        }	

    return render(request,'dashboard/graphics/graphics.html',context) 
 
@login_required(login_url='login') 

#check if user falls under the graphics manager grant premission to add Graphics
@allowed_users(allowed_roles=['Graphics Manager']) 
def addgraphics(request):
    graphicsform= GraphicsForm()
    getpublisher=request.user.profile
    currentlocaltime = timezone.now()
    if request.method=="POST":
            graphicsform=GraphicsForm(request.POST,request.FILES)
            if graphicsform.is_valid():
                newform=graphicsform.save()
                newform.publisher=getpublisher
                newform.save()
                graphicsform.save()
                return redirect('graphics')

    context={
            'graphicsform':graphicsform,
            'currentlocaltime':currentlocaltime,
        
    }
    return render(request,'dashboard/graphics/addgraphics.html',context) 

@login_required(login_url='login') 
@allowed_users(allowed_roles=['Graphics Manager']) 
def updategraphics(request,pk):
    graphicsproduct=PaidGraphicsProduct.objects.get(id=pk)
    graphicsform= GraphicsForm(instance=graphicsproduct)
    currentlocaltime = timezone.now()

    if request.method=="POST":
            graphicsform=GraphicsForm(request.POST,request.FILES,instance=graphicsproduct)
            if graphicsform.is_valid():
                graphicsform.save()
                return redirect('graphics')

    context={
            'graphicsform':graphicsform,
            'currentlocaltime':currentlocaltime,
        
    }
    return render(request,'dashboard/graphics/updategraphics.html',context) 

@login_required(login_url='login') 
@allowed_users(allowed_roles=['Graphics Manager']) 
def deletegraphics(request,pk):
    graphicsproduct=PaidGraphicsProduct.objects.get(id=pk)
    currentlocaltime = timezone.now()
    if request.method=="POST":
       graphicsproduct.delete()
       return redirect('graphics')
    context={
            'item':graphicsproduct,
            'currentlocaltime':currentlocaltime,
        
    }
    return render(request,'dashboard/graphics/deletegraphics.html',context)     
