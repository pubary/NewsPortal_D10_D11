from django.forms import DateInput, RadioSelect
from django_filters import FilterSet, ModelMultipleChoiceFilter, DateTimeFilter, ModelChoiceFilter, ChoiceFilter
from news.models import Post, Category, Author


class PostFilter(FilterSet):
    p_type = ChoiceFilter(
        choices=Post.TP,
        widget=RadioSelect,
        label='Тип публикации',
    )
    category = ModelMultipleChoiceFilter(
        field_name='postcategory__category',
        queryset=Category.objects.all(),
        label='Категория (или одна или несколько)',
        conjoined=True,
    )
    time = DateTimeFilter(
        field_name='time',
        lookup_expr='gte',
        widget=DateInput(attrs={'type': 'date'}),
    )
    # author = ModelChoiceFilter(
    #     field_name='author__author_acc',
    #     queryset=Author.objects.all(),
    #     label='Автор',
    # )

    class Meta:
        model = Post
        fields = {
            'title': ['icontains'],
            'text': ['icontains'],
#            'p_type': ['exact'],
            }


