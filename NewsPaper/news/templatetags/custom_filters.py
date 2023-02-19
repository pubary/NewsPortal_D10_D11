from django import template
from news.models import CensorVoc

register = template.Library()

@register.filter()
def censor(content):
    g = '*' * 26
    h = ''' !"#$%&'*+,-./:;=?@\^_`|~ '''
    text = content
    cens_words = CensorVoc.objects.values_list('word')
    for word in cens_words:
        j = len(word[0])
        i = 0
        while i >= 0:
            i = text.lower().translate(str.maketrans(h, g,)).find(word[0])
            if i > 0:
                text = text[:i] + '*' * j + text[(i + j):]
    return f'{text}'