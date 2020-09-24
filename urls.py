from django.urls import path
from .views import RegisterView, VerifyEmail, LoginView
from rest_framework_simplejwt.views import TokenRefreshView

application_name = "authentication"

urlpatterns = [
    path('register/', RegisterView.as_view(), name = "register"),
    path('email-verify/', VerifyEmail.as_view(), name = "email-verify"),
    path('login/', LoginView.as_view(), name="login"),
    path('token/refresh/', TokenRefreshView.as_view(), name = "token_refresh")
    #El path del refresh token sera usado sin que el usuario se de cuenta o se tratara de eso
]