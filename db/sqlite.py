import sqlite3

# если такой базы нет, то мы её создадим
conn = sqlite3.connect('my.sqlite')

# создаём курсор
c = conn.cursor()

# создаём таблицу в бд
c.execute('CREATE TABLE users (id INTEGER PRIMARY KEY, name VARCHAR, surname VARCHAR)')

# функция занесения пользователей в базу
def add_user(name, surname):
    c.execute("INSERT INTO users (name, surname) VALUES ('%s','%s')" % (username, surname))
    conn.commit()

n = int(input('Количество пользователей, которых нужно занести в БД: '))
for i in range(n):
    print('Пользователь', i + 1)
    username = input('Имя: ')
    surname = input('Фамилия: ')
    add_user(username, surname)

# выводим список пользователей в цикле
for row in c.execute('SELECT * FROM users'):
    print(row)

# закрываем соединение с базой
c.close()
conn.close()
