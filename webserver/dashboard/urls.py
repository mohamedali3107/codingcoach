from django.urls import path 
from . import views 


app_name = "dashboard"

urlpatterns = [
    path('' , views.home , name='home'),
    path('signup/' , views.sign_up , name="signup"),
    path('addTeam/' , views.addTeam , name="addTeam"), 
    path('createUser/' ,views.create_user , name="createUser" ),
    path('sendMood/', views.MoodView.as_view(), name="Mood"),
    path("addNewToken/" , views.addNewToken , name="addNewToken" ),
    path("updateRepo/" , views.updateRepo , name="updateRepo"),
]
