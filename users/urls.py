from django.urls import path
from users import views
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('', views.UserAPIView.as_view(), name='user-info'),
    path('register/', views.UserRegisterationAPIView.as_view(), name='user-register'),
    path('login/', views.UserLoginAPIView.as_view(), name='user-login'),
    path('logout/', views.UserLogoutAPIView.as_view(), name='user-logout'),
    path('token/refresh/',TokenRefreshView.as_view(), name='token-refresh'),
]
