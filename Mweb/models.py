from django.db import models
from django.db.models.deletion import SET_NULL

from Ehub.models import *
from decimal  import Decimal
from django.core.validators import FileExtensionValidator,MinValueValidator,MaxValueValidator

#Create your models here.
class TemplateCategory(models.Model):
	name=models.CharField(null=True,max_length=100)
 
	def __str__(self):
		return str(self.name) 


class FreeWebTemplate(models.Model):
    name=models.CharField(null=True,max_length=100)
    category=models.ForeignKey(TemplateCategory,on_delete=models.SET_NULL
                            ,verbose_name='Product Category'
                            ,null=True) 
    publisher= models.ForeignKey(Profile,on_delete=models.CASCADE,null=True)     
    demoproduct = models.FileField(upload_to="WebTemplates/free/%y"
                                    ,help_text="An show-case/Demo video for you web template. Only .mp4 is accepted"
                                    ,validators=[FileExtensionValidator(['mp4']),]
                                    ,null=True,blank=True)
    url=models.URLField(null=True,max_length=200
                                   ,help_text='an link of the website if it exists.'
                                   ,blank=True)
    file = models.FileField(upload_to="Web templates/free/%y"
                                    ,help_text="Provide a file that contains the source code of the web template .Only .zip and .rar are accepted"
                                    ,validators=[FileExtensionValidator(['zip','rar'])]
                                    ,null=True)
    date_published=models.DateTimeField(auto_now_add=True,null=True)
    
    def __str__(self):
        return str(self.name) 

class PaidWebTemplate(models.Model):
    name=models.CharField(null=True
                        ,verbose_name='Product name'
                    ,max_length=100)
    publisher= models.ForeignKey(Profile,on_delete=models.CASCADE,null=True)    
    category=models.ForeignKey(TemplateCategory,on_delete=models.SET_NULL
                            ,verbose_name='Template Category'
                            ,null=True) 
    price = models.DecimalField(max_digits=5 #2 digits for 2 decimal places
                                ,help_text="You can set up price up to $999.99.This is the max price."
                                ,validators=[MinValueValidator(Decimal('0')),MaxValueValidator(Decimal('999.99'))]
                                ,decimal_places=2)
    setdiscount=models.ForeignKey(SetDiscount,on_delete=SET_NULL,null=True,blank=True)
    demoproduct = models.FileField(upload_to="WebTemplates/free/%y"
                                    ,help_text="An show-case/Demo video for you web template. Only .mp4 is accepted"
                                    ,validators=[FileExtensionValidator(['mp4']),]
                                    ,null=True,blank=True)
    url=models.URLField(null=True,max_length=200
                                  ,help_text='an link of the website if it exists.'
                                   ,blank=True)
    file = models.FileField(upload_to="Web templates/free/%y"
                                    ,help_text="Provide a file that contains the source code of the web template .Only .zip and .rar are accepted"
                                    ,validators=[FileExtensionValidator(['zip','rar'])]
                                    ,null=True)
    date_published=models.DateTimeField(auto_now_add=True,null=True)

    @property 
    def get_final_total(self):    
        price = float(self.price)
        if self.setdiscount:
                discount=float(self.setdiscount.discount/100)
                total=price-discount*price    
        else: 
                total=self.price
        return total            
    
    @property 
    def get_actual_total(self):    
        total=float(self.price)
        return total          

    def __str__(self):
        return str(self.name) 
	
class OrderPaidWebTemplate(models.Model):  #make more orderitem
	profile = models.ForeignKey(Profile, on_delete=models.CASCADE, blank=True, null=True)     
	product = models.ForeignKey(PaidWebTemplate, on_delete=models.SET_NULL, blank=True, null=True)  #it's gonna give you what you actually define in  def__str___.....return self.name
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
		total = self.product.get_final_total * self.quantity 
		return total           
	
