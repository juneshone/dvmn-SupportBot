import logging
import random
import time
import vk_api as vk

from environs import Env
from vk_api.longpoll import VkLongPoll, VkEventType

from dialogflow import detect_intent_text


logger = logging.getLogger('vk_bot')


def perform_intent(event, vk_api):
    start = time.time()
    text, fallback = detect_intent_text(
        project_id=env.str('PROJECT_ID'),
        session_id=event.user_id,
        text=event.text,
        language_code='ru'
    )
    print("Время ожидания: " + str(time.time() - start)[:5])
    if fallback:
        return None
    else:
        return vk_api.messages.send(
            user_id=event.user_id,
            message=text,
            random_id=random.randint(1, 1000)
        )


def main():
    logging.basicConfig(
        format='%(asctime)s - %(funcName)s -  %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )
    logger.info('Бот запущен')
    vk_session = vk.VkApi(token=env.str('VK_GROUP_TOKEN'))
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            perform_intent(event, vk_api)


if __name__ == '__main__':
    env = Env()
    env.read_env()
    main()
