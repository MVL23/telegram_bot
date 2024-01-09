import telebot
import Test_sql
import chdata
import time

token_moonaviebot = '6243786271:AAFhj7aPcXma6O43E7AbT_hlxemEjMhLhRQ'
token_debaggingbot = '6003425774:AAE0myNh7RrDQpFqCiYAHA1YVx6n02qgyWg'
bot = telebot.TeleBot(token_debaggingbot)


# Занесение данных о продаже
@bot.message_handler(content_types=['text'], commands=['Лот', 'лот', 'Лоты', 'лоты'])
def get_text_messages(message):
    strk = message.text
    st = [i for i in strk.split('\n')]
    DATA_SQLite = []

    # Проверка введенных данных
    Flag_item = False
    Flag_price = False
    Flag_date = False
    Flag_commens = False

    # Проверка номера лота
    num_item = [j for j in st[0].split()]
    if num_item[0].lower() == '/лот':
        for n in num_item:
            if n.isdigit():
                DATA_SQLite.append(n)
                Flag_item = True
                break
            if n[0] == 'О':
                DATA_SQLite.append(n)
                Flag_item = True
                break
    elif num_item[0].lower() == '/лоты':
        num_start = st[0].find(' ')
        DATA_SQLite.append(str(st[0][num_start + 1:]))
        Flag_item = True
    else:
        Flag_item == False
        bot.send_message(
            message.chat.id, "Данные номера лота введены с ошибкой!")

    # Проверка стоимости лота
    st[1] = st[1].lower()
    num_price = st[1].strip()
    if num_price.find('р') or num_price.find('руб'):
        x = num_price.find('р')
        num_price = num_price[:x]
        num_price = num_price.strip()
        if num_price.isdigit():
            DATA_SQLite.append(int(num_price))
            Flag_price = True
        else:
            Flag_item == False
            bot.send_message(
                message.chat.id, "Данные стоимости лота введены с ошибкой!")
    elif num_price.isdigit():
        DATA_SQLite.append(int(num_price))
        Flag_price = True

    # проверка даты оплаты
    in_data = [int(m) for m in st[2].split('.')]
    if len(in_data) == 3 and str(in_data[0]).isdigit() and str(in_data[1]).isdigit() and str(in_data[2]).isdigit():
        dey = chdata.date_import()
        dey_counter = dey[2] * 10000 + dey[1] * 100 + dey[0]
        in_data_counter = in_data[2] * 10000 + in_data[1] * 100 + in_data[0]
        if in_data[2] // 100 == 0:
            in_data[2] = in_data[2] + 2000

        if dey_counter >= in_data_counter:
            DATA_SQLite.append(int(in_data[0]))
            DATA_SQLite.append(int(in_data[1]))
            DATA_SQLite.append(int(in_data[2]))
            Flag_date = True
        else:
            Flag_date = False
            bot.send_message(
                message.chat.id, "Данные о дате оплаты лота введены с ошибкой!")
    else:
        Flag_date == False
        bot.send_message(
            message.chat.id, "Данные о дате оплаты лота введены с ошибкой! ")

    if len(st) > 3:

        if len(st) == 4:
            if st[3].startswith('Доставка') or st[3].startswith('доставка'):
                delivery = [d for d in st[3].split()]
                if delivery[1].isdigit():
                    DATA_SQLite.append(int(delivery[1]))
                    DATA_SQLite.append('полная')
                    Flag_commens = True
                else:
                    y = delivery[1].find('р')
                    if delivery[1][:y].isdigit():
                        DATA_SQLite.append(int(delivery[1][:y]))
                        DATA_SQLite.append('полная')
                        Flag_commens = True
                    else:
                        Flag_commens = False
                        bot.send_message(
                            message.chat.id, f"Не верно указана стоимость доставки")
            elif st[3].lower().startswith('частичная'):
                DATA_SQLite.append(0)
                DATA_SQLite.append('частичная')
                Flag_commens = True
            else:
                Flag_commens = False
                bot.send_message(
                    message.chat.id, f"Не верно указана стоимость доставки или частичная оплата")

        elif len(st) == 5:
            if (st[3].startswith('Доставка') or st[3].startswith('доставка')) and (st[4].lower().startswith('частичная')):
                delivery = [d for d in st[3].split(' ')]
                if delivery[1].isdigit():
                    DATA_SQLite.append(int(delivery[1]))
                    DATA_SQLite.append('частичная')
                    Flag_commens = True
                else:
                    y = delivery[1].find('р')
                    if delivery[1][:y].isdigit():
                        DATA_SQLite.append(int(delivery[1][:y]))
                        DATA_SQLite.append('частичная')
                        Flag_commens = True
                    else:
                        bot.send_message(
                            message.chat.id, f"Не верно указана стоимость доставки")
                        Flag_commens = False

    elif len(st) == 3:
        i = 0
        DATA_SQLite.append(int(i))
        DATA_SQLite.append('полная')
        Flag_commens = True

    if Flag_item and Flag_price and Flag_date and Flag_commens:
        if Test_sql.plus_data(DATA_SQLite):
            # time.sleep(1)
            bot.send_message(message.chat.id, "Успешно")
        else:
            bot.send_message(
                message.chat.id, f"Не получилось:(\nскорее всего лот {DATA_SQLite[0]} был продан раньше")


# Удаление данных
@bot.message_handler(content_types=['text'], commands=['Удалить', 'удалить'])
def delete_text_message(message):
    stroka = message.text
    n = stroka.find(' ')
    ni = stroka[n+1:]
    ni = ni.rstrip()
    if Test_sql.minus_data(ni):
        bot.send_message(message.chat.id, "Успешно")
    else:
        bot.send_message(
            message.chat.id, "Указанного лота нет в базе данных:(")


# Формирование отчета
month = {'январь': 1, 'февраль': 2, 'март': 3, 'апрель': 4, 'май': 5, 'июнь': 6,
         'июль': 7, 'август': 8, 'сентябрь': 9, 'октябрь': 10, 'ноябрь': 11, 'декабрь': 12}


@bot.message_handler(content_types=['text'], commands=['Отчет', 'отчет'])
def report_selling_month(message):
    user_id = message.from_user.id
    # первый id Оли, второй - мой
    if user_id == 1070288458 or user_id == 374798033:
        txt = message.text
        mess = [t for t in txt.split()]
        calendare = chdata.date_import()
        Year = int(calendare[2])
        if month.get(mess[1]) != None and mess[2].isdigit() and Year >= int(mess[2]):
            month_num = month[mess[1]]
            count_item, profin_month, delivery_month = Test_sql.report(
                month_num, mess[2])
            if count_item > 0 and profin_month > 0:
                bot.send_message(
                    message.from_user.id, f"Количество проданных лотов за {mess[1]} - {count_item}:\nна общую стоимость - {profin_month}\nна оплату доставок - {delivery_month}")
            else:
                bot.send_message(message.from_user.id,
                                 "Данные не обнаружены:(")
        else:
            bot.send_message(message.from_user.id,
                             "Месяц или год указан не правильно!")
    else:
        bot.send_message(message.chat.id, "У Вас нет прав доступа:(")


# Приветствие
@bot.message_handler(content_types=['text'], commands=['старт', 'Старт', 'Start', 'start'])
def start_bot(message):
    bot.send_message(message.chat.id, f"Привет, я Moonavie_bot!\n\tМеня создали для того, чтобы я помогал Оле.\n"
                     f"Сейчас объясню, как со мной взаимодействовать. И так приступим!\n"
                     f"Для начала расскажу о командах, они то и вызывают меня для работы.\n"
                     f"В настоящее время реализованы следующие команды:\n"
                     f"'/start'\n"
                     f"'/лот' или '/лоты'\n"
                     f"'/удалить'\n"
                     f"Команда '/start' как раз и вызвала меня, тут все понятно.\n"
                     f"Команда '/лот' - данную команду стоит использвать, когда оплата пришла за 1 конкретный лот.\n"
                     f"Команда '/лоты' - применяется, если было продано 2 и более лотов. Сейчас покажу структуру написания команды, пожалуйста, строго соблюдайте ее, иначе у меня возникнут проблемы при занесении Ваших данных в базу. Предположим, что у Вас продался лот с номером 9870 за 5000 рублей.\n"
                     f"Пример, как занести данные о продаже:\n"
                     f"\n"
                     f"/лот 9870\n"
                     f"5000 рублей\n"
                     f"08.08.2023\n"
                     f"\n"
                     f"Внимание, дату указывать только в таком формате 'дд.мм.гг' и год вводить полностью (то есть 2023 и т.д.)!!!\n"
                     f"Вот и все, 3 строчки и Вы передали мне данные:)\n"
                     f"Если продалось несколько лотов, то изменится только команда\n"
                     f"\n"
                     f"/лоты 12390, 12395, 14001\n"
                     f"\n"
                     f"Теперь рассмотрим случай, когда нужно добавить чуточку больше информации о продаже.\n"
                     f"Например, указать сколько стоит доставка. Для этого нужно в 4 строке написать:\n"
                     f"\n"
                     f"доставка 300 рублей\n"
                     f"\n"
                     f"К сожалению, по другому нельзя, не пойму я Вас, а мы же не хотим, чтобы между нами было недопонимание?:)\n"
                     f"Так же в 4 строке можно указать, что оплата частичная. Для этого просто указать:\n"
                     f"\n"
                     f"частичная\n"
                     f"\n"
                     f"Но запомни, если нужно написать стоимость доставки и оплачена только часть заказа то снача укажи, стоимость доставки, а только потом частичную оплату!\n"
                     f"полностью сообщение будет выгялдеть так:\n"
                     f"\n"
                     f"команда /лот или /лоты номер лота или номера через запятую с пробелом\n"
                     f"(сумма поступившая на карту) рублей\n"
                     f"дата поступления средст на катру\n"
                     f"Доставка (ее стоимость) рублей или частичная оплата\n"
                     f"частичная оплата\n"
                     f"\n"
                     f"Последние два поля не обязательные и заполняются по необходимости.\n"
                     f"Пример:\n"
                     f"\n"
                     f"/лоты 4562, 5690, 13990, 17432\n"
                     f"10000 рублей\n"
                     f"01.08.2023\n"
                     f"Доставка 500 рублей\n"
                     f"частичная\n"
                     f"\n"
                     f"Сдесь вроде бы все, надеюсь у нас не возникнет недопонимания!\n"
                     f"Ну и осталась последняя команда, удалить.\n"
                     f"Вызывается она следующим образом:\n"
                     f"/удалить (номер лота или лотов)\n"
                     f"Используй ее если неправильно ввел данные о продаже.\n"
                     f"Пример:\n"
                     f"\n"
                     f"/удалить 9870\n"
                     f"/удалить 4562, 5690, 13990, 17432\n"
                     f"\n"
                     f"Вот вроде бы о себе все рассказал:)")


def infinity_polling():
    while True:
        try:
            bot.polling(none_stop=True, interval=0)
        except Exception as a:
            print(a)
            time.sleep(5)
            pass


infinity_polling()
