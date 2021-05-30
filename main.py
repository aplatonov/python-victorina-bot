import telebot
import config
from dbhelper.dbhelper import DBHelper

bot = telebot.TeleBot(config.TOKEN)
isRunning = False

db = DBHelper()
db.setup()
db.disconnect()


@bot.message_handler(commands=['start', 'help'])
def start_command(message):
    bot.send_message(
        message.chat.id,
        'Вы можете поучаствовать в викторине.\n' +
        'Для получения вопроса наберите /go.\n' +
        'ПОсмотреть свою статистику /info.\n' +
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
            '\t-вопросов: ' + str(info.get("count")) + '\n' +
            '\t-заработано баллов: ' + str(info.get("sum"))
    )


@bot.message_handler(commands=['go'])
def go_command(message):
    global isRunning
    if not isRunning:
        isRunning = True
        current_try = 1
        user_id = message.from_user.id
        username = message.from_user.username
        first_name = message.from_user.first_name
        last_name = message.from_user.last_name
        bot.send_message(
            message.chat.id,
            'Вопрос для ' + first_name + ' ' + last_name + ':'
        )
        db.upsert_user(user_id, first_name, last_name, username)
        question = db.get_questions_for_user(user_id, int(1))[0]
        sent = bot.send_message(message.chat.id, question[1])
        bot.register_next_step_handler(sent, process_question, question, current_try)
        isRunning = False


def process_question(message, question, current_try):
    user_id = message.from_user.id
    if current_try > config.MAX_TRY:
        db.upsert_user_points(user_id, int(question[0]), 0)
        bot.send_message(message.chat.id, 'Вы исчерпали все попытки.')
        return

    if message.text.lower() != str(question[2]).lower():
        current_try += 1
        sent = bot.send_message(
            message.chat.id,
            'Неверно, попробуйте еще. Осталось попыток: ' +
            str(config.MAX_TRY - current_try + 1) +
            '\n' +
            question[1]
        )
        bot.register_next_step_handler(sent, process_question, question, current_try)
        return
    points = int(question[3]) // current_try
    db.upsert_user_points(user_id, int(question[0]), points)
    bot.send_message(message.chat.id, 'Верно, заработано баллов {}'.format(points))


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


bot.polling(none_stop=True)
