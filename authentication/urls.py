from django.urls import path
from .views import SignUpView, LoginView, VerificationView

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('activate/<uidb64>/<token>', VerificationView.as_view(), name='verify'),
]