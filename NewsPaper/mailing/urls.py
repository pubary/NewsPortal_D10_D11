from django.urls import path
from .views import *

urlpatterns = [
   path('', FeedbackMailView.as_view(), name='feedback_mail'),
   path('feedback_answer_mail/', feedback_answer_mailview, name='feedback_answer_mail'),
   path('signup_mail/', signup_mailview, name='signup_mail'),
]