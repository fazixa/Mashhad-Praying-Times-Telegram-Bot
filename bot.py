from pprint import pprint
import requests
import json
import os
from time import sleep
from flask import Flask, request
import telebot

from tele_news import news
from tele_temp import temp

token = '859406292:AAGwGe5WLdWKDTD2c0-9GdEKYT9Bhb6iZOM'
url = 'https://api.telegram.org/bot{}/'.format(token)
TOKEN = '859406292:AAGwGe5WLdWKDTD2c0-9GdEKYT9Bhb6iZOM'
bot = telebot.TeleBot(TOKEN)
server = Flask(__name__)


def getme():
    res = requests.get(url + "getme")
    d = res.json()
    username = d['result']['username']


def get_updates(offset=None):
    while True:
        try:
            URL = url + 'getUpdates'
            if offset:
                URL += '?offset={}'.format(offset)

            res = requests.get(URL)
            while (res.status_code != 200 or len(res.json()['result']) == 0):
                sleep(1)
                res = requests.get(URL)
            print(res.url)
            return res.json()

        except:
            pass;


def get_last(data):
    results = data['result']
    count = len(results)
    last = count - 1
    last_update = results[last]
    return last_update


def get_last_id_text(updates):
    last_update = get_last(updates)
    chat_id = last_update['message']['chat']['id']
    update_id = last_update['update_id']
    try:
        text = last_update['message']['text']
    except:
        text = ''
    return chat_id, text, update_id


def ask_contact(chat_id):
    print('Ask Contact')
    text = 'Send Contact'
    keyboard = [[{"text": "Contact", "request_contact": True}]]
    reply_markup = {"keyboard": keyboard, "one_time_keyboard": True}
    send_message(chat_id, text, json.dumps(reply_markup))


def ask_location(chat_id):
    print('Ask Location')
    text = 'Send Location'
    keyboard = [[{"text": "Location", "request_location": True}]]
    reply_markup = {"keyboard": keyboard, "one_time_keyboard": True}
    send_message(chat_id, text, json.dumps(reply_markup))


def get_location(update_id):
    print('Get Location')
    updates = get_updates(update_id + 1)
    location = get_last(updates)['message']['location']
    chat_id, text, update_id = get_last_id_text(updates)
    lat = str(location['latitude'])
    lon = str(location['longitude'])
    return lat, lon, update_id


def send_message(chat_id, text, reply_markup=None):
    URL = url + "sendMessage?text={}&chat_id={}&parse_mode=Markdown".format(text, chat_id)
    if reply_markup:
        URL += '&reply_markup={}'.format(reply_markup)
    res = requests.get(URL)
    while res.status_code != 200:
        res = requests.get(URL)
    print(res.status_code)


def reply_markup_maker(data):
    keyboard = []
    for i in range(0, len(data), 2):
        key = []
        key.append(data[i].title())
        try:
            key.append(data[i + 1].title())
        except:
            pass
        keyboard.append(key)

    reply_markup = {"keyboard": keyboard, "one_time_keyboard": True}
    return json.dumps(reply_markup)


def newshey(chat_id):
    message = news()
    send_message(chat_id, message)


def weather(chat_id, update_id):
    ask_location(chat_id)
    lat, lon, update_id = get_location(update_id)
    message = temp(lat, lon)
    send_message(chat_id, message)


def welcome_note(chat_id, commands):

    text = 'Select'
    reply_markup = reply_markup_maker(commands)
    send_message(chat_id, text, reply_markup)


def start(chat_id):
    message = 'سیستم اطلاع رسانی اوقات شرعی شهر مشهد'
    reply_markup = reply_markup_maker(['Start'])
    send_message(chat_id, message, reply_markup)

    chat_id, text, update_id = get_last_id_text(get_updates())
    while (text.lower() != 'start'):
        chat_id, text, update_id = get_last_id_text(get_updates(update_id + 1))
        sleep(0.5)

    return chat_id, text, update_id


def end(chat_id, text, update_id):


    return 'N'



def menu(chat_id, text, update_id):
    commands = ['اوقات شرعی']
    welcome_note(chat_id, commands)

    while (text.lower() == 'start'):
        chat_id, text, update_id = get_last_id_text(get_updates(update_id + 1))
        sleep(0.5)
    print(text)
    while text.lower() not in commands:
        chat_id, text, update_id = get_last_id_text(get_updates(update_id + 1))
        sleep(0.5)


    newshey(chat_id)




def main():
    text = ''
    chat_id, text, update_id = get_last_id_text(get_updates())
    chat_id, text, update_id = start(chat_id)
    print('Started')

    while text.lower() != 'y':
        sleep(1)
        text = 'start'
        menu(chat_id, text, update_id)
        text = 'y'

        chat_id, text, update_id = get_last_id_text(get_updates())
        text = end(chat_id, text, update_id)



@server.route('/' + TOKEN, methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200


@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://shielded-headland-70919.herokuapp.com/' + TOKEN)
    return "!", 200

if __name__ == '__main__':
    main()
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))

