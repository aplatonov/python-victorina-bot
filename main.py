import telebot
import config
import time as tm
from telebot import types
from dbhelper.dbhelper import DBHelper

bot = telebot.TeleBot(config.TOKEN)
isRunning = False

db = DBHelper()
db.setup()
db.disconnect()


@bot.message_handler(commands=['start'])
def start_command(message):
	start_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
	start_markup.row('/start', '/help', '/hide')
	start_markup.row('/go', '/info', '/obnull')
	bot.send_message(message.chat.id, "Бот запущен!\nВведите /help для просмотра помощи.")
	bot.send_message(message.from_user.id, "Добавлена клавиатура!\nНажмите /hide чтобы убрать клавиатуру ", reply_markup=start_markup)

@bot.message_handler(commands=['hide'])
def hide_command(message):
	hide_markup = telebot.types.ReplyKeyboardRemove()
	bot.send_message(message.chat.id, 'Клавиатура убрана.\nВведите /start чтобы ее вернуть.', reply_markup=hide_markup)


@bot.message_handler(commands=['help'])
def help_command(message):
    bot.send_message(
        message.chat.id,
        'Вы можете поучаствовать в викторине.\n' +
        'Для получения вопроса наберите /go.\n' +
        'Посмотреть свою статистику /info.\n' +
        'Сбросить прогресс пользователя /obnull.\n' +
        'Для получения помощи наберите /help.'
    )


@bot.message_handler(commands=['info'])
def start_command(message):
    user_id = message.from_user.id
    username = message.from_user.username
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    info = db.get_info(user_id)
    if info != None:
        bot.send_message(
            message.chat.id,
            'Пользователь ' + first_name + ' ' + last_name + ' (id: ' + str(user_id) + ', ' + username + '):\n' +
            '\t- вопросов: ' + str(info.get("count")) + '\n' +
            '\t- заработано баллов: ' + str(info.get("sum"))
    )


@bot.message_handler(commands=['obnull'])
def start_command(message):
    user_id = message.from_user.id
    db.reset_progress(user_id)
    bot.send_message(
        message.chat.id,
        'Прогресс пользователя сброшен'
    )


@bot.message_handler(commands=['go'])
def go_command(message):
    global isRunning
    if not isRunning:
        isRunning = True
        current_try = 0
        user_id = message.from_user.id
        username = message.from_user.username
        first_name = message.from_user.first_name
        last_name = message.from_user.last_name
        db.upsert_user(user_id, first_name, last_name, username)
        questions = db.get_questions_for_user(user_id, int(1))
        if len(questions) == 0:
            sent = bot.send_message(
                message.chat.id,
                'Пользователь ответил на все вопросы. Сбросьте прогресс, чтобы начать заново.'
            )
        else:
            bot.send_message(
                message.chat.id,
                'Вопрос для ' + first_name + ' ' + last_name + ':'
            )
            question = questions[0]
            sent = bot.send_message(message.chat.id, question[1])
            bot.register_next_step_handler(sent, process_question, question, current_try)
        isRunning = False


def process_question(message, question, current_try):
    user_id = message.from_user.id
    current_try += 1
    if message.text.lower() != str(question[2]).lower():
        if current_try < config.MAX_TRY:
            sent = bot.send_message(
                message.chat.id,
                'Неверно, попробуйте еще. Осталось попыток: ' +
                str(config.MAX_TRY - current_try) +
                '\n' +
                question[1]
            )
            bot.register_next_step_handler(sent, process_question, question, current_try)
        else:
            db.upsert_user_points(user_id, int(question[0]), 0)
            bot.send_message(message.chat.id, 'Вы исчерпали все попытки.')
    elif message.text.lower() == str(question[2]).lower() and current_try <= config.MAX_TRY:
        points = int(question[3]) // current_try
        db.upsert_user_points(user_id, int(question[0]), points)
        bot.send_message(message.chat.id, 'Верно, заработано баллов: {}'.format(points))


@bot.message_handler(content_types=['text'])
def text_handler(message):
    text = message.text.lower()
    chat_id = message.chat.id
    if text == "привет":
        bot.send_message(
            chat_id,
            'Привет, ' + message.from_user.first_name + ' ' + message.from_user.last_name + ', я бот викторины.'
        )
    elif text == "как дела?":
        bot.send_message(chat_id, 'Хорошо, а у тебя?')
    else:
        bot.send_message(chat_id, 'Я еще не очень интеллектуален, всего не знаю')


# bot.polling(none_stop=True)
while True:
	try:
		bot.infinity_polling(True)
	except Exception:
		tm.sleep(1)