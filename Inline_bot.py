import telebot
from telebot import types

bot = telebot.TeleBot("1639481970:AAHwStqKHlRDWv7UHZYEjEGNIKADcvIsv-s")

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
    lGradeList = ["10", "9", "8", "7"]
    msg = call.data
    lClass = []
    for ClGr in lGradeList:
        if msg == ClGr:
            grade = ClGr
            # print(f"index: {grade}")
            bot.edit_message_text(chat_id=call.message.chat.id,
                                  message_id=call.message.message_id,
                                  text="enter the letter", reply_markup=letter_board())
            lClass.append(grade)
            # final_class(grade)

    lLetterList = ["а", "б", "в", "г", "д", "е", "ж"]
    iterNum = 0
    for ClLet in lLetterList:
        # iterNum += 1
        if msg == ClLet:
            letter = ClLet
            # print(f"index: {letter}")
            lClass.append(letter)
            # final_class(letter)

    for i in lClass:
        print(i)

# def final_class(cl):
#     lFinalClass = []
#     lFinalClass.append(cl)
#     # if len(lFinalClass) > 1:
#     print(lFinalClass.reverse())



bot.polling()
