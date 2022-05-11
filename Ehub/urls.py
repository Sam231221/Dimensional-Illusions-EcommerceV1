from django.contrib import admin
from django.urls import path
from Ehub import views
from .views import *

app_name='Ehub'

urlpatterns = [
    path('', views.Home, name="home"),

    #Authetication 
    path('account/register/' , registeruser , name="register"),
    path('account/login/' , loginuser, name="login-user"),
    path('account/logout/',views.logoutUser, name="logout-user"),
    path('account/token/' , token_send , name="token_send"),
    path('account/success/' , success , name='success'),
    path('account/verify/<auth_token>' , verify , name="verify"),
    path('account/error/' , error_page , name="error"),

    path('search/', views.SearchEngine, name="search"),
    path('Contact_Us/', views.ContactApi, name="Contact_Us"),
    
    path('downloadpage/', views.PurchasedProducts, name="download"),

    path('user-cart/', views.YourCart, name="YourCart"),
    path('Checkout/', views.Checkout, name="Checkout"),
    path('Checkout/Add_Coupon/', views.addcouponcode, name="AddCoupon"),    
    path("khalti-verify/", KhaltiVerifyView.as_view(), name="khaltiverify"),    
    
    path('process_order/', views.ProcessOrder, name="process_order"),    
        


]

