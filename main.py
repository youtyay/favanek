import sqlite3
from telebot import types
import telebot
import random
import logging
import datetime
import sys

date_obj = datetime.datetime.now()
date = date_obj.strftime('%m-%d-%y-%H-%M-%S ')

# logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(name)s %(message)s')
logging.basicConfig(
    level=logging.DEBUG,
    filename=('logs/' + date + '.log'),
    format='%(asctime)s %(levelname)s %(name)s %(message)s'
)

token = "6234331500:AAG2Hcuep4y4N58uuJeXrHnjbpaSyrpXk3c"
logging.info('Token successfully initted: ' + token)
bot = telebot.TeleBot(token)
logging.info("Bot successfully initted")
conn = sqlite3.connect('anek.db', check_same_thread=False)
c = conn.cursor()
logging.info("DB connected successfully, cursor created")


def log(message): logging.info(str(message.chat.id) + " " + "@" + str(message.from_user.username
                                                                      if message.from_user.username else "None")
                               + " " + str(message.text))


@bot.message_handler(commands=['start'])
def start(message):
    log(message)
    bot.send_message(message.chat.id, f'''👋 <b>Привет, {message.from_user.full_name}! Я - Фаванек, твой проводник в мир 
самых смешных анекдотов!</b>

😂 <i><b>У меня в коллекции большое количество шуток, как авторских, так и самых популярных из Интернета :)</b></i>

<b>🙃 Я помогу тебе:
- Искать новые анекдоты
- Сохранять любимые анекдоты как в боте, так и в виде симпатичных картинок
- Предлагать свои анекдоты администрации
- Получать рассылку с новыми анекдотами</b>

❗<b>ВНИМАНИЕ! Некоторые анекдоты могут содержать нецензурную лексику, чёрный юмор, неприемлемые темы. 
Мы не несём ответственность, если анекдот как-то задел вас и/или группу людей.</b>

🛠 <u><b>Технические вопросы к @anal_nosorog2009 и @Youtya_Youtyev</b></u>

😸 <b><i>Исходный код: https://github.com/YoutyaYoutyev/favanek</i></b>''', parse_mode='HTML')


@bot.message_handler(commands=['help'])
def start(message):
    log(message)
    bot.send_message(message.chat.id, f'''#⃣ <i>Список команд:
[номер анекдота] - выслать анекдот под этим номером
/start - это сообщение
/rand - случайный анекдот
/fav - список избранных анекдотов
/sub - подписаться на рассылку 
/unsub - отписаться от рассылки
/suggest - предложить ваш анекдот :)</i>''', parse_mode='HTML')


@bot.message_handler(commands=['rand'])
def gen_rand_anek(message):
    log(message)
    try:
        rand = random.randrange(1, 10)
        markup = types.InlineKeyboardMarkup()
        add_fav_btn = types.InlineKeyboardButton(text='🌟 Добавить в избранное',
                                                 callback_data='add_fav ' + str(rand))
        markup.add(add_fav_btn)
        anek = c.execute('SELECT text FROM anek WHERE id=' + str(rand)).fetchall()
        bot.send_message(message.chat.id, 'Вот тебе анекдот из моей базы данных.')
        bot.send_photo(message.chat.id, open('images/' + str(rand) + '.png', 'rb'),
                       caption=("<b>#" + str(rand) + "\n \n</b>" + "<i>" + anek[0][0] + "</i>"), parse_mode='HTML',
                       reply_markup=markup)
    except Exception as e:
        logging.error("Ошибка > " + str(e))
        bot.send_message(message.chat.id, 'Произошла ошибка.')


@bot.callback_query_handler(func=lambda call: True)
def add_fav(call):
    if 'add_fav' in call.data:
        anek_id = call.data.split()[-1]
        user_id = call.message.from_user.id
        print(anek_id)
        add_fav_to_db(anek_id, user_id, call.message)


@bot.message_handler(commands=['suggest'])
def suggest_message(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Отмена")
    markup.add(btn1)
    bot.send_message(message.chat.id, 'Пожалуйста, введите Ваш анекдот. Если передумали - кнопка отмены в помощь',
                     reply_markup=markup)
    bot.register_next_step_handler(message, save_suggestion)


def save_suggestion(message):
    user_id = str(message.from_user.id)
    username = str(message.from_user.username)
    suggestion = str(message.text)
    if message.text != "Отмена":
        try:
            c.execute("INSERT INTO suggestions VALUES (NULL, ?,?,?)", (user_id, username, suggestion))
            conn.commit()
            bot.send_message(message.chat.id, 'Спасибо за Ваш анекдот, мы оценим его!')
        except Exception as e:
            logging.error("Ошибка > " + str(e))
            bot.send_message(message.chat.id, 'Попробуйте позже, ошибка!')
    else:
        bot.send_message(message.chat.id, 'Возвращайтесь, как передумаете ;)')


@bot.message_handler(commands=['sub'])
def subscribe(message):
    try:
        user_id = str(message.from_user.id)
        with open('subs.txt', 'r') as sublist:
            sublist = sublist.read()
            sublist = sublist.split('\n')
        if user_id in sublist:
            bot.send_message(message.chat.id, 'Вы уже подписаны на рассылку анекдотов :)')
        else:
            with open('subs.txt', 'r+') as sublist:
                sublist.write(user_id + "\n")
            bot.send_message(message.chat.id, 'Вы подписались на рассылку анекдотов :)')
    except Exception as e:
        bot.send_message(message.chat.id, 'Произошла ошибка.')
        logging.error("Ошибка > " + str(e))


@bot.message_handler(commands=['unsub'])
def unsubscribe(message):
    try:
        user_id = str(message.from_user.id)
        with open('subs.txt', 'r') as sublist:
            sublist = sublist.read()
            sublist = sublist.split('\n')
        if user_id not in sublist:
            bot.send_message(message.chat.id, 'Вы ещё не подписаны на рассылку анекдотов :)')
        else:
            with open('subs.txt', 'r') as sublist:
                sublisttext = sublist.read()
                sublistlist = sublisttext.split('\n')
                sublistlist.remove(user_id)
                tempstr = ""
            with open('subs.txt', 'w') as sublist:
                for i in sublistlist:
                    tempstr = tempstr + i + "\n"
                sublist.write(tempstr)
            bot.send_message(message.chat.id, 'Вы отписались от рассылки анекдотов :(')
    except Exception as e:
        bot.send_message(message.chat.id, 'Произошла ошибка.')
        logging.error("Ошибка > " + str(e))


@bot.message_handler(commands=['send'])
def sendm(message):
    try:
        user_id = str(message.from_user.id)
        with open("admins.txt", "r") as adminl:
            adminl = adminl.read()
            adminl = adminl.split("\n")
        if user_id in adminl:
            with open('subs.txt', 'r') as sublist:
                sublist = sublist.read()
                sublist = sublist.split('\n')
            try:
                for i in sublist:
                    bot.send_message(i, message.text[5:])
            except Exception:
                pass
        else:
            bot.send_message(message.chat.id, 'У вас недостаточно прав для выполнения этой команды :)')
    except Exception as e:
        bot.send_message(message.chat.id, 'Что-то пошло не так.')
        logging.error("Ошибка > " + str(e))


@bot.message_handler(commands=['botstop'])
def botstop(message):
    try:
        user_id = str(message.from_user.id)
        with open("admins.txt", "r") as adminl:
            adminl = adminl.read()
            adminl = adminl.split("\n")
        if user_id in adminl:
            sys.exit()
        else:
            bot.send_message(message.chat.id, 'У вас недостаточно прав для выполнения этой команды :)')
    except Exception as e:
        bot.send_message(message.chat.id, 'Что-то пошло не так.')
        logging.error("Ошибка > " + str(e))


@bot.message_handler(content_types=['text'])
def anek_by_id(message):
    log(message)
    try:
        markup = types.InlineKeyboardMarkup()
        add_fav_btn = types.InlineKeyboardButton(text='🌟 Добавить в избранное',
                                                 callback_data='add_fav ' + str(message.text))
        markup.add(add_fav_btn)
        anek = c.execute('SELECT text FROM anek WHERE id=' + str(message.text)).fetchall()
        bot.send_photo(message.chat.id, open('images/' + message.text + '.png', 'rb'),
                       caption=("<b>#" + message.text + "\n \n</b>" + "<i>" + anek[0][0] + "</i>"), parse_mode='HTML',
                       reply_markup=markup)
    except Exception as e:
        bot.send_message(message.chat.id, 'Неверная команда или ID анекдота.')
        logging.error("Ошибка > " + str(e))


@bot.callback_query_handler(func=lambda call: True)
def add_fav(call):
    if 'add_fav' in call.data:
        anek_id = call.data.split()[-1]
        user_id = call.message.from_user.id
        print(anek_id)
        add_fav_to_db(anek_id, user_id, call.message)


def add_fav_to_db(anek_id, user_id, message):
    global c, conn

    keyboard = types.InlineKeyboardMarkup()
    anek_id, user_id = str(anek_id), str(user_id)

    try:
        c.execute("SELECT id FROM user_fav WHERE id = ?", (user_id, ))
        if c.fetchone() is None:
            bot.send_message(message.chat.id, 'Успешно добавлено')
            c.execute("INSERT INTO user_fav VALUES (?, ?)", (user_id, anek_id))
            conn.commit()
        else:
            favs = c.execute('SELECT favs FROM user_fav WHERE id = ?', (user_id, )).fetchall()[0][0]
            favs = str(favs)
            if anek_id not in favs:
                favs += ' ' + anek_id
                c.execute('UPDATE user_fav SET favs = ? WHERE id = ?', (favs, user_id))
                conn.commit()
                bot.send_message(message.chat.id, 'Успешно добавлено', reply_markup=keyboard)
            else:
                bot.send_message(message.chat.id, 'Этот анекдот уже есть в избранном')
    except Exception as e:
        logging.error("Ошибка > " + str(e))
        bot.send_message(message.chat.id, 'Попробуйте позже, ошибка!')


bot.infinity_polling()

if __name__ == '__main__':
    logging.info("Bot STOPPED")
