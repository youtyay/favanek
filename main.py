import sqlite3
import random
import telebot

# Настройки бота
token = '6234331500:AAG2Hcuep4y4N58uuJeXrHnjbpaSyrpXk3c'
bot = telebot.TeleBot(token)

# Создаем подключение к базе данных
db = sqlite3.connect("anek.db")
cur = db.cursor()


# Обработка команды /start
@bot.message_handler(commands=['start'])
def start_command(message):
    bot.send_message(message.chat.id, 'Привет, давай пошутим! Отправь мне любое число от 1 до 10, чтобы узнать анекдот.')


# Обрабатываем присланное пользователем число
@bot.message_handler(content_types=['text'])
def anek_command(message):
    if message.text.isdigit():
        number = int(message.text)
        if 0 < number <= 10:
            query = 'SELECT * FROM anek WHERE id=?'
            cur.execute(query, (number,))
            anek = cur.fetchone()
            # Отправляем сообщение с анекдотом
            bot.send_message(message.chat.id, anek[2])
        else:
            bot.send_message(message.chat.id, 'Отправь мне число от 1 до 10, чтобы узнать анекдот.')
    else:
        bot.send_message(message.chat.id, 'Отправь мне число от 1 до 10, чтобы узнать анекдот.')


# Обработка команды /rand
@bot.message_handler(commands=['rand'])
def anek_rand_command(message):
    # Получаем случайный id анекдота
    rand_num = random.randint(1, 10)
    # Получаем анекдот из базы по id
    query = 'SELECT * FROM anek WHERE id=?'
    cur.execute(query, (rand_num,))
    anek = cur.fetchone()
    # Отправляем сообщение со случайным анекдотом
    bot.send_message(message.chat.id, anek[2])


# Запуск бота
bot.polling()
