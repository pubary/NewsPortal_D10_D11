from django.contrib.auth.models import User
from django.db import models
from django.db.models import Sum
from django.urls import reverse
from transliterate import slugify


class Author(models.Model):
    author_acc = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
        verbose_name='Имя пользователя',
    )
    rating = models.IntegerField(default=0, verbose_name='Рейтинг',)

    def update_rating(self):
        self.rating = 0
        aut_post = Post.objects.filter(author=self.author_acc_id)
        r1 = aut_post.aggregate(Sum('rating'))
        r1 = r1.get(str(list(r1.keys())[0]))
        if r1 is None:
            r1 = 0
        aut_comm = Comment.objects.filter(user=self.author_acc_id)
        r2 = aut_comm.aggregate(Sum('rating'))
        r2 = r2.get(str(list(r2.keys())[0]))
        if r2 is None:
            r2 = 0
        all_com = Comment.objects.filter(post__author=self.author_acc_id).values('user', 'rating')
        r3 = all_com.aggregate(Sum('rating'))
        r3 = r3.get(str(list(r3.keys())[0]))
        if r3 is None:
            r3 = 0
        ex_com = Comment.objects.filter(user=self.author_acc_id, post__author=self.author_acc_id).values('user', 'rating')
        r4 = ex_com.aggregate(Sum('rating'))
        r4 = r4.get(str(list(r4.keys())[0]))
        if r4 is None:
            r4 = 0
        self.rating = 3 * r1 + r2 + r3 - r4
        self.save()

    def __str__(self):
        return f'{self.author_acc.username}'


    class Meta:
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'
        ordering = ['author_acc__username']


class Category(models.Model):
    cat_name = models.CharField(max_length=63,
                                unique=True,
                                verbose_name='Категория'
                                )
    slug = models.SlugField(max_length=63,
                            unique=True,
                            null=False,
                            verbose_name='URL',
                            )
    subscribers = models.ManyToManyField(
        User,
        through='Subscription',
        related_name='subscribers',
    )


    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['cat_name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.cat_name)
        return super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.cat_name}'


class Post(models.Model):
    article = 'AT'
    news = 'NW'
    TP = [
        (article, 'Статья'),
        (news, 'Новость'),
    ]
    p_type = models.CharField(
        max_length=7,
        choices=TP,
        verbose_name='Тип',
    )
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    time = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    text = models.TextField(verbose_name='Текст публикации')
    rating = models.IntegerField(default=0, verbose_name='Рейтинг')
    author = models.ForeignKey(
        Author,
        on_delete=models.SET('Автор неизвестен'),
        verbose_name='Автор',
    )
    category = models.ManyToManyField(
        Category,
        through='PostCategory',
        verbose_name='Категории'
    )

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return f'{self.title}\n{self.text[0:125]}...'

    def __str__(self):
        return f'{self.title.title()}: {self.text[:40]}'

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])

    class Meta:
        verbose_name = 'Публикация'
        verbose_name_plural = 'Публикации'
        ordering = ['-time']


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    text = models.TextField(verbose_name='Текст комментария')
    time = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    rating = models.IntegerField(default=0, verbose_name='Рейтинг')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='К публикации')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['-time']

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def __str__(self):
        return f'{self.text[:30]}'


class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, )
    category = models.ForeignKey(Category, on_delete=models.CASCADE, )


class CensorVoc(models.Model):
    word = models.CharField(max_length=63)