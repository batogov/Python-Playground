import re
from collections import defaultdict
from random import uniform, choice


def check_word(word):
    '''
    Если слово не является знаком препинания, то функция
    возвращает True, иначе – False.
    '''
    for symbol in '.,:;?!':
        if word == symbol:
            return False
    return True


def text_prettifier(text):
    '''
    Удаляет в тексте лишние пробелы вокруг знаков препинания.
    '''
    for symbol in '.,:;?!':
        text = text.replace(' ' + symbol + ' ', symbol + ' ')
    return text


def unirand(seq):
    sum_, freq_ = 0, 0
    for item, freq in seq:
        sum_ += freq
    rnd = uniform(0, sum_)
    for token, freq in seq:
        freq_ += freq
        if rnd < freq_:
            return token


def get_tokens(corpus_list):
    reg_exp = re.compile('[а-яА-Я0-9-]+|[.,:;?!]+')

    tokens = []
    for corpus in corpus_list:
        data = open(corpus, 'r')

        for line in data:
            tokens += reg_exp.findall(line.lower())

    return tokens


def train(corpus):
    trigrams = []

    for i in range(len(tokens) - 2):
        trigrams.append(tokens[i : i + 3])

    bi, tri = defaultdict(lambda: 0.0), defaultdict(lambda: 0.0)

    for t0, t1, t2 in trigrams:
        bi[t0, t1] += 1
        tri[t0, t1, t2] += 1

    model = {}
    for (t0, t1, t2), freq in tri.items():
        if (t0, t1) in model:
            model[t0, t1].append((t2, freq / bi[t0, t1]))
        else:
            model[t0, t1] = [(t2, freq / bi[t0, t1])]

    return model


def generate_text(model, sents_count):
    # случайно выбираем первые два слова (причём эти слова
    # не знаки препинания)
    t0, t1 = choice(list(model.keys()))
    while not (check_word(t0) and check_word(t1)):
        t0, t1 = choice(list(model.keys()))

    # добавляем эти два слова с список слов
    words = [t0.capitalize(), t1]

    # в цикле выбираем на основе прошлых
    # двух слов следующее слово
    while sents_count > 0:
        t2 = unirand(model[t0, t1])

        if t1 in '.?!':
            words.append(t2.capitalize())
        else:
            words.append(t2)

        if t2 == '.':
            sents_count -= 1

        t0, t1 = t1, t2

    # формируем результирующий текст
    text = ' '.join(words[:-1])
    text = text_prettifier(text) + '.'

    return text


tokens = get_tokens(['book1.txt', 'book2.txt'])
model = train(tokens)
print(generate_text(model, 3))
