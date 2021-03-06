import telebot, sqlite3, sys
from telebot import types

bot = telebot.TeleBot("1639481970:AAHwStqKHlRDWv7UHZYEjEGNIKADcvIsv-s")

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
            if sString.split()[1].isdecimal():
                if int(sString.split()[1]) > 0 and int(sString.split()[1]) < 12:
                    sClassName = f"{sString.split()[0]} {sString.split()[1]}"
                    return sClassName
                else:
                    return f"Therea are non class {sString.split()[1]} here"
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
            if sString.split()[0] == '/get':
                iIndex = 1
            else:
                iIndex = 0
            if sString.split()[iIndex].isdecimal():
                if int(sString.split()[iIndex]) > 0 and int(sString.split()[iIndex]) < 12:
                    sClassName = f"{sString.split()[iIndex]} {sString.split()[iIndex + 1]}"
                else:
                    return ["Class grade must be between 1 - 11"]
            else:
                return ["Wrong format"]
            c = self.conn.cursor()
            c.execute(f"select count(*) from v_timetable where class = '{sClassName}'")
            iExists = int(c.fetchone()[0])
            if iExists == 0:
                return [f"Class {sClassName} doesn't exists in timetable"]
            else:
                sDow = sString.split()[iIndex + 2]

            c.execute(f"select count(*) from  v_timetable where class = '{sClassName}' and upper(day_of_week) like upper('{sDow}%')")

            iExists = int(c.fetchone()[0])
            if iExists == 0:
                return [f"No timetable for {sClassName} to {sDow}"]
            else:
                c.execute(f"select lesson_index, class, subject, tutor  from v_timetable where class = '{sClassName}' and upper(day_of_week) like upper( '{sDow}%')")

                for record in c.fetchall():
                    lRecordList.append(record)
                return lRecordList

        except ValueError as err:
            return ("ERROR", err)
        except OSError as err:
            return  ("ERROR", err)


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



@bot.message_handler(commands=["start"])
def welcome_handler(message):
    bot.send_message(message.chat.id, "choose the class grade", reply_markup=grade_board())
    print("sent start")


def grade_board():
    markup = types.InlineKeyboardMarkup()
    BtnClassGrade_10 = types.InlineKeyboardButton(text="10", callback_data="10")
    BtnClassGrade_9 = types.InlineKeyboardButton(text="9", callback_data="9")
    BtnClassGrade_8 = types.InlineKeyboardButton(text="8", callback_data="8")
    markup.add(BtnClassGrade_8, BtnClassGrade_9, BtnClassGrade_10)
    return markup


def letter_board():
    markup = types.InlineKeyboardMarkup()
    BtnClassLetter_a = types.InlineKeyboardButton(text="a", callback_data="а")
    BtnClassLetter_b = types.InlineKeyboardButton(text="b", callback_data="б")
    markup.add(BtnClassLetter_a, BtnClassLetter_b)
    return markup

def DOW_board():
    markup = types.InlineKeyboardMarkup()
    monday = types.InlineKeyboardButton(text="понедельник", callback_data="monday")
    tuesday = types.InlineKeyboardButton(text="вторник", callback_data="tuesday")
    wednesday = types.InlineKeyboardButton(text="среда", callback_data="wednesday")
    thursday = types.InlineKeyboardButton(text="четверг", callback_data="thursday")
    friday = types.InlineKeyboardButton(text="пятница", callback_data="friday")
    markup.add(monday, tuesday, wednesday, thursday, friday)
    return markup

def get_class_name(call, lClassName):
    try:
        iGrade = int(call.data)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text="choose the letter", reply_markup=letter_board())
        lClassName.insert(0, iGrade)
        return lClassName[0]

    except:

        sLetter = call.data
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text="choose the day of week", reply_markup=DOW_board())
        lClassName.append(sLetter)
        return lClassName[1]

@bot.callback_query_handler(func=lambda call: True)
def choose_class(call):
    lClassName = ['', '']
    lClassName = get_class_name(call, lClassName)
    print(lClassName)


bot.polling()
