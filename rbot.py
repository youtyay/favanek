import telebot
from telebot import types
from PIL import Image, ImageDraw


bot = telebot.TeleBot('5107161099:AAHPhk_Cxw8eVwGZ_fLvHqopY1-LSnhh51k')


booking_table = {
'1': True,
'2': True,
'3': True,
'4': True,
'5': True,
'6': True
}


ordered = False
removing = False
administration = False
admin_reg = False
admin_password = 'X84SEQ'
account = False


booking = dict()
count28, count29, count30, count31, count32, count33, count34 = 0, 0, 0, 0, 0, 0, 0
count21, count22, count23, count24, count25, count26, count27 = 0, 0, 0, 0, 0, 0, 0
count14, count15, count16, count17, count18, count19, count20 = 0, 0, 0, 0, 0, 0, 0
count8, count9, count10, count11, count12, count13 = 0, 0, 0, 0, 0, 0
count1, count2, count3, count4, count5, count6, count7 = 0, 0, 0, 0, 0, 0, 0
count35, count36, count37, count38, count39, count40, count41 = 0, 0, 0, 0, 0, 0, 0


def clean_places():
    places = Image.new("RGB", (600, 600), (0, 0, 0))
    draw = ImageDraw.Draw(places)
    draw.rectangle(((150, 200), (170, 220)), '#008000')
    draw.rectangle(((300, 200), (320, 220)), '#008000')
    draw.rectangle(((450, 200), (470, 220)), '#008000')
    draw.rectangle(((150, 400), (170, 420)), '#008000')
    draw.rectangle(((300, 400), (320, 420)), '#008000')
    draw.rectangle(((450, 400), (470, 420)), '#008000')
    places.save('places.png', "PNG")


def order_place(n):
    global ordered
    if ordered:
        places_with_order = Image.open('places_with_order.png')
    else:
        places_with_order = Image.open('places.png')
    draw = ImageDraw.Draw(places_with_order)
    if n == '1':
        draw.rectangle(((150, 200), (170, 220)), '#ff0000')
    elif n == '2':
        draw.rectangle(((300, 200), (320, 220)), '#ff0000')
    elif n == '3':
        draw.rectangle(((450, 200), (470, 220)), '#ff0000')
    elif n == '4':
        draw.rectangle(((150, 400), (170, 420)), '#ff0000')
    elif n == '5':
        draw.rectangle(((300, 400), (320, 420)), '#ff0000')
    elif n == '6':
        draw.rectangle(((450, 400), (470, 420)), '#ff0000')
    places_with_order.save('places_with_order.png', "PNG")


def order_remove(n):
    global ordered
    if ordered:
        places_with_order = Image.open('places_with_order.png')
    else:
        places_with_order = Image.open('places.png')
    draw = ImageDraw.Draw(places_with_order)
    if n == '1':
        draw.rectangle(((150, 200), (170, 220)), '#008000')
    elif n == '2':
        draw.rectangle(((300, 200), (320, 220)), '#008000')
    elif n == '3':
        draw.rectangle(((450, 200), (470, 220)), '#008000')
    elif n == '4':
        draw.rectangle(((150, 400), (170, 420)), '#008000')
    elif n == '5':
        draw.rectangle(((300, 400), (320, 420)), '#008000')
    elif n == '6':
        draw.rectangle(((450, 400), (470, 420)), '#008000')
    places_with_order.save('places_with_order.png', "PNG")


@bot.message_handler(commands=['start'])
def start(message):
    global account

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('Бронирование столика')
    btn2 = types.KeyboardButton('Оформить заказ')
    btn3 = types.KeyboardButton('О нашем заведении')
    btn4 = types.KeyboardButton('Корзина')
    admin_btn = types.KeyboardButton('Администратор')
    user_btn = types.KeyboardButton('Пользователь')
    markup.add(btn1, btn2, btn3, btn4)
    bot.send_message(message.chat.id,
                     text='Привет, {0.first_name}! Я бот, который поможет '
                          'тебе сделать заказ, забронировать столик в нашем '
                          'ресторане и не только :) Выбери из списка ниже '
                          'что тебя интересует'.format(message.from_user),
                     reply_markup=markup)
    if not account:
        markup.add(user_btn, admin_btn)
        bot.send_message(message.chat.id, text='Обязательно войдите в аккаунт!'.format(message.from_user),
                     reply_markup=markup)


def back_btn(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('Бронирование столика')
    btn2 = types.KeyboardButton('Оформить заказ')
    btn3 = types.KeyboardButton('О нашем заведении')
    btn4 = types.KeyboardButton('Корзина')
    markup.add(btn1, btn2, btn3, btn4)
    bot.send_message(message.chat.id,
                     text='Выбери из списка ниже, что тебя интересует'.format(message.from_user),
                     reply_markup=markup)


def after_text_2(message):
    bot.send_message(710029246, f'Адрес: {message.text}')
    if booking:
        bot.send_message(710029246, ''.join(str(booking).replace('{', '').replace('}', '').replace("'", '')))
        booking.clear()


@bot.message_handler(content_types=['text'])
def variations_of_otv(message):
    global ordered, removing, administration, admin_reg, account

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('Назад')
    btn_back = types.KeyboardButton('Назад')
    btn_order1 = types.KeyboardButton('Cтол №1')
    btn_order2 = types.KeyboardButton('Cтол №2')
    btn_order3 = types.KeyboardButton('Cтол №3')
    btn_order4 = types.KeyboardButton('Cтол №4')
    btn_order5 = types.KeyboardButton('Cтол №5')
    btn_order6 = types.KeyboardButton('Cтол №6')
    btn_order_rmv = types.KeyboardButton('Удалить стол')
    markup1 = types.InlineKeyboardMarkup()
    if message.text == 'О нашем заведении':
        if not account:
            bot.send_message(message.chat.id,
                             text='Войдите в аккаунт!'.format(message.from_user),
                             reply_markup=markup)
        else:
            markup.add(btn_back)
            bot.send_message(message.chat.id,
                             text='РЕСТОРАН ШАШЛЫК МАШЛЫК, в душе не знаю что'
                                  ' писать поэтому пусть будет'
                                  ' так'.format(message.from_user),
                             reply_markup=markup)

    elif message.text == 'Бронирование столика':
        if not account:
            bot.send_message(message.chat.id,
                             text='Войдите в аккаунт!'.format(message.from_user),
                             reply_markup=markup)
        else:
            if administration:
                markup.add(btn_order1, btn_order2, btn_order3, btn_order4, btn_order5, btn_order6, btn_order_rmv,
                           btn_back)
            else:
                markup.add(btn_order1, btn_order2, btn_order3, btn_order4, btn_order5, btn_order6, btn_back)
            clean_places()
            removing = False
            bot.send_message(message.chat.id, text='Вот все доступные места:'.format(message.from_user),
                             reply_markup=markup)
            if ordered:
                places_with_orders = Image.open("places_with_order.png", 'r')
                bot.send_photo(message.chat.id, photo=places_with_orders)
            else:
                places = Image.open("places.png", 'r')
                bot.send_photo(message.chat.id, photo=places)

    elif message.text == 'Корзина':
        if not account:
            bot.send_message(message.chat.id,
                             text='Войдите в аккаунт!'.format(message.from_user),
                             reply_markup=markup)
        else:
            btn2 = types.KeyboardButton('Оформление заказа')
            btn3 = types.KeyboardButton('Очистить корзину')
            markup.add(btn2, btn3, btn1)
            if booking:
                bot.send_message(message.chat.id,
                                 text=''.join(str(booking).replace('{', '').replace('}', '').replace("'", '')).format(
                                     message.from_user), reply_markup=markup)
            else:
                bot.send_message(message.chat.id, text='Корзина пуста'.format(message.from_user), reply_markup=markup)

    elif message.text == 'Очистить корзину':
        booking.clear()
        bot.send_message(message.chat.id, text='Корзина успешно очищена'.format(message.from_user), reply_markup=markup)

    elif message.text == 'Забронировать стол':
        bot.send_message(message.chat.id,
                         text='Выбирайте номер понравившегося стола :)'.format(message.from_user),
                         reply_markup=markup)

    elif 'Cтол' in message.text and not removing:
        n_table = message.text[-1].strip()
        if booking_table[n_table]:
            booking_table[n_table] = False
            order_place(n_table)
            ordered = True
            bot.send_message(message.chat.id,
                         text='Стол успешно забронирован!'.format(message.from_user), reply_markup=markup)
        else:
            bot.send_message(message.chat.id,
                             text='Стол уже забронирован'.format(message.from_user), reply_markup=markup)

    elif message.text == 'Удалить стол':
        if administration:
            markup.add(btn_order1, btn_order2, btn_order3, btn_order4, btn_order5, btn_order6, btn_back)
            removing = True
            bot.send_message(message.chat.id, text='Выберете стол для удаления'.format(message.from_user),
                         reply_markup=markup)
        else:
            bot.send_message(message.chat.id, text='Вы не являетесь администратором'.format(message.from_user),
                             reply_markup=markup)

    elif 'Cтол' in message.text and removing:
        n_table = message.text[-1].strip()
        if not booking_table[n_table]:
            booking_table[n_table] = True
            order_remove(n_table)
            ordered = True
            bot.send_message(message.chat.id,
                             text='Стол успешно удалён!'.format(message.from_user), reply_markup=markup)
        else:
            bot.send_message(message.chat.id,
                             text='Этот стол свободен'.format(message.from_user), reply_markup=markup)

    elif message.text == 'Администратор':
        bot.send_message(message.chat.id, text='Введите PIN-код'.format(message.from_user),
                         reply_markup=markup)
        markup.add(btn_back)
        admin_reg = True

    elif message.text == admin_password and admin_reg:
        bot.send_message(message.chat.id, text='Вы успешно вошли как администратор!'.format(message.from_user),
                         reply_markup=types.ReplyKeyboardRemove(), parse_mode='Markdown')
        administration = True
        account = True

        markup2 = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('Бронирование столика')
        btn2 = types.KeyboardButton('Оформить заказ')
        btn3 = types.KeyboardButton('О нашем заведении')
        markup2.add(btn1, btn2, btn3)

        bot.send_message(message.chat.id,
                         text='Выбери из списка ниже '
                              'что тебя интересует'.format(message.from_user),
                         reply_markup=markup2)

    elif message.text != admin_password and admin_reg:
        bot.send_message(message.chat.id, text='Неверный пароль'.format(message.from_user),
                         reply_markup=markup)

    elif message.text == 'Пользователь':
        bot.send_message(message.chat.id, text='Вы успешно вошли как пользователь!'.format(message.from_user),
                         reply_markup=types.ReplyKeyboardRemove(), parse_mode='Markdown')

        account = True

        markup3 = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('Бронирование столика')
        btn2 = types.KeyboardButton('Оформить заказ')
        btn3 = types.KeyboardButton('О нашем заведении')
        markup3.add(btn1, btn2, btn3)

        bot.send_message(message.chat.id,
                         text='Выбери из списка ниже '
                              'что тебя интересует'.format(message.from_user),
                         reply_markup=markup3)

    elif message.text == 'Оформление заказа':
        if booking:
            markup.add(btn1)
            m = bot.send_message(message.chat.id, text='Введите полный адрес по которому стоит доставить заказ'.format(
                message.from_user), reply_markup=markup)
            bot.register_next_step_handler(m, after_text_2)
        else:
            bot.send_message(message.chat.id, text='Чтобы оформить заказ нужно заполнить корзину'.format(
                message.from_user), reply_markup=markup)

    elif message.text == 'Оформить заказ':
        if not account:
            bot.send_message(message.chat.id,
                             text='Войдите в аккаунт!'.format(message.from_user),
                             reply_markup=markup)
        else:
            btn2 = types.KeyboardButton('Закуски горячие')
            btn3 = types.KeyboardButton('Закуски холодные')
            btn4 = types.KeyboardButton('Салаты')
            btn5 = types.KeyboardButton('Первые блюда')
            btn6 = types.KeyboardButton('Горячие блюда')
            btn7 = types.KeyboardButton('Напитки')
            markup.add(btn2, btn3, btn4, btn5, btn6, btn7, btn1)
            bot.send_message(message.chat.id,
                             text='Итак, выбери блюда из меню ниже'.format(message.from_user), reply_markup=markup)

    elif message.text == 'Закуски горячие':
        btn8 = types.KeyboardButton('Наггетсы')
        btn9 = types.KeyboardButton('Сулугуни жареный')
        btn10 = types.KeyboardButton('Жульен с грибами')
        btn11 = types.KeyboardButton('Жульен с крабовым мясом')
        btn12 = types.KeyboardButton('Шампиньоны, запеченные с сыром')
        btn13 = types.KeyboardButton('Кальмар в кляре')
        btn14 = types.KeyboardButton('Баклажаны, запеченные с сыром')
        markup.add(btn8, btn9, btn10, btn11, btn12, btn13, btn14, btn1)
        bot.send_message(message.chat.id,
                         text='Закуски горячие'.format(message.from_user), reply_markup=markup)

    elif message.text == 'Закуски холодные':
        btn8 = types.KeyboardButton('Канапе с колбасой и сыром')
        btn9 = types.KeyboardButton('Закуска «Павлиний хвост»')
        btn10 = types.KeyboardButton('Тарталетки со сливочным сыром, '
                                     'авокадо и красной рыбой')
        btn11 = types.KeyboardButton('Гренки с тунцом, яйцами и'
                                     ' маринованными огурцами')
        btn12 = types.KeyboardButton('Закуска из сельди и яиц')
        btn13 = types.KeyboardButton('«Коньячная» закуска')
        markup.add(btn8, btn9, btn10, btn11, btn12, btn13, btn1)
        bot.send_message(message.chat.id,
                         text='Закуски холодные'.format(message.from_user), reply_markup=markup)

    elif message.text == 'Салаты':
        btn8 = types.KeyboardButton('Салат с сухариками «Королевский»')
        btn9 = types.KeyboardButton('Салат «Чикаго» с копченой'
                                    ' курицей и грибами')
        btn10 = types.KeyboardButton('Салат с фасолью, помидорами и сыром')
        btn11 = types.KeyboardButton('Салат «Гнездо глухаря»')
        btn12 = types.KeyboardButton('Салат «Пармиджано»')
        btn13 = types.KeyboardButton('Салат с ананасами и курицей')
        btn14 = types.KeyboardButton('Салат «Мимоза»')
        markup.add(btn8, btn9, btn10, btn11, btn12, btn13, btn14, btn1)
        bot.send_message(message.chat.id,
                         text='Салаты'.format(message.from_user), reply_markup=markup)

    elif message.text == 'Первые блюда':
        btn8 = types.KeyboardButton('Суп «Харчо»')
        btn9 = types.KeyboardButton('Томатный суп с курицей, фасолью и '
                                    'овощами')
        btn10 = types.KeyboardButton('Суп «Затируха» с курицей')
        btn11 = types.KeyboardButton('Солянка сборная с колбасой')
        btn12 = types.KeyboardButton('Лагман с говядиной')
        btn13 = types.KeyboardButton('Щи «По-русски»')
        btn14 = types.KeyboardButton('Зелёный борщ со щавелем и яйцами')
        markup.add(btn8, btn9, btn10, btn11, btn12, btn13, btn14, btn1)
        bot.send_message(message.chat.id,
                         text='Первые блюда'.format(message.from_user), reply_markup=markup)

    elif message.text == 'Горячие блюда':
        btn8 = types.KeyboardButton('Шкмерули')
        btn9 = types.KeyboardButton('Чахохбили из курицы')
        btn10 = types.KeyboardButton('Лобио по-мегрельски')
        btn11 = types.KeyboardButton('Курица по-грузински')
        btn12 = types.KeyboardButton('Курица, запечённая с ежевичным'
                                     ' соусом')
        btn13 = types.KeyboardButton('Лобио с шампиньонами')
        btn14 = types.KeyboardButton('Аджапсандал (в духовке)')
        markup.add(btn8, btn9, btn10, btn11, btn12, btn13, btn14, btn1)
        bot.send_message(message.chat.id,
                         text='Горячие блюда'.format(message.from_user), reply_markup=markup)

    elif message.text == 'Напитки':
        btn8 = types.KeyboardButton('Чача')
        btn9 = types.KeyboardButton('Вода газированная')
        btn10 = types.KeyboardButton('Вода без газа')
        btn11 = types.KeyboardButton('Вино красное')
        btn12 = types.KeyboardButton('Вино белое')
        btn13 = types.KeyboardButton('Чай черный')
        btn14 = types.KeyboardButton('Чай зеленый')
        markup.add(btn8, btn9, btn10, btn11, btn12, btn13, btn14, btn1)
        bot.send_message(message.chat.id,
                         text='Напитки'.format(message.from_user), reply_markup=markup)

    elif message.text == 'Наггетсы':
        btn2 = types.InlineKeyboardButton('+', callback_data='count1+')
        btn3 = types.InlineKeyboardButton('-', callback_data='count1-')
        markup1.add(btn2, btn3)
        bot.send_message(message.chat.id,
                         text='Наггетсы'.format(message.from_user), reply_markup=markup1)

    elif message.text == 'Сулугуни жареный':
        btn2 = types.InlineKeyboardButton('+', callback_data='count2+')
        btn3 = types.InlineKeyboardButton('-', callback_data='count2-')
        markup1.add(btn2, btn3)
        bot.send_message(message.chat.id,
                         text='Сулугуни жареный'.format(message.from_user), reply_markup=markup1)

    elif message.text == 'Жульен с грибами':
        btn2 = types.InlineKeyboardButton('+', callback_data='count3+')
        btn3 = types.InlineKeyboardButton('-', callback_data='count3-')
        markup1.add(btn2, btn3)
        bot.send_message(message.chat.id,
                         text='Жульен с грибами'.format(message.from_user), reply_markup=markup1)

    elif message.text == 'Жульен с крабовым мясом':
        btn2 = types.InlineKeyboardButton('+', callback_data='count4+')
        btn3 = types.InlineKeyboardButton('-', callback_data='count4-')
        markup1.add(btn2, btn3)
        bot.send_message(message.chat.id,
                         text='Жульен с крабовым мясом'.format(message.from_user), reply_markup=markup1)

    elif message.text == 'Шампиньоны, запеченные с сыром':
        btn2 = types.InlineKeyboardButton('+', callback_data='count5+')
        btn3 = types.InlineKeyboardButton('-', callback_data='count5-')
        markup1.add(btn2, btn3)
        bot.send_message(message.chat.id,
                         text='Шампиньоны, запеченные с сыром'.format(message.from_user), reply_markup=markup1)

    elif message.text == 'Кальмар в кляре':
        btn2 = types.InlineKeyboardButton('+', callback_data='count6+')
        btn3 = types.InlineKeyboardButton('-', callback_data='count6-')
        markup1.add(btn2, btn3)
        bot.send_message(message.chat.id,
                         text='Кальмар в кляре'.format(message.from_user), reply_markup=markup1)

    elif message.text == 'Баклажаны, запеченные с сыром':
        btn2 = types.InlineKeyboardButton('+', callback_data='count7+')
        btn3 = types.InlineKeyboardButton('-', callback_data='count7-')
        markup1.add(btn2, btn3)
        bot.send_message(message.chat.id,
                         text='Баклажаны, запеченные с сыром'.format(message.from_user), reply_markup=markup1)

    elif message.text == 'Канапе с колбасой и сыром':
        btn2 = types.InlineKeyboardButton('+', callback_data='count8+')
        btn3 = types.InlineKeyboardButton('-', callback_data='count8-')
        markup1.add(btn2, btn3)
        bot.send_message(message.chat.id,
                         text='Канапе с колбасой и сыром'.format(message.from_user), reply_markup=markup1)

    elif message.text == 'Закуска «Павлиний хвост»':
        btn2 = types.InlineKeyboardButton('+', callback_data='count9+')
        btn3 = types.InlineKeyboardButton('-', callback_data='count9-')
        markup1.add(btn2, btn3)
        bot.send_message(message.chat.id,
                         text='Закуска «Павлиний хвост»'.format(message.from_user), reply_markup=markup1)

    elif message.text == 'Тарталетки со сливочным сыром, авокадо и красной рыбой':
        btn2 = types.InlineKeyboardButton('+', callback_data='count10+')
        btn3 = types.InlineKeyboardButton('-', callback_data='count10-')
        markup1.add(btn2, btn3)
        bot.send_message(message.chat.id,
                         text='Тарталетки со сливочным сыром, авокадо и красной рыбой'.format(message.from_user),
                         reply_markup=markup1)

    elif message.text == 'Гренки с тунцом, яйцами и маринованными огурцами':
        btn2 = types.InlineKeyboardButton('+', callback_data='count11+')
        btn3 = types.InlineKeyboardButton('-', callback_data='count11-')
        markup1.add(btn2, btn3)
        bot.send_message(message.chat.id,
                         text='Гренки с тунцом, яйцами и маринованными огурцами'.format(message.from_user),
                         reply_markup=markup1)

    elif message.text == 'Закуска из сельди и яиц':
        btn2 = types.InlineKeyboardButton('+', callback_data='count12+')
        btn3 = types.InlineKeyboardButton('-', callback_data='count12-')
        markup1.add(btn2, btn3)
        bot.send_message(message.chat.id,
                         text='Закуска из сельди и яиц'.format(message.from_user), reply_markup=markup1)

    elif message.text == '«Коньячная» закуска':
        btn2 = types.InlineKeyboardButton('+', callback_data='count13+')
        btn3 = types.InlineKeyboardButton('-', callback_data='count13-')
        markup1.add(btn2, btn3)
        bot.send_message(message.chat.id,
                         text='«Коньячная» закуска'.format(message.from_user), reply_markup=markup1)

    elif message.text == 'Салат с сухариками «Королевский»':
        btn2 = types.InlineKeyboardButton('+', callback_data='count14+')
        btn3 = types.InlineKeyboardButton('-', callback_data='count14-')
        markup1.add(btn2, btn3)
        bot.send_message(message.chat.id,
                         text='Салат с сухариками «Королевский»'.format(message.from_user), reply_markup=markup1)

    elif message.text == 'Салат «Чикаго» с копченой курицей и грибами':
        btn2 = types.InlineKeyboardButton('+', callback_data='count15+')
        btn3 = types.InlineKeyboardButton('-', callback_data='count15-')
        markup1.add(btn2, btn3)
        bot.send_message(message.chat.id,
                         text='Салат «Чикаго» с копченой курицей и грибами'.format(message.from_user),
                         reply_markup=markup1)

    elif message.text == 'Салат с фасолью, помидорами и сыром':
        btn2 = types.InlineKeyboardButton('+', callback_data='count16+')
        btn3 = types.InlineKeyboardButton('-', callback_data='count16-')
        markup1.add(btn2, btn3)
        bot.send_message(message.chat.id,
                         text='Салат с фасолью, помидорами и сыром'.format(message.from_user), reply_markup=markup1)

    elif message.text == 'Салат «Гнездо глухаря»':
        btn2 = types.InlineKeyboardButton('+', callback_data='count17+')
        btn3 = types.InlineKeyboardButton('-', callback_data='count17-')
        markup1.add(btn2, btn3)
        bot.send_message(message.chat.id,
                         text='Салат «Гнездо глухаря»'.format(message.from_user), reply_markup=markup1)

    elif message.text == 'Салат «Пармиджано»':
        btn2 = types.InlineKeyboardButton('+', callback_data='count18+')
        btn3 = types.InlineKeyboardButton('-', callback_data='count18-')
        markup1.add(btn2, btn3)
        bot.send_message(message.chat.id,
                         text='Салат «Пармиджано»'.format(message.from_user), reply_markup=markup1)

    elif message.text == 'Салат с ананасами и курицей':
        btn2 = types.InlineKeyboardButton('+', callback_data='count19+')
        btn3 = types.InlineKeyboardButton('-', callback_data='count19-')
        markup1.add(btn2, btn3)
        bot.send_message(message.chat.id,
                         text='Салат с ананасами и курицей'.format(message.from_user), reply_markup=markup1)

    elif message.text == 'Салат «Мимоза»':
        btn2 = types.InlineKeyboardButton('+', callback_data='count20+')
        btn3 = types.InlineKeyboardButton('-', callback_data='count20-')
        markup1.add(btn2, btn3)
        bot.send_message(message.chat.id,
                         text='Салат «Мимоза»'.format(message.from_user), reply_markup=markup1)

    elif message.text == 'Суп «Харчо»':
        btn2 = types.InlineKeyboardButton('+', callback_data='count21+')
        btn3 = types.InlineKeyboardButton('-', callback_data='count21-')
        markup1.add(btn2, btn3)
        bot.send_message(message.chat.id,
                         text='Суп «Харчо»'.format(message.from_user), reply_markup=markup1)

    elif message.text == 'Томатный суп с курицей, фасолью и овощами':
        btn2 = types.InlineKeyboardButton('+', callback_data='count22+')
        btn3 = types.InlineKeyboardButton('-', callback_data='count22-')
        markup1.add(btn2, btn3)
        bot.send_message(message.chat.id,
                         text='Томатный суп с курицей, фасолью и овощами'.format(message.from_user),
                         reply_markup=markup1)

    elif message.text == 'Суп «Затируха» с курицей':
        btn2 = types.InlineKeyboardButton('+', callback_data='count23+')
        btn3 = types.InlineKeyboardButton('-', callback_data='count23-')
        markup1.add(btn2, btn3)
        bot.send_message(message.chat.id,
                         text='Суп «Затируха» с курицей'.format(message.from_user), reply_markup=markup1)

    elif message.text == 'Солянка сборная с колбасой':
        btn2 = types.InlineKeyboardButton('+', callback_data='count24+')
        btn3 = types.InlineKeyboardButton('-', callback_data='count24-')
        markup1.add(btn2, btn3)
        bot.send_message(message.chat.id,
                         text='Солянка сборная с колбасой'.format(message.from_user), reply_markup=markup1)

    elif message.text == 'Лагман с говядиной':
        btn2 = types.InlineKeyboardButton('+', callback_data='count25+')
        btn3 = types.InlineKeyboardButton('-', callback_data='count25-')
        markup1.add(btn2, btn3)
        bot.send_message(message.chat.id,
                         text='Лагман с говядиной'.format(message.from_user), reply_markup=markup1)

    elif message.text == 'Щи «По-русски»':
        btn2 = types.InlineKeyboardButton('+', callback_data='count26+')
        btn3 = types.InlineKeyboardButton('-', callback_data='count26-')
        markup1.add(btn2, btn3)
        bot.send_message(message.chat.id,
                         text='Щи «По-русски»'.format(message.from_user), reply_markup=markup1)

    elif message.text == 'Зелёный борщ со щавелем и яйцами':
        btn2 = types.InlineKeyboardButton('+', callback_data='count27+')
        btn3 = types.InlineKeyboardButton('-', callback_data='count27-')
        markup1.add(btn2, btn3)
        bot.send_message(message.chat.id,
                         text='Зелёный борщ со щавелем и яйцами'.format(message.from_user), reply_markup=markup1)

    elif message.text == 'Шкмерули':
        btn2 = types.InlineKeyboardButton('+', callback_data='count28+')
        btn3 = types.InlineKeyboardButton('-', callback_data='count28-')
        markup1.add(btn2, btn3)
        bot.send_message(message.chat.id,
                         text='Шкмерули'.format(message.from_user), reply_markup=markup1)

    elif message.text == 'Чахохбили из курицы':
        btn2 = types.InlineKeyboardButton('+', callback_data='count29+')
        btn3 = types.InlineKeyboardButton('-', callback_data='count29-')
        markup1.add(btn2, btn3)
        bot.send_message(message.chat.id,
                         text='Чахохбили из курицы'.format(message.from_user), reply_markup=markup1)

    elif message.text == 'Лобио по-мегрельски':
        btn2 = types.InlineKeyboardButton('+', callback_data='count30+')
        btn3 = types.InlineKeyboardButton('-', callback_data='count30-')
        markup1.add(btn2, btn3)
        bot.send_message(message.chat.id,
                         text='Лобио по-мегрельски'.format(message.from_user), reply_markup=markup1)

    elif message.text == 'Курица по-грузински':
        btn2 = types.InlineKeyboardButton('+', callback_data='count31+')
        btn3 = types.InlineKeyboardButton('-', callback_data='count31-')
        markup1.add(btn2, btn3)
        bot.send_message(message.chat.id,
                         text='Курица по-грузински'.format(message.from_user), reply_markup=markup1)

    elif message.text == 'Курица, запечённая с ежевичным соусом':
        btn2 = types.InlineKeyboardButton('+', callback_data='count32+')
        btn3 = types.InlineKeyboardButton('-', callback_data='count32-')
        markup1.add(btn2, btn3)
        bot.send_message(message.chat.id,
                         text='Курица, запечённая с ежевичным соусом'.format(message.from_user),
                         reply_markup=markup1)

    elif message.text == 'Лобио с шампиньонами':
        btn2 = types.InlineKeyboardButton('+', callback_data='count33+')
        btn3 = types.InlineKeyboardButton('-', callback_data='count33-')
        markup1.add(btn2, btn3)
        bot.send_message(message.chat.id,
                         text='Лобио с шампиньонами'.format(message.from_user), reply_markup=markup1)

    elif message.text == 'Аджапсандал (в духовке)':
        btn2 = types.InlineKeyboardButton('+', callback_data='count34+')
        btn3 = types.InlineKeyboardButton('-', callback_data='count34-')
        markup1.add(btn2, btn3)
        bot.send_message(message.chat.id,
                         text='Аджапсандал (в духовке)'.format(message.from_user), reply_markup=markup1)

    elif message.text == 'Чача':
        btn2 = types.InlineKeyboardButton('+', callback_data='count35+')
        btn3 = types.InlineKeyboardButton('-', callback_data='count35-')
        markup1.add(btn2, btn3)
        bot.send_message(message.chat.id,
                         text='Чача'.format(message.from_user), reply_markup=markup1)

    elif message.text == 'Вода газированная':
        btn2 = types.InlineKeyboardButton('+', callback_data='count36+')
        btn3 = types.InlineKeyboardButton('-', callback_data='count36-')
        markup1.add(btn2, btn3)
        bot.send_message(message.chat.id,
                         text='Вода газированная'.format(message.from_user), reply_markup=markup1)

    elif message.text == 'Вода без газа':
        btn2 = types.InlineKeyboardButton('+', callback_data='count37+')
        btn3 = types.InlineKeyboardButton('-', callback_data='count37-')
        markup1.add(btn2, btn3)
        bot.send_message(message.chat.id,
                         text='Вода без газа'.format(message.from_user), reply_markup=markup1)

    elif message.text == 'Вино красное':
        btn2 = types.InlineKeyboardButton('+', callback_data='count38+')
        btn3 = types.InlineKeyboardButton('-', callback_data='count38-')
        markup1.add(btn2, btn3)
        bot.send_message(message.chat.id,
                         text='Вино красное'.format(message.from_user), reply_markup=markup1)

    elif message.text == 'Вино белое':
        btn2 = types.InlineKeyboardButton('+', callback_data='count39+')
        btn3 = types.InlineKeyboardButton('-', callback_data='count39-')
        markup1.add(btn2, btn3)
        bot.send_message(message.chat.id,
                         text='Вино белое'.format(message.from_user), reply_markup=markup1)

    elif message.text == 'Чай черный':
        btn2 = types.InlineKeyboardButton('+', callback_data='count40+')
        btn3 = types.InlineKeyboardButton('-', callback_data='count40-')
        markup1.add(btn2, btn3)
        bot.send_message(message.chat.id,
                         text='Чай черный'.format(message.from_user), reply_markup=markup1)

    elif message.text == 'Чай зеленый':
        btn2 = types.InlineKeyboardButton('+', callback_data='count41+')
        btn3 = types.InlineKeyboardButton('-', callback_data='count41-')
        markup1.add(btn2, btn3)
        bot.send_message(message.chat.id,
                         text='Чай зеленый'.format(message.from_user), reply_markup=markup1)

    elif message.text == 'Назад':
        back_btn(message)

    else:
        bot.send_message(message.chat.id,
                         text='Я тебя не понимаю, попробуй снова'.format(message.from_user), reply_markup=markup)

    @bot.callback_query_handler(func=lambda call: True)
    def callback_inline(call):
        global count1, count2, count3, count4, count5, count6, count7, count8, \
            count9, count10, count11, count11, count12, count13, count14, \
            count15, count16, count17, count18, count19, count20, count20, \
            count21, count22, count23, count24, count25, count26, count27, \
            count28, count29, count30, count31, count32, count33, count34, \
            count35, count36, count37, count38, count39, count40, count41
        if call.data == 'count1+':
            count1 += 1
            bot.send_message(message.chat.id, 'Успешно добавлено!')
            booking['Наггетсы'] = count1
        elif call.data == 'count1-':
            if count1 > 0:
                count1 -= 1
                bot.send_message(message.chat.id, 'Успешно удалено!')
                booking['Наггетсы'] = count1

        if call.data == 'count2+':
            count2 += 1
            bot.send_message(message.chat.id, 'Успешно добавлено!')
            booking['Сулугуни жареный'] = count2
        elif call.data == 'count2-':
            if count2 > 0:
                count2 -= 1
                bot.send_message(message.chat.id, 'Успешно удалено!')
                booking['Сулугуни жареный'] = count2

        if call.data == 'count3+':
            count3 += 1
            bot.send_message(message.chat.id, 'Успешно добавлено!')
            booking['Жульен с грибами'] = count3
        elif call.data == 'count3-':
            if count3 > 0:
                count3 -= 1
                bot.send_message(message.chat.id, 'Успешно удалено!')
                booking['Жульен с грибами'] = count3

        if call.data == 'count4+':
            count4 += 1
            bot.send_message(message.chat.id, 'Успешно добавлено!')
            booking['Жульен с крабовым мясом'] = count4
        elif call.data == 'count4-':
            if count4 > 0:
                count4 -= 1
                bot.send_message(message.chat.id, 'Успешно удалено!')
                booking['Жульен с крабовым мясом'] = count4

        if call.data == 'count5+':
            count5 += 1
            bot.send_message(message.chat.id, 'Успешно добавлено!')
            booking['Шампиньоны, запеченные с сыром'] = count5
        elif call.data == 'count5-':
            if count5 > 0:
                count5 -= 1
                bot.send_message(message.chat.id, 'Успешно удалено!')
                booking['Шампиньоны, запеченные с сыром'] = count5

        if call.data == 'count6+':
            count6 += 1
            bot.send_message(message.chat.id, 'Успешно добавлено!')
            booking['Кальмар в кляре'] = count6
        elif call.data == 'count6-':
            if count6 > 0:
                count6 -= 1
                bot.send_message(message.chat.id, 'Успешно удалено!')
                booking['Кальмар в кляре'] = count6

        if call.data == 'count7+':
            count7 += 1
            bot.send_message(message.chat.id, 'Успешно добавлено!')
            booking['Баклажаны, запеченные с сыром'] = count7
        elif call.data == 'count7-':
            if count7 > 0:
                count7 -= 1
                bot.send_message(message.chat.id, 'Успешно удалено!')
                booking['Баклажаны, запеченные с сыром'] = count7

        if call.data == 'count8+':
            count8 += 1
            bot.send_message(message.chat.id, 'Успешно добавлено!')
            booking['Канапе с колбасой и сыром'] = count8
        elif call.data == 'count8-':
            if count8 > 0:
                count8 -= 1
                bot.send_message(message.chat.id, 'Успешно удалено!')
                booking['Канапе с колбасой и сыром'] = count8

        if call.data == 'count9+':
            count9 += 1
            bot.send_message(message.chat.id, 'Успешно добавлено!')
            booking['Закуска «Павлиний хвост»'] = count9
        elif call.data == 'count9-':
            if count9 > 0:
                count9 -= 1
                bot.send_message(message.chat.id, 'Успешно удалено!')
                booking['Закуска «Павлиний хвост»'] = count9

        if call.data == 'count10+':
            count10 += 1
            bot.send_message(message.chat.id, 'Успешно добавлено!')
            booking['Тарталетки со сливочным сыром, авокадо и красной рыбой'] = count10
        elif call.data == 'count10-':
            if count10 > 0:
                count10 -= 1
                bot.send_message(message.chat.id, 'Успешно удалено!')
                booking['Тарталетки со сливочным сыром, авокадо и красной рыбой'] = count10

        if call.data == 'count11+':
            count11 += 1
            bot.send_message(message.chat.id, 'Успешно добавлено!')
            booking['Гренки с тунцом, яйцами и маринованными огурцами'] = count11
        elif call.data == 'count11-':
            if count11 > 0:
                count11 -= 1
                bot.send_message(message.chat.id, 'Успешно удалено!')
                booking['Гренки с тунцом, яйцами и маринованными огурцами'] = count11

        if call.data == 'count12+':
            count12 += 1
            bot.send_message(message.chat.id, 'Успешно добавлено!')
            booking['Закуска из сельди и яиц'] = count12
        elif call.data == 'count12-':
            if count12 > 0:
                count12 -= 1
                bot.send_message(message.chat.id, 'Успешно удалено!')
                booking['Закуска из сельди и яиц'] = count12

        if call.data == 'count13+':
            count13 += 1
            bot.send_message(message.chat.id, 'Успешно добавлено!')
            booking['«Коньячная» закуска'] = count13
        elif call.data == 'count13-':
            if count13 > 0:
                count13 -= 1
                bot.send_message(message.chat.id, 'Успешно удалено!')
                booking['«Коньячная» закуска'] = count13

        if call.data == 'count14+':
            count14 += 1
            bot.send_message(message.chat.id, 'Успешно добавлено!')
            booking['Салат с сухариками «Королевский»'] = count14
        elif call.data == 'count14-':
            if count14 > 0:
                count14 -= 1
                bot.send_message(message.chat.id, 'Успешно удалено!')
                booking['Салат с сухариками «Королевский»'] = count14

        if call.data == 'count15+':
            count15 += 1
            bot.send_message(message.chat.id, 'Успешно добавлено!')
            booking['Салат «Чикаго» с копченой курицей и грибами'] = count15
        elif call.data == 'count15-':
            if count15 > 0:
                count15 -= 1
                bot.send_message(message.chat.id, 'Успешно удалено!')
                booking['Салат «Чикаго» с копченой курицей и грибами'] = count15

        if call.data == 'count16+':
            count16 += 1
            bot.send_message(message.chat.id, 'Успешно добавлено!')
            booking['Салат с фасолью, помидорами и сыром'] = count16
        elif call.data == 'count16-':
            if count16 > 0:
                count16 -= 1
                bot.send_message(message.chat.id, 'Успешно удалено!')
                booking['Салат с фасолью, помидорами и сыром'] = count16

        if call.data == 'count17+':
            count17 += 1
            bot.send_message(message.chat.id, 'Успешно добавлено!')
            booking['Салат «Гнездо глухаря»'] = count17
        elif call.data == 'count17-':
            if count17 > 0:
                count17 -= 1
                bot.send_message(message.chat.id, 'Успешно удалено!')
                booking['Салат «Гнездо глухаря»'] = count17

        if call.data == 'count18+':
            count18 += 1
            bot.send_message(message.chat.id, 'Успешно добавлено!')
            booking['Салат «Пармиджано»'] = count18
        elif call.data == 'count18-':
            if count18 > 0:
                count18 -= 1
                bot.send_message(message.chat.id, 'Успешно удалено!')
                booking['Салат «Пармиджано»'] = count18

        if call.data == 'count19+':
            count19 += 1
            bot.send_message(message.chat.id, 'Успешно добавлено!')
            booking['Салат с ананасами и курицей'] = count19
        elif call.data == 'count19-':
            if count19 > 0:
                count19 -= 1
                bot.send_message(message.chat.id, 'Успешно удалено!')
                booking['Салат с ананасами и курицей'] = count19

        if call.data == 'count20+':
            count20 += 1
            bot.send_message(message.chat.id, 'Успешно добавлено!')
            booking['Салат «Мимоза»'] = count20
        elif call.data == 'count20-':
            if count20 > 0:
                count20 -= 1
                bot.send_message(message.chat.id, 'Успешно удалено!')
                booking['Салат «Мимоза»'] = count20

        if call.data == 'count21+':
            count21 += 1
            bot.send_message(message.chat.id, 'Успешно добавлено!')
            booking['Суп «Харчо»'] = count21
        elif call.data == 'count21-':
            if count21 > 0:
                count21 -= 1
                bot.send_message(message.chat.id, 'Успешно удалено!')
                booking['Суп «Харчо»'] = count21

        if call.data == 'count22+':
            count22 += 1
            bot.send_message(message.chat.id, 'Успешно добавлено!')
            booking['Томатный суп с курицей, фасолью и овощами'] = count22
        elif call.data == 'count22-':
            if count22 > 0:
                count22 -= 1
                bot.send_message(message.chat.id, 'Успешно удалено!')
                booking['Томатный суп с курицей, фасолью и овощами'] = count22

        if call.data == 'count23+':
            count23 += 1
            bot.send_message(message.chat.id, 'Успешно добавлено!')
            booking['Суп «Затируха» с курицей'] = count23
        elif call.data == 'count23-':
            if count23 > 0:
                count23 -= 1
                bot.send_message(message.chat.id, 'Успешно удалено!')
                booking['Суп «Затируха» с курицей'] = count23

        if call.data == 'count24+':
            count24 += 1
            bot.send_message(message.chat.id, 'Успешно добавлено!')
            booking['Солянка сборная с колбасой'] = count24
        elif call.data == 'count24-':
            if count24 > 0:
                count24 -= 1
                bot.send_message(message.chat.id, 'Успешно удалено!')
                booking['Солянка сборная с колбасой'] = count24

        if call.data == 'count25+':
            count25 += 1
            bot.send_message(message.chat.id, 'Успешно добавлено!')
            booking['Лагман с говядиной'] = count25
        elif call.data == 'count25-':
            if count25 > 0:
                count25 -= 1
                bot.send_message(message.chat.id, 'Успешно удалено!')
                booking['Лагман с говядиной'] = count25

        if call.data == 'count26+':
            count26 += 1
            bot.send_message(message.chat.id, 'Успешно добавлено!')
            booking['Щи «По-русски»'] = count26
        elif call.data == 'count26-':
            if count26 > 0:
                count26 -= 1
                bot.send_message(message.chat.id, 'Успешно удалено!')
                booking['Щи «По-русски»'] = count26

        if call.data == 'count27+':
            count27 += 1
            bot.send_message(message.chat.id, 'Успешно добавлено!')
            booking['Зелёный борщ со щавелем и яйцами'] = count27
        elif call.data == 'count27-':
            if count27 > 0:
                count27 -= 1
                bot.send_message(message.chat.id, 'Успешно удалено!')
                booking['Зелёный борщ со щавелем и яйцами'] = count27

        if call.data == 'count28+':
            count28 += 1
            bot.send_message(message.chat.id, 'Успешно добавлено!')
            booking['Шкмерули'] = count28
        elif call.data == 'count28-':
            if count28 > 0:
                count28 -= 1
                bot.send_message(message.chat.id, 'Успешно удалено!')
                booking['Шкмерули'] = count28

        if call.data == 'count29+':
            count29 += 1
            bot.send_message(message.chat.id, 'Успешно добавлено!')
            booking['Чахохбили из курицы'] = count29
        elif call.data == 'count29-':
            if count29 > 0:
                count29 -= 1
                bot.send_message(message.chat.id, 'Успешно удалено!')
                booking['Чахохбили из курицы'] = count29

        if call.data == 'count30+':
            count30 += 1
            bot.send_message(message.chat.id, 'Успешно добавлено!')
            booking['Лобио по-мегрельски'] = count30
        elif call.data == 'count30-':
            if count30 > 0:
                count30 -= 1
                bot.send_message(message.chat.id, 'Успешно удалено!')
                booking['Лобио по-мегрельски'] = count30

        if call.data == 'count31+':
            count31 += 1
            bot.send_message(message.chat.id, 'Успешно добавлено!')
            booking['Курица по-грузински'] = count31
        elif call.data == 'count31-':
            if count31 > 0:
                count31 -= 1
                bot.send_message(message.chat.id, 'Успешно удалено!')
                booking['Курица по-грузински'] = count31

        if call.data == 'count32+':
            count32 += 1
            bot.send_message(message.chat.id, 'Успешно добавлено!')
            booking['Курица, запечённая с ежевичным соусом'] = count32
        elif call.data == 'count32-':
            if count32 > 0:
                count32 -= 1
                bot.send_message(message.chat.id, 'Успешно удалено!')
                booking['Курица, запечённая с ежевичным соусом'] = count32

        if call.data == 'count33+':
            count33 += 1
            bot.send_message(message.chat.id, 'Успешно добавлено!')
            booking['Лобио с шампиньонами'] = count33
        elif call.data == 'count33-':
            if count33 > 0:
                count33 -= 1
                bot.send_message(message.chat.id, 'Успешно удалено!')
                booking['Лобио с шампиньонами'] = count33

        if call.data == 'count34+':
            count34 += 1
            bot.send_message(message.chat.id, 'Успешно добавлено!')
            booking['Аджапсандал (в духовке)'] = count34
        elif call.data == 'count34-':
            if count34 > 0:
                count34 -= 1
                bot.send_message(message.chat.id, 'Успешно удалено!')
                booking['Аджапсандал (в духовке)'] = count34

        if call.data == 'count35+':
            count35 += 1
            bot.send_message(message.chat.id, 'Успешно добавлено!')
            booking['Чача'] = count35
        elif call.data == 'count35-':
            if count35 > 0:
                count35 -= 1
                bot.send_message(message.chat.id, 'Успешно удалено!')
                booking['Чача'] = count35

        if call.data == 'count36+':
            count36 += 1
            bot.send_message(message.chat.id, 'Успешно добавлено!')
            booking['Вода газированная'] = count36
        elif call.data == 'count36-':
            if count36 > 0:
                count36 -= 1
                bot.send_message(message.chat.id, 'Успешно удалено!')
                booking['Вода газированная'] = count36

        if call.data == 'count37+':
            count37 += 1
            bot.send_message(message.chat.id, 'Успешно добавлено!')
            booking['Вода без газа'] = count37
        elif call.data == 'count37-':
            if count37 > 0:
                count37 -= 1
                bot.send_message(message.chat.id, 'Успешно удалено!')
                booking['Вода без газа'] = count37

        if call.data == 'count38+':
            count38 += 1
            bot.send_message(message.chat.id, 'Успешно добавлено!')
            booking['Вино красное'] = count38
        elif call.data == 'count38-':
            if count38 > 0:
                count38 -= 1
                bot.send_message(message.chat.id, 'Успешно удалено!')
                booking['Вино красное'] = count38

        if call.data == 'count39+':
            count39 += 1
            bot.send_message(message.chat.id, 'Успешно добавлено!')
            booking['Вино белое'] = count39
        elif call.data == 'count39-':
            if count39 > 0:
                count39 -= 1
                bot.send_message(message.chat.id, 'Успешно удалено!')
                booking['Вино белое'] = count39

        if call.data == 'count40+':
            count40 += 1
            bot.send_message(message.chat.id, 'Успешно добавлено!')
            booking['Чай черный'] = count40
        elif call.data == 'count40-':
            if count40 > 0:
                count40 -= 1
                bot.send_message(message.chat.id, 'Успешно удалено!')
                booking['Чай черный'] = count40

        if call.data == 'count41+':
            count41 += 1
            bot.send_message(message.chat.id, 'Успешно добавлено!')
            booking['Чай зеленый'] = count41
        elif call.data == 'count41-':
            if count41 > 0:
                count41 -= 1
                bot.send_message(message.chat.id, 'Успешно удалено!')
                booking['Чай зеленый'] = count41


bot.polling(none_stop=True)