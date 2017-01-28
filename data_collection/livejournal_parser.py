'''
Парсер постов ЖЖ на примере Артемия Лебедева.
start_page_id – id поста, с которого необходимо парсить.
'''

import urllib.request
from bs4 import BeautifulSoup

texts_list = []

start_page_id = '2397668'
url = 'http://tema.livejournal.com/' + start_page_id + '.html'
n = 10


for i in range(n):
    data = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(data, "html.parser")

    text = soup.find('article', class_='b-singlepost-body').text
    texts_list.append(text)

    content_tag = soup.find_all('meta')[-2]['content']
    page_id = content_tag.split('/')[-1].split('.')[0]
    url = 'http://www.livejournal.com/go.bml?journal=tema&itemid=' + page_id + '&dir=prev'


with open('lj_result.txt', 'w') as data_file:
    for text in texts_list:
        data_file.write(text + '\n')
