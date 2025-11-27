import os
import telebot

dir_path = os.path.dirname(os.path.abspath(__file__))
logs_path = os.path.join(dir_path, "logs.txt")


bot = telebot.TeleBot("7738822411:AAFbIwBf6dr1oCWhJgsStLcm8dmn4KUmwEs")

hero = {
    "name": "Archer",
    "hp": 100,
    "max_hp": 100,
    "attack": 10,
    "defense": 5,
    "abilities": ["супер скорость"]  # список строк, например ["shield", "regen"]
}

enemy = {
    "name": "Goblin",
    "hp": 60,
    "attack": 8,
    "max_hp": 60,
    "defense": 3
}

def log_function(message):
    with open(logs_path, "a") as log_file:
        log_file.write(message + "\n")

def deal_damage(attacker, defender, send_message_func):
    damage = attacker["attack"] - defender["defense"]
    if damage < 0:
        damage = 0
    send_message_func(f"{attacker['name']} наносит {damage} урона {defender['name']}!")
    defender["hp"] -= damage
    
    if defender["hp"] <= 0:
        defender["hp"] = 0
        send_message_func(f"{defender['name']} повержен!")
    else:
        send_message_func(f"У {defender['name']} осталось {defender['hp']} HP.")

@bot.message_handler(commands=['start'])
def start_game(message):
    def send_message_func(text):
        bot.send_message(message.chat.id, text)
        log_function(text)
    
    send_message_func("Игра началась!")
    deal_damage(hero, enemy, send_message_func)
    deal_damage(enemy, hero, send_message_func)

bot.polling()
# Написать функцию лечения

def heal(character, amount, send_message_func):
    pass
# Написать функцию добавления спосностей герою "abilities": []

def add_ability(character, ability, send_message_func):
    pass
