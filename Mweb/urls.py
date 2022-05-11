
from django.urls import path
from Mvfx import views

app_name='Mweb'

urlpatterns = [
    path('WEB_TEMPLATES/', views.vfxproducts, name="VfxProducts"),
    path('updatevfxproducts/', views.updatepaidvfxproducts, name="updatevfxproducts"),

]
