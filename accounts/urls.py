from django.urls import path
from .views import RegisterUserView, UserLoginView, ProtectedView


urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('protected/', ProtectedView.as_view(), name='protected'),

]
