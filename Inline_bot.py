import telebot
from telebot import types
from my_token import token

bot = telebot.Telebot(token)

@bot.message_handler(commands=["start"])
def welcome_handler(message):
    bot.send_message(message.chat.id, "choose the class grade", reply_markup=grade_board())
    print("sent start")


def grade_board():
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text="10", callback_data="10")
    btn2 = types.InlineKeyboardButton(text="9", callback_data="9")
    btn3 = types.InlineKeyboardButton(text="8", callback_data="8")
    markup.add(btn1, btn2, btn3)
    return markup

def letter_board(index):
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text="a", callback_data="а")
    btn2 = types.InlineKeyboardButton(text="b", callback_data="б")
    markup.add(btn1, btn2)
    return markup

@bot.callback_query_handler(func=lambda call: True)
def choose_grade(call):
    lGradeList = [10, 9, 8, 7, 6]
    msg = call.data
    for ClGr in lGradeList:
        if int(msg) == ClGr:
            index = ClGr
            print(f"index: {index}")
            return letter_board(index)
        else:
            print("wrong")


bot.polling()
