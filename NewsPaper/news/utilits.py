import time

from allauth.account.models import EmailAddress
from django.contrib.auth.models import User

from .models import Post
from .tasks import mail_notify_new_post


DAY_POST_LIMIT = 3


def is_limit_spent(user):
    lim = DAY_POST_LIMIT
    posts = Post.objects.filter(author__author_acc=user)
    quantity = posts.count()
    if quantity < lim:
        return False
    else:
        time_post = posts.order_by('-time').values_list('time', flat=True)[(lim-1):lim]
        dt = (time.time() - time_post[0].timestamp()) / 3600 / 24
        if dt > 1:
            return False
        else:
            return lim


def notify_new_post():
    new_post = Post.objects.all().order_by('-time').first()
    msg_data = {}
    msg_data['new_post_title'] = new_post.title
    msg_data['new_post_text'] = new_post.text[:63]
    msg_data['new_post_time'] = new_post.time
    msg_data['author_first_name'] = new_post.author.author_acc.first_name
    msg_data['author_last_name'] = new_post.author.author_acc.last_name
    msg_data['new_post_pk'] = new_post.id
    subscribers_name = set(new_post.category.values_list('subscribers__username', flat=True))
    t = 7
    print(f'Поиск подписчиков новой публикации id{new_post.id}')
    for subscriber_name in subscribers_name:
        if subscriber_name == new_post.author.author_acc.username:
            break
        if subscriber_name:
            msg_data['subscriber_name'] = subscriber_name
            subscriber_email = User.objects.get(username=subscriber_name).email
            if subscriber_email:
                print(f'Проверка валидации почты {subscriber_email}')
                if EmailAddress.objects.filter(email=subscriber_email).exists():
                    if EmailAddress.objects.get(email=subscriber_email).verified:
                        msg_data['subscriber_email'] = subscriber_email
                        print(t, ' Создание задачи уведомления для ', msg_data['subscriber_email'])
                        mail_notify_new_post.apply_async([msg_data], countdown=t)
                        t += 7

