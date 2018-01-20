import requests
import random
from config import token


class BotHandler:

    def __init__(self, token):
        self.token = token
        self.api_url = "https://api.telegram.org/bot{}/".format(token)

    def get_updates(self, offset=None, timeout=30):
        method = 'getUpdates'
        params = {'timeout': timeout, 'offset': offset}
        resp = requests.get(self.api_url + method, params)
        result_json = resp.json()['result']
        return result_json

    def send_message(self, chat_id, text):
        params = {'chat_id': chat_id, 'text': text}
        method = 'sendMessage'
        resp = requests.post(self.api_url + method, params)
        return resp

    def get_last_update(self):
        get_result = self.get_updates()

        if len(get_result) > 0:
            last_update = get_result[-1]
        else:
           last_update = get_result[len(get_result)] # IndexError: list index out of range

        return last_update #UnboundLocalError: local variable 'last_update' referenced before assignment

    def entities_type(self):
        last_update = self.get_last_update()
        entities = last_update['message']['entities']
        if len(entities)>0:
            types = entities[-1]
        else:
            types = entities[len(entities)]
        return types['type']

    def start(self, chat_id, text):
        types = self.entities_type()
        if types == 'bot_command':
            if text == '/start':
                self.send_message(chat_id,"Привет, я Катихо. Пока я бесполезный бот. Но я расту и развиваюсь. Надеюсь, скоро я стану для тебя полезен.")

    def welcome_user(self, chat_id, name, text):
        greetings = ('привет катихо', 'hello', 'hi', 'привет', 'привет, катихо')
        greetings_office = ('доброе утро', 'добрый день', 'добрый вечер')
        print(text.lower())
        i = random.randint(1, 3)
        if text.lower() in greetings:
            if i == 1:
                self.send_message(chat_id, 'Привет, {}'.format(name))
            if i == 2:
                self.send_message(chat_id, 'Катихо здесь)')
            if i == 3:
                self.send_message(chat_id, 'Дратути')

        elif text.lower() in greetings_office:
            greet_bot.send_message(chat_id, 'Здравствуй, {}'.format(name))


greet_bot = BotHandler(token) # НЕ ПОТЕРЯЙ!!

def main():
    new_offset = None
    while True:

        update = greet_bot.get_updates(new_offset)
        print(update)
        try:
            last_update = greet_bot.get_last_update()
            print(greet_bot.get_last_update())
            last_update_id = last_update['update_id']
            last_chat_text = last_update['message']['text']
            last_chat_id = last_update['message']['chat']['id']
            last_chat_name = last_update['message']['chat']['first_name']

            # приветствие
            greet_bot.welcome_user(last_chat_id, last_chat_name, last_chat_text)

            # start
            try:
                greet_bot.start(last_chat_id,last_chat_text)
            except:
                print("команды нет")

            #перейти к новому обновлению
            new_offset = last_update_id + 1
            print(new_offset)

        except:
            print("Нет новых сообщений")
            new_offset = last_update_id + 1
            print(new_offset)




if __name__ == '__main__':
    try:
        main()
    except:
        exit()