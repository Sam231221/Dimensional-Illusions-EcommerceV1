from django.urls import path
from . import views

app_name="Eblog"#it is important for get_absolute_url to get work

urlpatterns = [
    path('blog/', views.bloghome, name='blogs'),
    path('blog/search/', views.searchview, name='searchview'),
    path('blog/category/<cat_title>/', views.category_post, name='category'),
    path('blog/<slug:post>', views.post_single, name='post_single'),
]