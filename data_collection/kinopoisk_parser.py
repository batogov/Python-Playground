import requests
from bs4 import BeautifulSoup
import time


def write_to_file(filename, text):
    with open(filename, 'a') as data_file:
        data_file.write(text + '\n')


def do_parsing(count, offset, error_step, filename):
    base_url = 'https://plus.kinopoisk.ru/film/'
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'}

    i = 0
    while i < count:
        url = base_url + str(i + offset)

        r = requests.get(url, headers = headers)
        soup = BeautifulSoup(r.text, "html.parser")

        tags = soup.findAll('div', itemprop='description')
        if tags != []:
            text = tags[0].text
            write_to_file(filename, text)
            print('FILM #{} DONE!'.format(i + offset))
            i += 1
        else:
            print('FILM #{} ERROR!'.format(i + offset))
            i += error_step

        time.sleep(5)

# начинаем с id = 2000 до id = 4000 c шагом ошибки = 10
do_parsing(2000, 2000, 10, 'kinopoisk_results.txt')
