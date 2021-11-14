import asyncio
import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.handler import SkipHandler
from googleapiclient import discovery
from credentials import BOT_TOKEN, API_KEY


def check_toxic(text):
    client = discovery.build(
        "commentanalyzer",
        "v1alpha1",
        developerKey=API_KEY,
        discoveryServiceUrl="https://commentanalyzer.googleapis.com/$discovery/rest?version=v1alpha1",
        static_discovery=False,
    )


    analyze_request = {
        'comment': {'text': text},
        'requestedAttributes': {'TOXICITY': {}, 'SEVERE_TOXICITY': {}, 'IDENTITY_ATTACK': {}, 'INSULT': {},
                                'PROFANITY': {}, 'THREAT': {}}
    }

    response = client.comments().analyze(body=analyze_request).execute()
    return f"Язык: {''.join(response['detectedLanguages']), {x: round(100 * response['attributeScores'][x]['spanScores'][0]['score']['value']) for x in response['attributeScores']} }"
    # return(json.dumps(response, indent=2))


bot = Bot(token=BOT_TOKEN)
disp = Dispatcher(bot=bot)
logging.basicConfig(level=logging.DEBUG)


@disp.message_handler()
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends message in private chat or supergroup
    """
    # print(message.text)
    await message.reply(str(check_toxic(message.text)))
    raise SkipHandler


async def main():
    try:
        disp.register_message_handler(send_welcome, commands={"start", "restart"})
        await disp.start_polling()
    finally:
        await bot.close()

asyncio.run(main())