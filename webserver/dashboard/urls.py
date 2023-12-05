from django.urls import path 
from . import views 


app_name = "dashboard"

urlpatterns = [
    path('' , views.home , name='home'),
    path('signup/' , views.sign_up , name="signup"),
    path('add_team/' , views.add_team , name="add_team"), 
    path('create_user/' ,views.create_user , name="create_user" ),
    path('send_mood/', views.MoodView.as_view(), name="Mood"),
    path("add_new_token/" , views.add_new_token , name="add_new_token" ),
    path("update_repo/" , views.update_repo , name="update_repo"),   
]
