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
    bot.reply_to(msg,"Hi I'm a Vk-relay bot.\n" \
            "I'm really in the development state now"
    )

# Handle all text messages
@bot.message_handler(func=lambda m: True)
def message_handle(msg):

    # check for reply and then send message
    if msg.reply_to_message:

        # Prepare some credential to anser in VK
        peer_id=msg.reply_to_message.text.split()[1]
        message_id=msg.reply_to_message.text.split()[2]

        session = vk.Session(access_token=VK_TOKEN)
        api     = vk.API(session, v=VK_API_VERSION, lang='ru', timeout=1)
        api.messages.send(
                random_id=random.randrange(1,2**16), peer_id=peer_id, message=msg.text,  reply_to=message_id
        )

        bot.reply_to(msg, "Message sent succesfully!")
        print("[D] message sent to", peer_id)

if __name__ == '__main__':
    print('Vk relaybot started')
    bot.polling(none_stop=True)
