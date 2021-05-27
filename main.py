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
        'Для начала викторины наберите /go.\n' +
        'Для получения помощи наберите /help.'
    )


@bot.message_handler(commands=['go'])
def go_command(message):
    global isRunning
    if not isRunning:
        isRunning = True
        bot.send_message(
            message.chat.id,
            'Так будет начинаться викторина.\n' +
            'id:' + str(message.from_user.id) + '\n' +
            'username: ' + message.from_user.username + '\n' +
            'first_name + last_name ' + message.from_user.first_name + ' ' + message.from_user.last_name
        )
        isRunning = False


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
