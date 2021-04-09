

from django.contrib.auth import logout
from django.urls import path
from django.urls.conf import include
from .import views
urlpatterns = [
    path('',views.index,name='home'),
    path('register',views.register,name='register'),
    path('login',views.login_user,name='login'),
    path('logout',views.logout_user,name='logout'),
    path('create_post/',views.create_blog,name='create'),
    path('detail/<int:id>',views.blog_details,name='detail'),

    path('update/<int:id>',views.update_article,name='update'),
    path('delete/<int:id>',views.delete,name='delete'),
    

]
