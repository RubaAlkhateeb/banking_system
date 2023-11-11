from django.urls import path
from .views import UserRegistrationView, ObtionUserToken

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='user-registration'),
    path('login/', ObtionUserToken.as_view(), name='user-login'),
]