
import tinvest
import telebot

token = ''
client = tinvest.SyncClient(token)
api = tinvest.PortfolioApi(client)

bot = telebot.TeleBot('');

names = ("Название бумаги", "Цена бумаги", "Кол-во в портфели", "Тиккер")
name_paper = ("Газпром нефть", "Татнефть","Тинькофф Вечный портфель USD0","Доллар США")

# Метод для получения текстовых сообщений (поле content_types может быть равен не только тексту, но и аудио, документы и т.п. (content_types=['text', 'document', 'audio']))
@bot.message_handler(content_types=['text'])
# Создание функции обработки сообщений, с параметром message, и отпраки сообщений от бота bot.send_message, функция .lower() для понимания написанного не только по шаблону
def get_text_messages(message):
    if message.text == "Привет":
        bot.send_message(message.from_user.id, "Привет, чем я могу тебе помочь?")
        bot.register_next_step_handler(message, get_tinkoff)  # Переход к след. функции, после ответа на вопрос
    elif message.text == "Дальше":
        bot.send_message(message.from_user.id, "Какую бумагу показать следующей?")
        bot.register_next_step_handler(message, get_tinkoff)
    else:
        bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши 'Привет' или 'Помощь'.")


def get_tinkoff(message):
    if message.text in name_paper:
        def broker_tinkoff():
            response = api.portfolio_get()
            if response.status_code == 200:
                for paper in response.parse_json().payload.positions:
                    if paper.name == message.text:
                        return (paper.name,
                                paper.average_position_price.value,
                                paper.balance,
                                paper.ticker)
        values = broker_tinkoff()
        for i in range(len(values)):
            bot.send_message(message.from_user.id, "{0}: {1}".format(names[i], values[i]))
    else:
        bot.send_message(message.from_user.id, "Я тебя не понимаю, напиши 'Привет'")

# Запрос бота к серверу Телеграм, с интервалом 0 секунд (написал ли кто-то боту)
bot.polling(none_stop=True, interval=0)
