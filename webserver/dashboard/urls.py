from django.urls import path 
from . import views 


app_name = "dashboard"

urlpatterns = [
    path('' , views.home , name='home'),
    path('signup' , views.sign_up , name="signup"),
]