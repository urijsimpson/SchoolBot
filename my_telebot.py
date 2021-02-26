import telebot
import sys, io
from telebot import types


import sqlite3
from my_token import token

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
    bot.send_message(message.chat.id, 'выберите класс', reply_markup=class_grade_keyboard())
    if message.text == '5':
        bot.register_next_step_handler(message, class_letter(message))

    elif message.text == '6':
        bot.register_next_step_handler(message, class_letter(message))

def class_grade_keyboard():
    markup = types.ReplyKeyboardMarkup()
    KeyBtnGrade_5 = types.KeyboardButton('5')
    KeyBtnGrade_6 = types.KeyboardButton('6')
    markup.add(KeyBtnGrade_5, KeyBtnGrade_6)
    return markup

@bot.message_handler(content_types='text')
def class_letter(message):
    bot.send_message(message.chat.id, 'выберите букву класса', reply_markup=class_letter_keyboard())
    if message.text == 'а':
        bot.register_next_step_handler(message, day(message))

    elif message.text == 'б':
        bot.register_next_step_handler(message, day(message))

@bot.message_handler(content_types='text')
def day(message):
    bot.send_message(message.chat.id, 'выберите день недели', reply_markup=day_of_week())



def day_of_week():
    markup = types.ReplyKeyboardMarkup()
    KeyBtnMonday = types.KeyboardButton('понедельник')
    KeyBtnTuesday = types.KeyboardButton('вторник')
    KeyBtnWednesday = types.KeyboardButton('среда')
    KeyBtnThursday = types.KeyboardButton('четверг')
    KeyBtnFriday = types.KeyboardButton('пятница')
    markup.add(KeyBtnMonday, KeyBtnTuesday, KeyBtnWednesday, KeyBtnThursday, KeyBtnFriday)
    return markup


def class_letter_keyboard():
    markup = types.ReplyKeyboardMarkup()
    KeyBtnLetter_a = types.KeyboardButton('а')
    KeyBtnLetter_b = types.KeyboardButton('б')
    markup.add(KeyBtnLetter_a, KeyBtnLetter_b)
    return markup







bot.polling(none_stop=True)
