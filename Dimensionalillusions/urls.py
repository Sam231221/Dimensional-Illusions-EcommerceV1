
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views

#from Ehub.urls import *
from django.urls import path, include, re_path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Ehub.urls')),
    path('', include('Eblog.urls')),
    path('', include('Edashboard.urls')),

    re_path(r'^', include('Msfx.urls')),
    re_path(r'^', include('Mvfx.urls')),

    path('', include('Mgraphics.urls')),
    # url(r'^',include('Mgraphics.urls')),

    # Custom Url
    path('reset_password/', auth_views.PasswordResetView.as_view(
        template_name="PasswordReset/password_reset.html"), name="reset_password"),

    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(
        template_name="PasswordReset/password_reset_sent.html"), name="password_reset_done"),

    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name="PasswordReset/password_reset_form.html"),
         name="password_reset_confirm"),

    path('reset_password_complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name="PasswordReset/password_reset_done.html"),
         name="password_reset_complete"),
]

# for acessing media url
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


'''    
    url(r'^',include('Eblog.urls')),
    path('',include('Edashboard.urls')),   
      
    path('',include('Msfx.urls')), 
    path('',include('Mvfx.urls')), 
    path('',include('Mweb.urls')),
    path('',include('Mtemplate.urls')),   
'''
