from django import template
from django.core.cache import cache

from news.models import CensorVoc

register = template.Library()

@register.filter()
def censor(content):
    st = '*' * 26
    sb = ''' !"#$%&'*+,-./:;=?@\^_`|~ '''
    text = content
    cens_words = cache.get(f'cens_words', None)
    if not cens_words:
        cens_words = CensorVoc.objects.values_list('word')
        cache.set(f'cens_words', cens_words)
    for word in cens_words:
        j = len(word[0])
        i = 0
        while i >= 0:
            i = text.lower().translate(str.maketrans(sb, st,)).find(word[0])
            if i > 0:
                text = text[:i] + '*' * j + text[(i + j):]
    return f'{text}'
