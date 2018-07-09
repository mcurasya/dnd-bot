import time
import telebot
import constants
from rolls import *
import logging
import json
name = ''
abilities = {}
bot = telebot.TeleBot(constants.token)
log_bot = telebot.TeleBot(constants.log_token)


def next_step(message):
    global abilities
    with open('names_and_surnames\\abilities.json', 'r', encoding='utf-8') as f:
        s = f.read()
        abilities = json.loads(s, encoding='utf-8')
    user_markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
    user_markup.row('roll dice', 'generate name')
    user_markup.row('add name', 'add surname')
    user_markup.row('add ability', 'show ability')
    bot.send_message(message.from_user.id, 'select next move', reply_markup=user_markup)
    del message


@bot.message_handler(commands=['start'])
def handle_start(message):
    users = open('names_and_surnames\\users.txt', 'r', encoding='utf-8').read().strip().split()
    if message.from_user.first_name not in users:
        log_bot.send_message(constants.my_id, 'new user {}'.format(message.from_user.first_name))
        new_user(message)
    user_markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
    user_markup.row('roll dice', 'generate name')
    user_markup.row('add name', 'add surname')
    user_markup.row('add ability', 'show ability')
    bot.send_message(message.from_user.id, 'some text', reply_markup=user_markup)


@bot.message_handler(content_types=['text'])
def handle_message(message):
    if message.text == 'roll dice':
        handle_roll(message)
    elif message.text == 'generate name':
        handle_generation(message)
    elif message.text == 'add name':
        handle_add_name(message)
    elif message.text == 'add surname':
        handle_add_surname(message)
    elif message.text == 'add ability':
        handle_add_ability(message)
    elif message.text == 'show ability':
        handle_show_ability(message)
    else:
        bot.send_message(message.from_user.id, 'извините, я не знаю эту комманду')


def handle_roll(message):
    log_bot.send_message(constants.my_id, message.from_user.first_name + ' rolls dice')
    print(message.from_user.first_name + ' rolls dice')
    msg = bot.send_message(message.from_user.id, 'введите кубик в формате XdY или XкY')
    bot.register_next_step_handler(msg, process_dice_roll)


def process_dice_roll(message):
    try:
        n, die = map(int, message.text.strip().lower().split('d', 'к', ' '))
        x, s = multiple_roll(die, n)
        bot.send_message(message.from_user.id, 'you rolled {}, sum is {}'.format(x, s))
        bot.send_message(constants.dm_id, '{} rolled {}, sum is {}'.format(message.from_user.first_name, x, s))
        log_bot.send_message(constants.my_id, '{} rolled {}, sum is {}'.format(message.from_user.first_name, x, s))
        print(x, s)
    except ValueError as e:
        print(e)
        bot.send_message(message.from_user.id, "извините, вы ввели что то не так")
        log_bot.send_message(constants.my_id, message.from_user.first_name + ' made a mistake')
    next_step(message)


def handle_generation(message):
    log_bot.send_message(constants.my_id, message.from_user.first_name + ' generates name')
    print(message.from_user.first_name + ' generates name')
    name = generate_name()
    bot.send_message(message.from_user.id, name)
    log_bot.send_message(constants.my_id, message.from_user.first_name + ' generated ' + name)
    next_step(message)


def handle_add_name(message):
    log_bot.send_message(constants.my_id, message.from_user.first_name + ' adds name')
    print(message.from_user.first_name + ' adds name')
    msg = bot.send_message(message.from_user.id, 'введите имя, если хотите добавить несколько имен, введите их через пробел')
    bot.register_next_step_handler(msg, process_add_name)


def handle_add_surname(message):
    log_bot.send_message(constants.my_id, message.from_user.first_name + 'adds surname')
    print(message.from_user.first_name + ' adds surname')
    msg = bot.send_message(message.from_user.id, 'введите фамилию, если хотите добавить несколько фамилий, введите их через запятую')
    bot.register_next_step_handler(msg, process_add_surname)


def process_add_surname(message):
    txt = message.text
    surnames = add_sur(txt)
    log_bot.send_message(constants.my_id, message.from_user.first_name + ' adds surnames' + surnames)
    next_step(message)


def process_add_name(message):
    txt = message.text
    names = add_name(txt)
    log_bot.send_message(constants.my_id, message.from_user.first_name + ' adds names' + names)
    next_step(message)


def new_user(message):
    """add user that uses bot first time"""
    with open('names_and_surnames\\users.txt', 'a', encoding='utf-8') as f:
        f.write(message.from_user.first_name+' ')


def handle_add_ability(message):
    log_bot.send_message(constants.my_id, '{} adds ability'.format(message.from_user.first_name))
    msg = bot.send_message(message.from_user.id, 'введите название способности')
    bot.register_next_step_handler(msg, process_add_ability_name)


def process_add_ability_name(message):
    global name
    name = message.text
    if name not in abilities.keys():
        msg = bot.send_message(message.from_user.id, 'введите описание способности')
        bot.register_next_step_handler(msg, process_add_ability_description)
    else:
        bot.send_message(message.from_user.id, 'извините, такая способность уже есть')
        next_step(message)


def process_add_ability_description(message):
    abilities[name.strip().lower()] = message.text.strip().lower()
    sorted_abilities = sort_dict(abilities)
    s = json.dumps(sorted_abilities)
    with open('names_and_surnames\\abilities.json', 'w', encoding='utf-8') as f:
        f.write(s)
    next_step(message)


def handle_show_ability(message):
    for name in abilities.keys():
        bot.send_message(message.from_user.id, name)
    msg = bot.send_message(message.from_user.id, 'введите название способности')
    bot.register_next_step_handler(msg, process_show_ability)


def process_show_ability(message):
    log_bot.send_message(constants.my_id, '{} looks for ability'.format(message.from_user.first_name))
    if message.text.strip().lower() in abilities:
        bot.send_message(message.from_user.id, abilities[message.text.strip().lower()])
    else:
        bot.send_message(message.from_user.id, 'извините, я не знаю эту способность')
    next_step(message)


while True:
    try:
        with open('names_and_surnames\\abilities.json', 'r', encoding='utf-8') as f:
            s = f.read()
            abilities = json.loads(s, encoding='utf-8')
        bot.polling(none_stop=True)
    except Exception as e:
        print(e)
        time.sleep(3)
        logging.error(e)