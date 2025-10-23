from django.urls import path
from .views import (
    SignupView,
    LoginView,
    PredictView,
    HistoryView,
    UserProfileView
)

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('predict/', PredictView.as_view(), name='predict'),
    path('history/', HistoryView.as_view(), name='history'),
    path('profile/', UserProfileView.as_view(), name='profile'),
]
