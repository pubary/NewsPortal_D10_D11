d = {
    'а' : ['a', '@'],
    'б' : ['6', 'b'],
    'в' : ['b', 'v'],
    'г' : ['r', 'g'],
    'д' : ['d'],
    'е' : ['e',],
    'ё' : ['е', 'e'],
    'ж' : ['zh', '*'],
    'з' : ['3', 'z'],
    'и' : ['u', 'i'],
    'й' : ['и', 'u', 'i'],
    'к' : ['k', 'i{', '|{'],
    'л' : ['l', 'ji'],
    'м' : ['m'],
    'н' : ['h', 'n'],
    'о' : ['o', '0'],
    'п' : ['n',],
    'р' : ['r', 'p'],
    'с' : ['c', 's'],
    'т' : ['m', 't'],
    'у' : ['y', 'u'],
    'ф' : ['f'],
    'х' : ['x', '}{', ')(', '><'],
    'ц' : ['c', 'u,'],
    'ч' : ['ch', '4'],
    'ш' : ['sh', 'lli'],
    'щ' : ['sch', 'lll'],
    'ь' : ['b',],
    'ы' : ['bi', 'bl'],
    'ъ' : ['`b',],
    'э' : ['e',],
    'ю' : ['io',],
    'я' : ['ya',],
    }
spaces = [' ', '*']

bed_parts = ['редис',]


def censorList():
    bed_words = []
    for part in bed_parts:
        for space in spaces:
            bed_word = space.join(part)
            bed_words.append(bed_word)
    bed_words.extend(bed_parts)

    cens_words = []
    for word in bed_words:
        cens_words.append(word)
        for letter in word:
            symbols = d.get(letter)
            if symbols:
                for symbol in symbols:
                    cens_word = word.replace(letter, symbol)
                    bed_words.append(cens_word)
    cens_words = list(set(cens_words))
    # print(len(cens_words))
    return cens_words


if __name__ == '__main__':

    text = f'пои ватыоащо аp.е.д.и.c ку! сЛ?ова\n в спап4у4 '
    g = '*' * 26
    h = ''' !"#$%&'*+,-./:;=?@\^_`|~ '''
    cens_words = censorList()
    for word in cens_words:
        j = len(word)
        i = 0
        while i >= 0:
            i = text.lower().translate(str.maketrans(h, g,)).find(word)
            if i > 0:
                text = text[:i] + '*' * j + text[(i + j):]

###  to start move for example to views.MainPage
### from news.models import CensorVoc
### from news.templatetags.censor_init import censorList

    ### cens_words = censorList()
    ### for word in cens_words:
    ###     if not CensorVoc.objects.filter(word=word):
    ###         CensorVoc.objects.create(word=word)