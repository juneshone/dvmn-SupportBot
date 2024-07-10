import logging
import random
import vk_api as vk

from environs import Env
from vk_api.longpoll import VkLongPoll, VkEventType

from dialogflow import detect_intent_text
from logs import TelegramLogsHandler


logger = logging.getLogger('vk_bot')


def perform_intent(event, vk_api, project_id):
    text, fallback = detect_intent_text(
        project_id=project_id,
        session_id=event.user_id,
        text=event.text,
        language_code='ru'
    )
    if fallback:
        return None
    else:
        return vk_api.messages.send(
            user_id=event.user_id,
            message=text,
            random_id=random.randint(1, 1000)
        )


def main():
    env = Env()
    env.read_env()
    tg_token = env.str('TELEGRAM_BOT_TOKEN')
    chat_id = env.int('TELEGRAM_CHAT_ID')
    project_id = env.str('PROJECT_ID')
    logging.basicConfig(
        format='%(asctime)s - %(funcName)s -  %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )
    logger.setLevel(logging.DEBUG)
    logger.addHandler(TelegramLogsHandler(tg_token, chat_id))
    try:
        logger.info('VK Бот запущен')
        vk_session = vk.VkApi(token=env.str('VK_GROUP_TOKEN'))
        vk_api = vk_session.get_api()
        longpoll = VkLongPoll(vk_session)

        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                perform_intent(event, vk_api, project_id)
    except Exception as err:
        logger.error(err, exc_info=True)


if __name__ == '__main__':
    main()
