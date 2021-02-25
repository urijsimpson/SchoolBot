import telebot
import sys, io
from telebot import types


import sqlite3
from my_token import chat_id, token

bot = telebot.TeleBot(token)



def create_conection(datafile):
    conn = None
    try:
        conn = sqlite3.connect(datafile)
        return conn
    except sqlite3.DatabaseError as e:
        print(e)
        return conn


def exec_sql(conn, sSql):
    try:
        c = conn.cursor()
        c.execute(sSql)
    except sqlite3.DatabaseError as e:
        print(e)

def get_record(conn, sSql):
    try:
        c = conn.cursor()
        c.execute(sSql)
        return c.fetchone()[0]
    except sqlite3.DatabaseError as e:
        print(e)

def get_records(conn, sSql):
    try:
        c = conn.cursor()
        c.execute(sSql)
        return c.fetchall()
    except sqlite3.DatabaseError as e:
        print(e)


conn = create_conection("timetable.db")

lSql = []
'''
Таблица - расписание
'''
lSql.append(""" CREATE TABLE IF NOT EXISTS timetable (id integer PRIMARY KEY,
                                                      class_id integer not null,  
                                                      lesson_subject_id integer not NULL,
                                                      lesson_index integer not NULL,
                                                      lesson_day_id integer not NULL
                                                      ); """)

'''
Справочник предметов
'''
lSql.append(""" CREATE TABLE IF NOT EXISTS subjects (subject_id integer PRIMARY KEY,
                                                     subject_name text not NULL,
                                                     subject_tutor text
                                                     ); """)
'''
Справочник дней недели Days of weeek
'''
lSql.append(""" CREATE TABLE IF NOT EXISTS dow (day_id integer PRIMARY KEY,
                                                day_name text not NULL
                                                ); """)

'''
Справоник классов
'''
lSql.append(""" CREATE TABLE IF NOT EXISTS classes (class_id integer PRIMARY KEY,
                                                    class_grade integer not NULL,
                                                    class_letter text not null
                                                    ); """)
'''
Здесь создается структура базы данных
'''
for sSql in lSql:
    exec_sql(conn, sSql)

'''
Здесь база заполняется
'''
def fill_tables(conn):
    try:
        lSubList = ["алгебра"
            , "химия"
            , "физика"
            , "география"
            , "физкультура"
            , "английский"
            , "информатика"
            , "история"
            , "русский"
            , "литература"
            , "геометрия"
            , "биология"
            , "обж"]

        lDayOW = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

        for i, sName in enumerate(lSubList):
            '''
            Вставка записи в таблицу, содержащую список предметов
            '''
            sSql = f"insert into subjects (subject_id, subject_name, subject_tutor) values ('{i}', '{sName}', '{sName}')"
            exec_sql(conn, sSql)
            conn.commit()

        for i, sDay in enumerate(lDayOW):
            '''
            Вставка записей в таблицу - справочник дней недели
            '''
            sSql = f"insert into dow (day_id, day_name) values ('{i}','{sDay}')"
            exec_sql(conn, sSql)
            conn.commit()

        lClasses = [[5, 'а', 'б', 'в', 'г', 'д', 'е', 'ж'],
                    [6, 'а', 'б', 'в', 'г', 'д', 'е'],
                    [7, 'а', 'б', 'в'],
                    [8, 'а', 'б', 'в', 'г'],
                    [9, 'а', 'б', 'в'],
                    [10, 'а', 'б', 'в'],
                    [11, 'а', 'б'], ]

        for j, lGrade in enumerate(lClasses):
            print(lGrade)
            for i, sLetter in enumerate(lGrade):
                iGrade = lGrade[0]
                if isinstance(sLetter, int) != True:
                    ij = int(str(j) + str(i))
                    '''
                    Вставка записей в таблицу - справочник , содержащий классы
                    '''
                    sSql = f"insert into classes (class_id, class_grade, class_letter) values ('{ij}','{iGrade}','{sLetter}')"
                    print(sSql)
                    exec_sql(conn, sSql)
                    conn.commit()
        return True

    except:
        return False

'''
Проверим, есть ли уже записи в БД
'''
#print(get_record(conn, 'select count(*) from classes'))
iRecordCount = int(get_record(conn, 'select count(*) from classes'))
if iRecordCount == 0:
    '''
    Если записей нет - заполним
    '''
    if fill_tables(conn):
        print("Common data has been upload to DB")
    else:
        print("Something went wrong")
        sys.exit(0)


'''
Пример, как получить записи из базы
'''
print('****')
print("Будут выбраны ВСЕ записи из представления v_timetable")
print('****')
records = get_records(conn, 'select id, class, subject, tutor, lesson_index, day_of_week from v_timetable')
for record in records:
    if record:
        print(record)


'''
Пример, как получить записи по определенному классу и дню недели из базы
'''
sClassName = '10 а'
sDowName = 'Tuesday'

print('****')
print(f"Будут выбраны предметы для класса {sClassName} и дня недели {sDowName}")
print('****')
records = get_records(conn, f"select id, class, subject, tutor, lesson_index, day_of_week from v_timetable where class = '{sClassName}' and day_of_week = '{sDowName}'")
for record in records:
    if record:
        print(record)

print('')

'''
Пример, как получить записи по определенному классу и дню недели из базы
'''
sClassName = '10 б'
sDowName = 'Tuesday'

print('****')
print(f"Будут выбраны предметы для класса {sClassName} и дня недели {sDowName}")
print('****')
records = get_records(conn, f"select id, class, subject, tutor, lesson_index, day_of_week from v_timetable where class = '{sClassName}' and day_of_week = '{sDowName}'")
for record in records:
    if record:
        print(record)

print('')

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, 'to continue type \'keyboard\'')


@bot.message_handler(commands=['keyboard'])
def KeyBoardWelc(message):
    markup = types.ReplyKeyboardMarkup(row_width=2)
    button1 = types.KeyboardButton('10')
    button2 = types.KeyboardButton('9')
    button3 = types.KeyboardButton('8')
    markup.add(button1, button2, button3)
    bot.send_message(chat_id, 'select class digit', reply_markup=markup)


@bot.message_handler(regexp='8')
def KeyBoardBtn(message):
    markup = types.ReplyKeyboardMarkup(row_width=2)
    button1 = types.KeyboardButton('V')
    button2 = types.KeyboardButton('B')
    markup.add(button1, button2)
    bot.send_message(chat_id, 'select class letter', reply_markup=markup)


@bot.message_handler(regexp='9')
def KeyBoartBtn(message):
    markup = types.ReplyKeyboardMarkup(row_width=2)
    button1 = types.KeyboardButton('V')
    button2 = types.KeyboardButton('B')
    markup.add(button1, button2)
    bot.send_message(chat_id, 'select class letter', reply_markup=markup)


@bot.message_handler(regexp='10')
def KeyBoartBtn(message):
    markup = types.ReplyKeyboardMarkup()
    button1 = types.KeyboardButton('V')
    button2 = types.KeyboardButton('B')
    markup.add(button1, button2)
    bot.send_message(chat_id, 'select class letter', reply_markup=markup)


bot.polling()
