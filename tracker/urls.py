from django.urls import path
from tracker import views


app_name = 'tracker'

urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('update_status/', views.user_update_status, name='status_update'),
]
