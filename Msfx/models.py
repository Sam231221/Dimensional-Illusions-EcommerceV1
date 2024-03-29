from django.db import models
from django.db.models.deletion import SET_NULL
from Ehub.models import *
from decimal  import Decimal
from django.core.validators import MinValueValidator,MaxValueValidator

#Create your models here.

class SfxCategory(models.Model):
	name=models.CharField(null=True,max_length=100)
 
	def __str__(self):
		return str(self.name) 


class FreeSfxProduct(models.Model):
	name=models.CharField(null=True,max_length=100)
	category=models.ForeignKey(SfxCategory,on_delete=models.SET_NULL
							   ,verbose_name='Product Category'
							   ,null=True) 
	publisher= models.ForeignKey(Profile,on_delete=models.CASCADE,null=True)     
	watermarkfreeproduct = models.URLField(null=True)
	date_published=models.DateTimeField(auto_now_add=True,null=True)
	
	def __str__(self):
		return str(self.name) 

class PaidSfxProduct(models.Model):
	name=models.CharField(null=True
						,verbose_name='Product name'
					   ,max_length=100)
	publisher= models.ForeignKey(Profile,on_delete=models.CASCADE,null=True)    
	category=models.ForeignKey(SfxCategory,on_delete=models.SET_NULL
							   ,verbose_name='Sfx Category'
							   ,null=True) 
	price = models.DecimalField(max_digits=5 #2 digits for 2 decimal places
                             	,help_text="You can set up price up to $999.99.This is the max price."
								,validators=[MinValueValidator(Decimal('0')),MaxValueValidator(Decimal('999.99'))]
								,decimal_places=2)
	setdiscount=models.ForeignKey(SetDiscount,on_delete=SET_NULL,null=True,blank=True)
	watermarkproduct = models.URLField(null=True)
	watermarkfreeproduct = models.URLField(null=True)
	date_published=models.DateTimeField(auto_now_add=True,null=True)
 
	@property 
	def get_final_total(self):    
		price = float(self.price)
		if not self.setdiscount:
				return self.price
		discount=float(self.setdiscount.discount/100)
		return  price-discount*price
		 		             
	 
	@property 
	def get_actual_total(self):    
		return float(self.price)         

	def __str__(self):
		return str(self.name) 
	
class OrderPaidSfxProduct(models.Model):  #make more orderitem
	profile = models.ForeignKey(Profile, on_delete=models.CASCADE, blank=True, null=True)     
	product = models.ForeignKey(PaidSfxProduct, on_delete=models.SET_NULL, blank=True, null=True)  #it's gonna give you what you actually define in  def__str___.....return self.name
	order = models.ForeignKey(Order, on_delete=models.CASCADE, blank=True, null=True)
	addtoDpage = models.ForeignKey(PurchasedProduct, on_delete=models.CASCADE, blank=True, null=True)
	quantity = models.IntegerField(default=0, null=True, blank=True)
	complete = models.BooleanField(default=False, null=True, blank=False)  #default is false which means unchecked box
	date_ordered = models.DateTimeField(auto_now_add=True,null=True)
	published_by=models.CharField(null=True,max_length=20)
	
	def __str__(self):
		return str(self.product)

	@property 
	def get_total(self):      
		return self.product.get_final_total * self.quantity         
	
