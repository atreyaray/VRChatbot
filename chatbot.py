import telebot
import requests
import datetime
import time
import json

token = '992203635:AAFpVxyxwj7Vi0H_XBLDcE9L3jkFsL2KEpI'
bot = telebot.TeleBot(token=token)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(
        message, 'Hello, I am Qewtbot! Use /nextstop [train number] to see where the train will stop next')


def next_stop(train_number):
    current_date = str(datetime.date.today())
    current_time = str(datetime.datetime.now())[11:19]
    train_data = requests.get(
        f'http://rata.digitraffic.fi/api/v1/trains/{current_date}/{train_number}')

    if len(train_data.json()) == 0:
        print('Got here A')
        return 'no such train'

    timetables = train_data.json()[0]['timeTableRows']

    for row in timetables:
        if row['scheduledTime'][11:19] > current_time:
            return row['stationShortCode']
    return 'train not running'


@bot.message_handler(commands=['nextstop'])
def send_next_stop(message):
    train_number = message.text.split(' ')[1]
    stop = next_stop(train_number)
    if stop == 'no such train':
        print('B')
        bot.reply_to(message, 'No such train')
    elif stop == 'train not running':
        bot.reply_to(message, 'That train has finished running for the day')
    else:
        bot.reply_to(message, f'The next stop will be {stop}')


while True:
    try:
        bot.polling()
    except:
        time.sleep(5)
