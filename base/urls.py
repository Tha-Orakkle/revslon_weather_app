from django.urls import path
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import (
    RegisterView,
    GetWeatherView,
    HistoryView,
    LandingView
)

urlpatterns = [
    path('', LandingView.as_view()),
    path('register/', RegisterView.as_view(), name='register'),
    path('token/', TokenObtainPairView.as_view(), name='token'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('weather/', GetWeatherView.as_view(), name="weather"),
    path('history/', HistoryView.as_view(), name="history"),
]