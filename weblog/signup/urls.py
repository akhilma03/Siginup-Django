from django import views
from django.urls import path
from . import views

urlpatterns = [
    path ('',views.userlogin, name= 'login' ),

    path ('signup/',views.usersignup, name= 'signup' ),
  
    path ('home/',views.home, name='home' ),
    
    path('logout/',views.userlogout,name='ilogout'),

    path('ihome/',views.ihome,name='ihome'),

    # path ('main/',views.dashboard, name='main' )

    
]