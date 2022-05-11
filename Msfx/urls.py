
from django.urls import path
from Msfx import views

app_name='Msfx'

urlpatterns = [
    path('SFX/', views.sfxproducts, name="SfxProducts"),
    path('updatesfxproducts/', views.updatepaidsfxproducts, name="updatesfxproducts"),
        

]
