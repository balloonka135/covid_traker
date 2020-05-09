from django.urls import path
from tracker import views


app_name = 'tracker'

urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('user_data/', views.user_share_data, name='user_share_data'),
]
