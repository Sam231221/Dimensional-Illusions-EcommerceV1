
from django.urls import path
from Mvfx import views

app_name='Mvfx'

urlpatterns = [
    path('VFX/', views.vfxproducts, name="VfxProducts"),
    path('updatevfxproducts/', views.updatepaidvfxproducts, name="updatevfxproducts"),

]
