from django.db.models.signals import m2m_changed
from django.dispatch import receiver

from .models import Post
from .utilits import notify_new_post


@receiver(m2m_changed, sender=Post.category.through)
def notify_post_subscriber(sender, instance, **kwargs):
    if kwargs['action'] == 'post_add':
        print('Начало работы по сигналу о новой публикации')
        notify_new_post()

