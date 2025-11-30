import os
import json
import telebot

dir_path = os.path.dirname(os.path.abspath(__file__))


bot = telebot.TeleBot("7949321674:AAGKjVDCG3vt6f56_agEuItSIgvbKir9n1Q")
list_path = os.path.join(dir_path, "wishlist.json")
wishlist = {}

def start_bot():
    global wishlist
    with open(list_path, "r") as file:
        wishlist = json.load(file)

def add_to_wish_list(user_name):
    if user_name not in wishlist:
        wishlist[user_name] = []
        with open(list_path, "w") as file:
            json.dump(wishlist, file)
        

@bot.message_handler(commands=["start"])
def start_handler(message):
    user_name = message.from_user.username
    add_to_wish_list(user_name)
    bot.send_message(message.chat.id, f"Привет, {user_name}! Твой список желаний готов.")
    bot.send_message(message.chat.id, "Используй /add_wish чтобы добавить желание \n и /get_my_wish_list чтобы посмотреть свой список.")

@bot.message_handler(commands=["get_my_wish_list"])
def get_my_wish_list_handler(message):
    user_name = message.from_user.username
    if len(wishlist[user_name]) == 0:
        bot.send_message(message.chat.id, f"Твой список желаний пуст.")
    else:
        listt = wishlist.get(user_name)
        st = "Твой список желаний:\n"

        for i, item in enumerate(listt, start=1):
            st += f"{i}. {item}\n"

        bot.send_message(message.chat.id, st)

#добавить функцию просмотр листа друга, пользователь пишет /get_my_friends_list username_друга
#бот отвечает списком желаний друга

@bot.message_handler(commands=["add_wish"])
def add_wish_handler(message):
    pass

start_bot()
bot.polling()