from Edashboard import views

from django.urls import path


urlpatterns = [
    # Dashboard Section
    path('account/dashboard/', views.dashboard, name="dashboard"),

    path('account/dashboard/profiledetail/<str:pk>/',
         views.profileinfo, name="profileinfo"),

    # Energy CRUD
    path('account/dashboard/energy/', views.energy, name="energy"),
    path('account/dashboard/addenergy/', views.addenergy, name="addenergy"),
    path('account/dashboard/updateenergy/<str:pk>/update',
         views.updateenergy, name="updateenergy"),
    path('account/dashboard/energy/<str:pk>/delete/',
         views.deleteenergy, name="deleteenergy"),

    # Graphics CRUD
    path('account/dashboard/graphics/', views.graphics, name="graphics"),
    path('account/dashboard/addgraphics/',
         views.addgraphics, name="addgraphics"),
    path('account/dashboard/updategraphics/<str:pk>/update',
         views.updategraphics, name="updategraphics"),
    path('account/dashboard/graphics/<str:pk>/delete/',
         views.deletegraphics, name="deletegraphics"),

]
