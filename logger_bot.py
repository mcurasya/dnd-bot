import logging
import telebot
import constants
import time
import json
log_bot = telebot.TeleBot(constants.log_token)
abilities = {}


def next_step(message):
    if message.from_user.id == constants.my_id:
        user_markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True)
        user_markup.add('/users', '/names', '/surnames', '/abilities')
        log_bot.send_message(constants.my_id, 'логгирование', reply_markup=user_markup)
    else:
        log_bot.send_message(message.from_user.id, 'извините, этот бот не для вас')


@log_bot.message_handler(commands='start')
def start_handler(message):
    if message.from_user.id == constants.my_id:
        user_markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True)
        user_markup.add('/users', '/names', '/surnames', '/abilities')
        log_bot.send_message(constants.my_id, 'логгирование', reply_markup=user_markup)
    else:
        log_bot.send_message(message.from_user.id, 'извините, этот бот не для вас')


@log_bot.message_handler(commands='users')
def users_handler(message):
    with open('names_and_surnames\\users.txt', 'r', encoding='utf-8') as f:
        users = f.read().strip().split(' ')
        for user in users:
            log_bot.send_message(constants.my_id, user)


@log_bot.message_handler(commands='names')
def names_handler(message):
    with open('names_and_surnames\\names.txt', 'r', encoding='utf-8') as f:
        names= f.read().strip().split(' ')
        for name in names:
            log_bot.send_message(constants.my_id, name)


@log_bot.message_handler(commands='surnames')
def names_handler(message):
    with open('names_and_surnames\\surnames.txt', 'r', encoding='utf-8') as f:
        names = list(map(str.strip, filter(None, f.read().strip().split(','))))
        for name in names:
            log_bot.send_message(constants.my_id, name)


@log_bot.message_handler(commands='abilities')
def abilities_handler(message):
    global  abilities
    markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True)
    with open('names_and_surnames\\abilities.json', 'r', encoding='utf-8') as f:
        s = f.read()
        abilities = json.loads(s)
        for name in abilities:
            markup.add(name)
            log_bot.send_message(constants.my_id, name)
    msg = log_bot.send_message(constants.my_id, 'выбери способность', reply_markup=markup)
    log_bot.register_next_step_handler(msg, process_ability)


def process_ability(message):
    log_bot.send_message(constants.my_id, abilities[message.text])
    next_step(message)


while True:
    try:
        log_bot.polling(none_stop=True)
    except Exception as e:
        print(e)
        time.sleep(3)
        logging.error(e)
