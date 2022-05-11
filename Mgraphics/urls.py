
from django.urls import path
from Mgraphics import views

app_name='Mgraphics'

urlpatterns = [
    path('Graphics/', views.graphicsproducts, name="GraphicsProducts"),
    path('updategraphicsproducts/', views.updatepaidgraphicsproducts, name="updategraphicsproducts"),
        

]
