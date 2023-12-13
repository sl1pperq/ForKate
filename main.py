import telebot
from telebot import types
import json

bot = telebot.TeleBot('')
lessons = []
users = []

try:
    with open('lessons.json', 'r') as file:
        lessons = json.loads(file.read())
    with open('users.json', 'r') as file:
        users = json.loads(file.read())
except Exception as e:
    print(e)


def save_data():
    with open('lessons.json', 'w') as file:
        file.write(json.dumps(lessons, ensure_ascii=False))
    with open('users.json', 'w') as file:
        file.write(json.dumps(users, ensure_ascii=False))


@bot.message_handler(commands=['start', 'help'])
def start(message):
    chat_id = message.chat.id
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    class_10t = types.KeyboardButton("10Т")
    class_10i = types.KeyboardButton("10И")
    markup.add(class_10t, class_10i)
    m = bot.send_message(chat_id, 'Привет! В каком ты классе?', reply_markup=markup)
    bot.register_next_step_handler(m, know_user_class)


def know_user_class(message):
    chat_id = message.chat.id
    user_class = message.text
    if user_class == "10Т" or user_class == "10И":
        users.append({
            "id": chat_id,
            "class": user_class
        })
        save_data()
        bot.send_message(chat_id, 'Вы успешно завершили регистрацию', reply_markup=types.ReplyKeyboardRemove())
    else:
        m = bot.send_message(chat_id, 'Повторите попытку')
        bot.register_next_step_handler(m, know_user_class)


@bot.message_handler(commands=['rasp'])
def rasp(message):
    chat_id = message.chat.id
    uroks = return_lessons(return_user_class(chat_id))
    for urok in uroks:
        bot.send_message(chat_id, f'{urok["name"]}, каб. {urok["room"]}\n{urok["teacher"]}')

def return_user_class(chat_id):
    for user in users:
        if user['id'] == chat_id:
            return user['class']

def return_lessons(class_name):
    for lesson in lessons:
        if lesson['class'] == class_name:
            return lesson['lessons']



bot.polling()
