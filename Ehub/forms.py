from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django import forms  

from django.contrib.auth.models import User  #For importing User model of the django database
from .models import *

class CreateUserForm(UserCreationForm): #Newly defined CreateUserForm's gonna inherit UserCreationForm 
	class Meta:
		model = User     #User ia model in database
		fields =['username','email','password1','password2']  #write the fields exact  #field that will be shown in registration.html
  
