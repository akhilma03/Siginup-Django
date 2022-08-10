from django import views
from django.urls import path
from . import views

urlpatterns = [

    path ('',views.useradmin, name='admin' ),
    path ('main/',views.dashboard, name='main' ),
    path ('signnup/',views.siginn, name='signup2' ),
    path ('logout/',views.userlogout, name='ulogout' ),
    path('delete/<int:id>', views.destroy, name='distroy' ),  
    path ('update/<int:id>',views.update, name='update'),
    
    
]