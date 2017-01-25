'''
Скрипт парсинга сообщений на стене пользователя/сообщества в vk.
Для работы необходимо создать приложение в vk и получить access_token.

Для получения токена использовать следующий запрос:
https://oauth.vk.com/authorize?client_id={CLIENT_ID}&display=page&redirect_uri=https://oauth.vk.com/blank.html&response_type=token&v=5.60
(вместо {CLIENT_ID} ID вашего приложения)

Необходимые константы:
ACCESS_TOKEN – полученный access_token, строка.
OWNER_ID – ID цели (группы или пользователя), число. ID группы – отрицательное число.
FROM – начальное значение для цикла парсинга.
TO – конечное значение для цикла парсига.

По-умолчанию FROM = 0, TO = 500. Так как шаг в цикле фиксированный (100),
то это значит, что программа сделает 4 итерации и в каждой итерации спарсит
100 текущих постов из ленты.
'''


import vk
import re
import time


ACCESS_TOKEN = 'TOKEN'
OWNER_ID = 12345678
FROM = 0
TO = 400


session = vk.Session(access_token=ACCESS_TOKEN)
api = vk.API(session, v='5.60')


def check_strings(str_list):
    '''
    На вход функции подаётся список строк. Функция проверяет, что:
    - Список не пустой
    - В списке больше 1 строки
    - Длина всех строк не больше 150
    - Ни одна строка не содержит символ переноса строки
    '''
    if str_list == [] or len(str_list) == 1:
        return False

    for string in str_list:
        if len(string) > 150 or string.count('\n') > 0:
            return False

    return True


dialogues = []

for offset in range(FROM, TO, 100):
    # получаем 100 постов из ленты
    response = api.wall.get(owner_id=OWNER_ID, count=100, offset=offset)

    for item in response['items']:
        post_id = item['id']

        # получаем 100 комментариев из текущего поста
        res = api.wall.getComments(owner_id=OWNER_ID, post_id=post_id, count=100)

        # список всех спарсенных комментариев и мн-во айди юзеров
        messages = []
        id_set = set()

        for message in res['items']:
            if message['text'] != '' and 'reply_to_user' in message:

                # убираем [id0123456789|Username]
                text = re.sub('\[\S+.\S+\],', '', message['text'])
                text = text.strip()

                messages.append([message['from_id'],
                                 message['reply_to_user'],
                                 text])

                id_set.add(message['from_id'])

        # словарь диалогов - ключом в словаре являются строки
        # вида "first_id second_id"
        messages_dict = dict()
        # множество уникальный id в виде списка
        id_list = list(id_set)

        # составляем все возможные пары из пользователей (без повторений)
        for i in range(len(id_list) - 1):
            for j in range(i + 1, len(id_list)):
                messages_dict[str(id_list[i]) + ' ' + str(id_list[j])] = []

        # заполняем словарь со следующей структурой:
        # ключ - строка вида "first_id second_id"
        # значение - массив строк (диалог между пользователями)
        for i in range(len(messages)):
            m_i0, m_i1 = messages[i][0], messages[i][1]

            cond_1 = (str(m_i0) + ' ' + str(m_i1)) in messages_dict
            cond_2 = (str(m_i1) + ' ' + str(m_i0)) in messages_dict

            if cond_1:
                messages_dict[str(m_i0) + ' ' + str(m_i1)].append(messages[i][2])
            elif cond_2:
                messages_dict[str(m_i1) + ' ' + str(m_i0)].append(messages[i][2])

        # проходимся по словарю с диалогами и отбираем те, ВСЕ строки
        # в которых соответствуют правилам
        for key, value in messages_dict.items():
            if value != [] and len(value) != 1 and check_strings(value):
                dialogues.append(value)

        # задержка, чтобы не падать с ошибкой
        time.sleep(0.5)
    print('{} posts – DONE!'.format(offset + 100))

# записываем диалоги в файл
with open('vk_comments_parser_result.txt', 'w') as out_file:
    for dialogue in dialogues:
        for string in dialogue:
            out_file.write(string)
            out_file.write('\n')
        out_file.write('\n')
