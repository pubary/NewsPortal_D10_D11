from django.contrib.auth.models import User
from django.db import models
from datetime import datetime


class FeedbackMail(models.Model):
    date = models.DateField(
        default=datetime.utcnow,
    )
    reader_name = models.CharField(
        max_length=255
    )
    message = models.TextField()

    def __str__(self):
        return f'{self.reader_name}: {self.message}'

# class NotifyNewPost(models.Model):
#     date = models.DateField(
#         default=datetime.utcnow,
#     )
#     subscriber_name = models.OneToOneField(
#         User,
#         on_delete=models.CASCADE,
#         primary_key=True,
#         verbose_name='Имя пользователя',
#     )
#     message = models.TextField()