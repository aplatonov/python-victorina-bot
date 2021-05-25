import telebot
import config

bot = telebot.TeleBot(config.TOKEN)

@bot.message_handler(commands=['start'])
def start_command(message):
    bot.send_message(
        message.chat.id,
        'Поздравляем! Вы можете поучаствовать в викторине.\n' +
        'Для начала викторины наберите /go.\n' +
        'Для получения помощи наберите /help.'
    )

if __name__ == '__main__':
     bot.polling(none_stop=True)