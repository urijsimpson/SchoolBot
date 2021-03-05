import telebot
from telebot import types
from my_token import token

bot = telebot.TeleBot(token)

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

def letter_board():
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
            global gr_index
            gr_index = ClGr
            print(f"index: {gr_index}")
            bot.edit_message_text(chat_id=call.message.chat.id,
                                  message_id=call.message.message_id,
                                  text="enter the letter", reply_markup=letter_board())
        else:
            print("wrong")
            lLetterList = ["а", "б", "в", "г", "д", "е", "ж"]
            iterNum = 0
            for ClLet in lLetterList:
                iterNum += 1
                if msg == ClLet:
                    global let_index
                    let_index = iterNum
                    print(f"index: {let_index}")




bot.polling()
