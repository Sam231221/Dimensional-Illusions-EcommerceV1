from django.core import paginator
from django.db.models import Count, Q
from django.shortcuts import render, get_object_or_404,HttpResponseRedirect
from .forms import *
from .models import *

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.
def searchview(request):
		queryset = Post.postmanager.all()
		query = request.GET.get('query')
		lenquery=len(query)
		if lenquery >=3:
			getquerypost = queryset.filter(title__icontains=query,content__icontains=query) 
			count=getquerypost.count()
			print(count)
		else:
			getquerypost = Post.objects.none()
			count=getquerypost.count()
			print(count)
		context = {
			'query':query,
			'count':count,
			'queryset': getquerypost
		}
		return render(request, 'Blogs/search_results.html', context)

def bloghome(request):

	recent_posts = Post.postmanager.order_by('-publish_date')[0:3]
	category=Category.objects.all()
	all_posts = Post.postmanager.all()#it is same as all_posts= Post.objects.filter(status="published")
	paginator=Paginator(all_posts,6)#creating an instance of Paginator taking all posts and create 6 items per page
	page_var='page'
	page=request.GET.get(page_var)#get the string 
	try:
		paginate_queryset=paginator.page(page)
	except PageNotAnInteger:
		paginate_queryset=paginator.page(1)
	except EmptyPage:
		paginate_queryset=paginator.page(paginator.num_pages)      
	 
	print(paginate_queryset) 
	print(recent_posts)  
	print(category)   
   
	context={
		'recent_posts':recent_posts,
		'category':category,
		'queryset' : paginate_queryset,
		'page_var':page_var ,  
		}
	return render(request, 'Blogs/bloghome.html',context)

def post_single(request, post):
	post = get_object_or_404(Post, slug=post, status='published')
	recent_posts = Post.postmanager.order_by('-publish_date')[0:3]
	category=Category.objects.all().exclude(name="Default")
	
	def get_client_ip(request):
		x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
		if x_forwarded_for:
			ip = x_forwarded_for.split(',')[0]
		else:
			ip = request.META.get('REMOTE_ADDR')
		return ip

	ip = get_client_ip(request)
	if IpModel.objects.filter(ip=ip).exists():
			print("Ip Already exist")
			post.views.add(IpModel.objects.get(ip=ip))
	   
	else:   
			IpModel.objects.create(ip=ip)
			post.views.add(IpModel.objects.get(ip=ip))

	
	comment_form = NewCommentForm()
  #display comments whose status are true
	allcomments = post.comments.filter(status=True)
	page = request.GET.get('page', 1)#displays first page
	paginator = Paginator(allcomments, 21)#we wanna show 10 items per page.
	try:
		comments = paginator.page(page)#request for certain paginator
	except PageNotAnInteger:#when page url has not an integer value, send user to page 1
		comments = paginator.page(1)
		
	except EmptyPage: #when your page has just 2 but user types for page 10
		comments = paginator.page(paginator.num_pages)
	user_comment = None

	if request.method == 'POST':
		comment_form = NewCommentForm(request.POST)
		if comment_form.is_valid():
			getuser=request.user.profile
			user_comment = comment_form.save()
			user_comment.post = post
			user_comment.user = getuser
			print(user_comment.user)
			print(user_comment.post)
			user_comment.save()
			return HttpResponseRedirect('/blog/' + post.slug)
	else:
		comment_form = NewCommentForm()

	context={
						'post': post, 
						'recent_posts':  recent_posts,
						 'category':category,
						#'comments':  user_comment, 
       
                         #recursive tree comment display
						'comments': comments, 
      
						'comment_form': comment_form, 
      
                        #for displaying total comments
						'allcomments': allcomments,
	}    
	return render(request, 'Blogs/blogpost.html', context)

def category_post(request,cat_title):
	recent_posts = Post.postmanager.order_by('-publish_date')[0:3]
	category=Category.objects.all().exclude(name="Default")
	
	cat_post=Post.postmanager.filter(category=cat_title)
	catpost_count=Post.postmanager.filter(category=cat_title).count()
	print(cat_post)
	
	paginator=Paginator(cat_post,6)#creating an instance of Paginator taking all posts and create 6 items per page
	page_var='page'
	page=request.GET.get(page_var)#get the string 
	try:
		paginate_queryset=paginator.page(page)
	except PageNotAnInteger:
		paginate_queryset=paginator.page(1)
	except EmptyPage:
		paginate_queryset=paginator.page(paginator.num_pages)      
			
	context={
				  'recent_posts':recent_posts,
				  'category':category,
				  'cat_title':cat_title,
				  'post_count': catpost_count,
				  'cat_post':cat_post,
				  
				  'queryset' : paginate_queryset,
				  'page_var':page_var ,  
	}
	return render(request,'Blogs/category_post.html',context)

