import telebot
import cryptpars

bot = telebot.TeleBot(TOKEN)

keyboard1 = telebot.types.ReplyKeyboardMarkup(True, True)
keyboard1.row('Посмотреть список доступных криптовалют')


@bot.message_handler(content_types=['text'])
def send_information(message):
    if message.text == '/start':
        bot.send_message(message.chat.id, "I don't respond to any commands, just write name")
    else:
        bot.send_message(message.chat.id, cryptpars.bot.for_tg_bot(message.text))


def main():
    bot.polling()


if __name__ == '__main__':
    main()
