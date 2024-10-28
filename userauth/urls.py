from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('<int:pk>',views.UserDetailApiView.as_view(), name='user'),
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('reset_password/<str:encoded_pk>/<str:token>/', views.reset_password, name='reset_password'),
]