from datetime import timedelta, datetime, timezone

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.models import User
from django.core.cache import cache
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .filters.filters import PostFilter
from .forms import PostForm
from .models import Post, Author, Category, Comment
from .utilits import is_limit_spent, DAY_POST_LIMIT


class PostsList(ListView):
    model = Post
    ordering = '-time'
    template_name = 'news.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        cat_slug = self.kwargs.get('slug')
        p_type = self.kwargs.get('p_type')
        if ('AT' in self.request.path) or ('NW' in self.request.path):
            context = Post.objects.filter(p_type=p_type)
        elif cat_slug:
            context = Post.objects.filter(category__slug=cat_slug)
        else:
            context = Post.objects.all()
        return context

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        current_user = self.request.user
        cat_slug = self.kwargs.get('slug')
        p_type = self.kwargs.get('p_type')
        if p_type:
            context['post_type'] = p_type
            if p_type == Post.TP[0][0]:
                context['title'] = 'Статьи'
            elif p_type == Post.TP[1][0]:
                context['title'] = 'Новости'
            quantity = cache.get(f'quantity-{p_type}', None)
            if not quantity:
                quantity = Post.objects.filter(p_type=p_type).count()
                cache.set(f'quantity-{p_type}', quantity, 60*60*12)
            context['quantity'] = quantity
            if current_user.is_authenticated:
                if current_user.groups.filter(name='authors').exists():
                    context['is_limit_spent'] = is_limit_spent(current_user)
        elif cat_slug:
            cat_name = Category.objects.get(slug=cat_slug)
            context['category'] = cat_name
            quantity = cache.get(f'quantity-{cat_slug}', None)
            if not quantity:
                quantity = Post.objects.filter(category__slug=cat_slug).count()
                cache.set(f'quantity-{cat_slug}', quantity, 60*60*12)
            context['quantity'] = quantity
        else:
            context['title'] = 'Все публикации'
            quantity = cache.get(f'quantity-posts', None)
            if not quantity:
                quantity = Post.objects.all().count()
                cache.set(f'quantity-posts', quantity, 60*60*12)
            context['quantity'] = quantity
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'new.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = Post.objects.get(id=self.kwargs['pk'])
        comments = Comment.objects.filter(post=post)
        context['comments'] = comments
        return context

    def get_object(self, *args, **kwargs):
        obj = cache.get(f'post-{self.kwargs["pk"]}', None)
        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'post-{self.kwargs["pk"]}', obj)
        return obj

class PostSearch(ListView):
    model = Post
    ordering = '-time'
    template_name = 'search.html'
    context_object_name = 'posts'
    extra_context = {'title': 'Поиск публикации'}
    paginate_by = 4

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        if 'do_search' in self.request.GET:
            context['is_search'] = True
        return context


class PostCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post', )
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create'] = 'True'
        if Post.TP[0][0] in self.request.path:
            context['title'] = 'Добавить статью'
        elif Post.TP[1][0] in self.request.path:
            context['title'] = 'Добавить новость'
        return context

    def form_valid(self, form, **kwargs):
        if not is_limit_spent(self.request.user):
            post = form.save(commit=False)
            post.p_type = self.kwargs["p_type"]
            author = Author.objects.get(author_acc=self.request.user)
            post.author = author
            return super().form_valid(form)
        else:
            return redirect('post_limit_spent')


class PostEdit(PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post', )
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    extra_context = {'title': 'Редактировать публикацию', }


class PostDelete(DeleteView):
    # permission_required = ('news.delete_post', )
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('posts_page')
    extra_context = {'title': 'Удалить публикацию'}

    # def form_valid(self, form, **kwargs):
    #     p_type = self.object.p_type
    #     cache.delete(f'quantity-{p_type}')
    #     return super().form_valid(form)

@login_required
def subscribe_me(request, slug):
    user = request.user
    category = Category.objects.get(slug=slug)
    categories = Category.objects.filter(subscribers__username=user)
    if category not in categories:
        category.subscribers.add(user)
    return redirect(request.META.get('HTTP_REFERER'))


@login_required
def unsubscribe_me(request, slug):
    user = request.user
    category = Category.objects.get(slug=slug)
    if Category.objects.filter(subscribers__username=user).exists():
        category.subscribers.remove(user)
    return redirect(request.META.get('HTTP_REFERER'))


def post_limit_spent_view(request):
    title = 'имя_подписчика',
    limit = DAY_POST_LIMIT
    return render(request, 'post_limit_spent.html', {'title': title, 'limit': limit})


# function for test the view of the notification email
def mail_notify_new_post_view(request):
    msg_data = {'subscriber_name': 'имя_подписчика',
        'new_post_title': 'заголовок_новой_публикации',
        'author_first_name': 'имя_автора',
        'author_last_name': 'фамилия_автора',
        'new_post_time': 'время_выхода_новой_публикации',
        'new_post_text': 'текст_новой_публикации',
        'new_post_pk': '7',
    }
    return render(request, 'notify_new_post.html', {'msg_data': msg_data, })


# function for test the view of the notification email
def mail_weekly_notify_posts_view(request):
    user = User.objects.get(id=14)
    last_week = datetime.now(timezone.utc) - timedelta(days=70)
    posts = Post.objects.filter(category__subscribers__username=user.username, time__gt=last_week).values('id', 'title', 'time')
    msg_data = {'subscriber_name': user.username, 'posts': posts}
    return render(request, 'weekly_notify_posts.html', {'msg_data': msg_data, })

