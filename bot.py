import psycopg2
import telebot
from telebot import types

import config

bot = telebot.TeleBot(config.TOKEN)


@bot.message_handler(commands=['start'])
def start_chat(message):
    bot.send_message(message.chat.id, f'Привет!Нажми на /help, что бы увидеть список команд!')


@bot.message_handler(commands=['add'])
def add(message):
    list_sports = 'Введите название спорта:\n'
    for i in config.view_sport:
        list_sports = list_sports + i + "\n"
    message_add = bot.send_message(message.chat.id, list_sports)
    bot.register_next_step_handler(message_add, choose_sport)
    

@bot.message_handler(commands=['remove'])
def remove(message):
    msg_remove = bot.send_message(message.chat.id, 'Введите название спорта:')
    bot.register_next_step_handler(msg_remove, choose_sport_remove)    


@bot.message_handler(commands=['help'])
def help(message):
    list_commands = 'Команды:\n'
    for i in config.view_commands:
        list_commands = list_commands + i + "\n"
    bot.send_message(message.chat.id, list_commands)


@bot.message_handler(commands=['list'])
def list_(message):
    rows = select_user(str(message.chat.id))
    list_add = ''
    if rows == None:
        list_add = 'У вас нет подписок!'
    else:
        list_add = 'Подписки:\n'
        for i in rows:
            list_add = list_add + f'{i[1]} - {i[2]}\n'
    bot.send_message(message.chat.id, list_add)


def choose_sport(message):
    try:
        chat_id = message.chat.id
        sport = message.text
        if sport == u'Футбол':
            user = config.User(sport)
            user.chat_id = chat_id
            config.user_dict[chat_id] = user
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
            markup.add('1 тайм', '2 тайм')
            msg = bot.reply_to(message, 'Выберите тайм:', reply_markup=markup)
            bot.register_next_step_handler(msg, choose_time)
        else:
            raise Exception()
    except Exception:
        bot.reply_to(message, 'ooops')


def choose_time(message):
    chat_id = message.chat.id
    time = message.text
    user = config.user_dict[chat_id]
    if (time == u'1 тайм') or (time == u'2 тайм'):
        user.gg = time
        reply = insert_user(str(user.chat_id), user.sport, user.gg)
        bot.send_message(chat_id, reply)


def insert_user(chat_id, sport, gg):
    conn = psycopg2.connect(config.link_db)
    conn.autocommit = True
    reply = ''
    cursor = conn.cursor()
    cursor.execute("select * from player where chat_id=%(str)s", {'str': chat_id})
    user_info = cursor.fetchall()
    if user_info == None:
        cursor.execute("insert into player values (%s,%s,%s)", (chat_id, sport, gg))
        cursor.close()
        conn.close()
        reply = 'Вы подписались на событие: '+sport+' '+gg
        return reply
    else:
        for row in user_info:
            if(row[1] == sport) and (row[2] == gg):
                reply = 'Вы уже подписаны на событие: '+sport+' '+gg
                return reply
    cursor.execute("insert into player values (%s,%s,%s)", (chat_id, sport, gg))
    cursor.close()
    conn.close()
    reply = 'Вы подписались на событие: '+sport+' '+gg
    return reply


def choose_sport_remove(message):
    chat_id = message.chat.id
    sport = message.text
    if sport == u'Футбол':
        reply = delete_user(chat_id, sport)
        bot.send_message(chat_id, reply)


def delete_user(chat_id, sport):
    conn = psycopg2.connect(config.link_db)
    conn.autocommit = True
    reply = ''
    cursor = conn.cursor()
    cursor.execute("delete from player where chat_id=%s and sport=%s", (str(chat_id), sport))
    user_info = cursor.rowcount
    if user_info == 0:
        reply = 'Вы не подписаны на событие: '+sport
    else:
        reply = 'Вы отписались от события: '+sport
    cursor.close()
    conn.close()
    return reply


def select_user(chat_id):
    conn = psycopg2.connect(config.link_db)
    cursor = conn.cursor()
    cursor.execute("select * from player where chat_id=%s", (chat_id,))
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows


bot.polling(none_stop=True)
