import sqlite3
from telebot import types
import telebot
import random
import logging

#logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(name)s %(message)s')
logging.basicConfig(
    level=logging.DEBUG,
    filename='log.log',
    format='%(asctime)s %(levelname)s %(name)s %(message)s'
)

token = "6234331500:AAG2Hcuep4y4N58uuJeXrHnjbpaSyrpXk3c"
logging.info('Token successfully initted: ' + token)
bot = telebot.TeleBot(token)
logging.info("Bot successfully initted")
conn = sqlite3.connect('anek.db', check_same_thread=False)
c = conn.cursor()
logging.info("DB connected successfully, cursor created")


@bot.message_handler(commands=['start'])
def start(message):
    logging.info(str(message.chat.id) + " " + "@" + str(message.from_user.username) + " " + str(message.text))
    name = message.from_user.first_name
    bot.send_message(message.chat.id, f'''👋 <b>Привет, {name}! Я - Фаванек, твой проводник в мир самых 
смешных анекдотов!</b>

😂 <i><b>У меня в коллекции большое количество шуток, как авторских, так и самых популярных из Интернета :)</b></i>

<b>🙃 Я помогу тебе:
- Искать новые анекдоты
- Сохранять любимые анекдоты как в боте, так и в виде симпатичных картинок
- Предлагать свои анекдоты администрации
- Получать рассылку с новыми анекдотами</b>

#⃣ <i>Список команд:
[номер анекдота] - выслать анекдот под этим номером

/start - это сообщение

/rand - случайный анекдот

/fav [номер анекдота] - добавить конкретный анекдот в избранное

/unfav [номер анекдота] - аналогично предыдущей, но удаляет анекдот из избранного

/sub - подписаться на рассылку 

/unsub - отписаться от рассылки</i>

❗<b>ВНИМАНИЕ! Некоторые анекдоты могут содержать нецензурную лексику, чёрный юмор, неприемлемые темы. 
Мы не несём ответственность, если анекдот как-то задел вас и/или группу людей.</b>

🛠 <u><b>Технические вопросы к @anal_nosorog2009 и @Youtya_Youtyev</b></u>

😸 <b><i>Исходный код: https://github.com/YoutyaYoutyev/favanek</i></b>''', parse_mode='HTML')


@bot.message_handler(commands=['rand'])
def gen_rand_anek(message):
    logging.info(str(message.chat.id) + " " + "@" + str(message.from_user.username) + " " + str(message.text))
    try:
        rand = random.randint(1, 5)
        anek = c.execute('SELECT text FROM anek WHERE id=' + str(rand)).fetchall()
        bot.send_message(message.chat.id, 'Вот тебе анекдот из моей базы данных.')
        path = 'images/' + str(rand) + '.png'
        bot.send_photo(message.chat.id, open(path, 'rb'), caption=anek[0][0])
    except:
        bot.send_message(message.chat.id, 'Произошла ошибка.')


@bot.message_handler(content_types=['text'])
def anek_by_id(message):
    logging.info(str(message.chat.id) + " " + "@" + str(message.from_user.username) + " " + str(message.text))
    try:
        anek_id = message.text
        anek = c.execute('SELECT text FROM anek WHERE id=' + str(anek_id)).fetchall()
        bot.send_message(message.chat.id, 'Вот анекдот с указанным id:')
        path = 'images/' + message.text + '.png'
        bot.send_photo(message.chat.id, open(path, 'rb'), caption=anek[0][0])
    except:
        bot.send_message(message.chat.id, 'Такого анекдота нет. Попробуй другой id.')
        logging.error('Not found (anek_by_id)')


bot.polling()

if __name__ == '__main__':
    logging.info("Bot STOPPED")
