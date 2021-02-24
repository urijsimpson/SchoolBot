import telebot
from telebot import types
import sqlite3
from my_token import chat_id, bot




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


conn = create_conection("timetable.db")

lSql = []
lSql.append(""" CREATE TABLE IF NOT EXISTS timetable (id integer PRIMARY KEY,
                                                      class_id integer not null,  
                                                      lesson_subject_id integer not NULL,
                                                      lesson_index integer not NULL,
                                                      lesson_day_id integer not NULL
                                                      ); """)

lSql.append(""" CREATE TABLE IF NOT EXISTS subjects (subject_id integer PRIMARY KEY,
                                                     subject_name text not NULL,
                                                     ); """)

lSql.append(""" CREATE TABLE IF NOT EXISTS dow (day_id integer PRIMARY KEY,
                                                day_name text not NULL
                                                ); """)

lSql.append(""" CREATE TABLE IF NOT EXISTS classes (class_id integer PRIMARY KEY,
                                                    class_grade integer not NULL,
                                                    class_letter text not null
                                                    ); """)


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
