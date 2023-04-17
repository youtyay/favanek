import telebot
bot = telebot.TeleBot('6234331500:AAG2Hcuep4y4N58uuJeXrHnjbpaSyrpXk3c')
with open('subs.txt', 'r') as sublist:
    sublist = sublist.read()
    sublist = sublist.split('\n')
try:
    for i in sublist:
        bot.send_message(i, 'УРА')
except:
      pass
