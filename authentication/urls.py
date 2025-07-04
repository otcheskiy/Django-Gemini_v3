from django.urls import path
from .views import RegisterView, LoginView, UserDetailView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='auth_register'),
    path('login/', LoginView.as_view(), name='auth_login'),
    path('user/<int:pk>/', UserDetailView.as_view(), name='user_detail'),
] 