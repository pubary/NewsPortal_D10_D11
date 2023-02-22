from django.core.cache import cache
from django.db.models.signals import m2m_changed, post_delete, post_save
from django.dispatch import receiver

from .models import Post, Category, Comment
from .utilits import notify_new_post


@receiver(m2m_changed, sender=Post.category.through)
def notify_post_subscriber(sender, instance, action, **kwargs):
    if action == 'post_add':
        print('Сигнал о новой публикации')
        notify_new_post()


@receiver(m2m_changed, sender=Post.category.through)
def delete_cache_count(sender, instance, action, **kwargs):
    if action == 'post_add' or action == 'post_remove':
        cache.delete(f'quantity-{instance.p_type}')
        cache.delete(f'quantity-posts')
        for cat in instance.category.all().values_list('cat_name', flat=True):
            slug = Category.objects.get(cat_name=cat).slug
            cache.delete(f'quantity-{slug}')


@receiver(post_delete, sender=Comment)
def delete_comment_cache(sender, instance, **kwargs):
    cache.delete(f'com-to-id{instance.post.id}')


@receiver(post_save, sender=Comment)
def delete_comment_cache(sender, instance, **kwargs):
    cache.delete(f'com-to-id{instance.post.id}')