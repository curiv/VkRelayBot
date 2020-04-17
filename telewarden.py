#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import telebot, vk
import random
from config import VK_TOKEN, VK_API_VERSION, TG_TOKEN, TG_MY_CHAT
from telebot import apihelper

bot = telebot.TeleBot(TG_TOKEN)

@bot.message_handler(commands=['start'])
def handle_start_help(msg):
    start_text = 'Hello :)'
    bot.send_message(msg.chat.id, start_text)

@bot.message_handler(commands=['help'])
def handle_start_help(msg):
    pass

@bot.message_handler(commands=['send'])
def send_message(msg):
   session = vk.Session(access_token=VK_TOKEN)
   api     = vk.API(session, v=VK_API_VERSION, lang='ru', timeout=1)
   api.messages.send(
            random_id=random.randrange(1,2**16), peer_id=62136092, message=":)"
        )

if __name__ == '__main__':
    print('Vk relaybot started')
    bot.polling(none_stop=True)
