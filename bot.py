import asyncio
import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.handler import SkipHandler
from googleapiclient import discovery
from credentials import BOT_TOKEN, API_KEY
from db import *
logging.basicConfig(level=logging.DEBUG)

telegram_bot = Bot(token=BOT_TOKEN)
dispatcher = Dispatcher(bot=telegram_bot)


class ToxicBot():
    def __init__(self):
        self.GlobalHistory = GlobalHistory()
        self.GlobalHistory.create_table([GlobalHistory])

#    def __del__(self):
#        self.GlobalHistory

    def write_history(self, message, result):
        print(f'{message.text} from {message["from"]["username"]} at chat {message["chat"]["id"]} {result}')
        self.GlobalHistory.create(chat_id=message['chat']['id'],
                                  message_text=message.text,
                                  message_author_name=message['from']['username'] or None,
                                  message_author_id=message['from']['id'],
                                  result_toxicity=result['TOXICITY'])

    def get_history(self):
        result = []
        for line in self.GlobalHistory.select():
            result.append(f'{line.message_text} TOXICITY {line.result_toxicity}')
        return result


    def check_toxic(self, text):
        client = discovery.build(
            "commentanalyzer",
            "v1alpha1",
            developerKey=API_KEY,
            discoveryServiceUrl="https://commentanalyzer.googleapis.com/$discovery/rest?version=v1alpha1",
            static_discovery=False,
            )
        analyze_request = {
            'comment': {'text': text},
            'languages': "ru",
            'requestedAttributes': {'TOXICITY': {} }
                                    #'SEVERE_TOXICITY': {}, 'IDENTITY_ATTACK': {}, 'INSULT': {},
                                    #'PROFANITY': {}, 'THREAT': {}}
        }

        response = client.comments().analyze(body=analyze_request).execute()
        return {'Lang': ''.join(response['detectedLanguages'])} | {x: round(100 * response['attributeScores'][x]['spanScores'][0]['score']['value']) for x in response['attributeScores']}

    async def start_bot(self):
        try:
            dispatcher.register_message_handler(telegram_send_message, commands=["start", "restart"])
            dispatcher.register_message_handler(telegram_show_history, commands=["history"])
            await dispatcher.start_polling()
        finally:
            await dispatcher.stop_polling()


t = ToxicBot()
# "'{"ok":true,"result":[{"update_id":103763882,\n
# "message":{"message_id":234,"from":{"id":140231806,"is_bot":false,"first_name":"Andrey","last_name":"Z","username":"andyevil","language_code":"en"},
# "chat":{"id":-708781826,"title":"Toxic Detection test chat","type":"group","all_members_are_administrators":true},"date":1637266347,"text":"\\u0430 \\u0447\\u0442\\u043e \\u044d\\u0442\\u043e \\u0432\\u044b \\u0442\\u0443\\u0442 \\u0432\\u0441\\u0435 \\u0434\\u0435\\u043b\\u0430\\u0435\\u0442\\u0435?"}}]}'"


@dispatcher.message_handler()
async def telegram_send_message(message: types.Message):
    result = t.check_toxic(message.text)
    await message.reply(str(result))
    t.write_history(message, result)
    raise SkipHandler


@dispatcher.message_handler(commands=['history'])
async def telegram_show_history(message: types.Message):
    await message.reply('\n'.join(t.get_history()))



asyncio.run(t.start_bot())
