#decorators.py is for to take control over the pages that we wanna show to admin only and the pages that we wanna show only to the customers
#A decorator is a function that takes in another funciton as a parameter and lets us add a extra  #funcitonlity before the original function is called .It is represented by @ .
		  
from django.http import HttpResponse
from django.shortcuts import redirect

def unauthenticated_user(view_func):       #view_func refers to login function that we define in views.py which relfects the fucntions in views.py which we are passing as parameter            
	def wrapper_func(request, *args, **kwargs):  #define a new function
		if request.user.is_authenticated: #if user is authenticated  redirect to home no need to send him/her to login page
			return redirect('home')              
		else:  #if user is anonymous then return login page function.
			return view_func(request, *args, **kwargs)

	return wrapper_func   

def allowed_users(allowed_roles=[]):  #list
	def decorator(view_func):
		def wrapper_func(request, *args, **kwargs):

			group = None
			if request.user.groups.exists():# if a user is a part of a group that we define in django database
				group = request.user.groups.all()[0].name #if we were to re
				print(group)
			if group in allowed_roles: #if the username exist in the group return vivewfun else return httpresponse for non-authorized people
				return view_func(request, *args, **kwargs)
			else:
				return HttpResponse('You are not authorized to view this page')
		return wrapper_func
	return decorator

def admin_only(view_func):
	def wrapper_function(request, *args, **kwargs):
		group = None
		if request.user.groups.exists():
			group = request.user.groups.all()[0].name

		if group == 'Customers':
			return redirect('userpage')

		if group == 'Admin':
			return view_func(request, *args, **kwargs)

	return wrapper_function