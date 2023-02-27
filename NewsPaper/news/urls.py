from django.views.decorators.cache import cache_page
from django.urls import path
from .views import *

urlpatterns = [
   path('search/', PostSearch.as_view(), name='post_search'),
   path('cat/<slug:slug>/', cache_page(60*3)(PostsList.as_view()), name='category_show'),
   path('cat/<slug:slug>/subscribe', subscribe_me, name='subscription'),
   path('cat/<slug:slug>/unsubscribe', unsubscribe_me, name='unsubscription'),
   path('<int:pk>/', PostDetail.as_view(), name='post_detail'),
   path('<slug:p_type>/create/', PostCreate.as_view(), name='post_create'),
   path('<int:pk>/edit/', PostEdit.as_view(), name='post_edit'),
   path('<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
   path('mail_notify_new_post/', mail_notify_new_post_view, name='mail_notify_new_post'),
   path('weekly_notify_posts/', mail_weekly_notify_posts_view, name='mail_weekly_notify_posts'),
   path('<slug:p_type>/', cache_page(60*3)(PostsList.as_view()), name='post_type'),

]