from datetime import datetime, timezone, timedelta

from allauth.account.models import EmailAddress
from celery import shared_task
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from NewsPaper.settings import MY_MAIL

from .models import Post


@shared_task
def mail_notify_new_post(msg_data):
    html_content = render_to_string(
        'notify_new_post.html',
        {
            'msg_data': msg_data,
        }
    )
    msg = EmailMultiAlternatives(
        subject=f'Уведомление о новой публикации',
        body=f'Новая публикация в вашем любимом разделе',
        from_email=MY_MAIL,
        to=[msg_data['subscriber_email'], ],
    )
    msg.attach_alternative(html_content, "text/html")
    print(f'Отправка уведомления для: {msg_data["subscriber_email"]}')
    msg.send()


@shared_task
def weekly_notify_posts():
    print('Старт создания еженедельника')
    last_week = datetime.now(timezone.utc) - timedelta(days=7)
    users = User.objects.all()
    t = 17
    for user in users:
        msg_data = {}
        posts = Post.objects.filter(category__subscribers=user, time__gt=last_week).values('id').exists()
        if posts:
            subscriber_email = user.email
            if subscriber_email:
                if EmailAddress.objects.filter(email=subscriber_email).exists():
                    if EmailAddress.objects.get(email=subscriber_email).verified:
                        msg_data['last_week'] = last_week
                        msg_data['subscriber_name'] = user.username
                        msg_data['subscriber_email'] = subscriber_email
                        print(f'{t} Создание еженедельника для: {msg_data["subscriber_email"]}')
                        mail_weekly_notify_posts.apply_async([msg_data], countdown=t)
                        t += 17


@shared_task
def mail_weekly_notify_posts(msg_data):
    user = msg_data['subscriber_name']
    last_week = msg_data['last_week']
    posts = Post.objects.filter(
        category__subscribers__username=user,
        time__gt=last_week
    ).values('id', 'title', 'time').distinct()
    msg_data['posts'] = posts
    html_content = render_to_string(
        'weekly_notify_posts.html',
        {
            'msg_data': msg_data,
        }
    )
    msg = EmailMultiAlternatives(
        subject=f'Публикации за неделю',
        body=f'Новые публикация в вашем любимом разделе',
        from_email=MY_MAIL,
        to=[msg_data['subscriber_email'], ],
    )
    msg.attach_alternative(html_content, "text/html")
    print(f" Отправка еженедельника для: {msg_data['subscriber_email']}")
    msg.send()




