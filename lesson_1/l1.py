import telebot

bot = telebot.TeleBot('7738822411:AAFbIwBf6dr1oCWhJgsStLcm8dmn4KUmwEs')

@bot.message_handler(commands=['start'])
def start_command(message):
    bot.reply_to(message, "Привет! Я бот.")
    bot.send_message(message.chat.id, "Чем могу помочь?")

@bot.message_handler(content_types=['text'])
def handle_text(message):
    if message.text.lower() == "привет":
        bot.send_message(message.chat.id, f"Здравствуйте, {message.from_user.first_name}!")
    else:
        bot.reply_to(message, "Я вас понял")

bot.polling(none_stop=True)