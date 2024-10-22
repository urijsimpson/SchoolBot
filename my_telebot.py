import sys
import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from my_token import token, chat_id

sMyToken = token

import sqlite3


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


class StringParser():
    def __init__(self, connection):
        self.conn = connection
        pass

    def get_class(self, sString):
        try:
            if sString.split()[0].isdecimal() and int(sString.split()[0]) > 0 and int(sString.split()[0]) < 12:
                sClassName = f"{sString.split()[0]} {sString.split()[1]}"
                return sClassName
            else:
                return -1

        except ValueError as err:
            return -2
        except OSError as err:
            return -3

    def get_dow(self, sString):
        return

    def get_data(self, sString):
        lRecordList = []
        lRecordList.clear()
        try:
            if sString.split()[1].isdecimal():
                if int(sString.split()[1]) > 0 and int(sString.split()[1]) < 12:
                    sClassName = f"{sString.split()[1]} {sString.split()[2]}"
                else:
                    return "Class grade must be between 1 - 11"
            else:
                return ["Wrong format"]
            c = self.conn.cursor()
            c.execute(f"select count(*) from v_timetable where class = '{sClassName}'")
            iExists = int(c.fetchone()[0])
            if iExists == 0:
                return [f"Class {sClassName} doesn't exists in timetable"]
            else:
                sDow = sString.split()[3]

            c.execute(
                f"select count(*) from  v_timetable where class = '{sClassName}' and upper(day_of_week) = upper('{sDow}')")

            iExists = int(c.fetchone()[0])
            if iExists == 0:
                return [f"No timetable for {sClassName} to {sDow}"]
            else:
                c.execute(
                    f"select lesson_index, class, subject, tutor  from v_timetable where class = '{sClassName}' and day_of_week = '{sDowName}'")

                for record in c.fetchall():
                    lRecordList.append(record)
                return lRecordList

        except ValueError as err:
            return ("ERROR", err)
        except OSError as err:
            return ("ERROR", err)


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
records = get_records(conn,
                      f"select id, class, subject, tutor, lesson_index, day_of_week from v_timetable where class = '{sClassName}' and day_of_week = '{sDowName}'")
for record in records:
    if record:
        print(record)

print('')

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO,
                    filename='telebot.log')

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.

def get(update, context):
    """Send a message when the command /start is issued."""
    myParser = StringParser(create_conection("timetable.db"))
    tTimeTable = myParser.get_data(update.message.text)
    sResultRecord = ''
    if tTimeTable:
        for sRecord in tTimeTable:
            sCurentRecord, sCurentRecord = '', ''
            for sField in sRecord:
                sCurentField = str(sField)
                sCurentRecord = f"{sCurentRecord} {sCurentField}"

            update.message.reply_text(sCurentRecord)


def help(update, context):
    """Send a message when the command /help is issued."""
    print("Received HELP query")
    update.message.reply_text('/get <N> <L> where N - class grade L - class letter')


def echo(update, context):
    """Echo the user message."""
    update.message.reply_text(update.message.text)


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def author(update, context):
    sMessage = 'Jury A Kondratyev'
    update.message.reply_text(sMessage)


def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    token = sMyToken
    updater = Updater(token, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("get", get))
    dp.add_handler(CommandHandler("help", help))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
