from django.urls import path
from .views import RegisterUserView


urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register'),
    path('user/<int:user_id>/', RegisterUserView.as_view(), name='get_user'),

]
