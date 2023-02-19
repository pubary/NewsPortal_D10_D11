from django.urls import path

from .views import UserAccountView

urlpatterns = [
    path('', UserAccountView.as_view(), name='user_home'),
]