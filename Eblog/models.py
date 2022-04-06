from django.db import models
from django.utils import timezone
from Ehub.models import *
from django.urls import reverse
from django.contrib.auth.models import User
from mptt.models import MPTTModel, TreeForeignKey

from taggit.managers import TaggableManager
from ckeditor.fields import RichTextField

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return str(self.name)

class IpModel(models.Model):
    ip=models.CharField(max_length=100,null=True)
    
    def __str__(self):
        return str(self.ip)
    
class Post(models.Model):
    options=(
        ('draft','Draft'),
        ('published','Published'),
    )

   # we aint gonna show the draft post so we create a new class that can only return published posts.    
    class NewManager(models.Manager):
        def get_queryset(self):
            return super().get_queryset() .filter(status='published')   
         
    title=models.CharField(max_length=250,null=True)
    thumbnail = models.URLField(null=True)
    content = RichTextField(null=True,blank=True)
    author=models.ForeignKey(User,on_delete=models.CASCADE,related_name='blog_posts')
    slug=models.SlugField(max_length=250,unique=True)#it must be unique for date
    tags=TaggableManager()
    category = models.ManyToManyField(Category)
    publish_date=models.DateTimeField(default=timezone.now)
    views=models.ManyToManyField(IpModel,related_name="post_views",blank=True)
    featured = models.BooleanField(default=False)
    status=models.CharField(max_length=10,choices=options,default='draft')  
    previous_post = models.ForeignKey('self', related_name='previous', on_delete=models.SET_NULL, blank=True, null=True)
    next_post = models.ForeignKey('self', related_name='next', on_delete=models.SET_NULL, blank=True, null=True)    
    objects = models.Manager()
    postmanager = NewManager() 
   
    class Meta:
            ordering = ('publish_date',)#show all the post according to the publish_date    
    #ordering = ('publish_date',)
    
    #Sblog is name of app and post_single is view function
    def get_absolute_url(self):
        return reverse('Eblog:post_single',kwargs={'post':self.slug})    #get the url  of every post of view 'post_single' of EBlog app
    
    def __str__(self):
        return str(self.title)
    
    def totalviews(self):
        return self.views.count()
    
class Comment(MPTTModel):
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='comments',null=True)#Many comments to One Post
    user=models.ForeignKey(Profile,on_delete=models.CASCADE,null=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE,null=True, blank=True, related_name='children')
    content = models.TextField()
    publish = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=True)

    class Meta:
        ordering = ('publish',)

    def __str__(self):
        return 'Comment by '+str(self.user)
        #return f'Comment by {self.name}'