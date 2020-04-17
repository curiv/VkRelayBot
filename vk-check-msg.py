import requests, json, sqlite3, time
import vk, telebot

from config import VK_TOKEN, VK_API_VERSION, TG_TOKEN, TG_MY_CHAT

# Check for new messages
def vk_check_msg(api, cursor):
    # Get a messages object from API
    messages      = api.messages.getConversations(filter="unread")
    message_count = messages['count']

    print(f"{message_count} new messages")

    # Check for message count
    if message_count:

        for order in range(message_count):
            message_body = messages['items'][order]['last_message']
            #print(message_body)

            # Get some information about user
            sender_id    = message_body['from_id']
            sender_text  = message_body['text']
            message_id   = message_body['id']

            try:
                user_info    = api.users.get(user_ids=sender_id)[0]
                first_name   = user_info['first_name']
                last_name    = user_info['last_name']
            except vk.exceptions.VkAPIError:
                first_name   = "Comm"
                last_name    = "Comm"

            # Insert values to the database
            cursor.execute("INSERT INTO vk VALUES (?, ?, ?, ?, ?, ?, ?)",
                                (None, sender_id , first_name, last_name, sender_text, message_id, 0)
                    )

            # Forming a message template
            msg = f"[VK] {sender_id} {message_id}\n"\
                  f"{first_name} {last_name}\n"\
                  f"{sender_text}"

            print(msg)
            bot.send_message(TG_MY_CHAT, msg)

if __name__ == "__main__":
    # Define some variables

    # Initialize vk and tg session
    session = vk.Session(access_token=VK_TOKEN)
    bot     = telebot.TeleBot(TG_TOKEN)
    api     = vk.API(session, v=VK_API_VERSION, lang='ru', timeout=1)

    # Initialize db
    conn    = sqlite3.connect('vk.sqlite3')
    cursor  = conn.cursor()

    vk_check_msg(api, cursor)

    conn.commit()
