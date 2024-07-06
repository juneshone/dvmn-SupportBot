import random
import vk_api as vk

from environs import Env
from vk_api.longpoll import VkLongPoll, VkEventType

from dialogflow import detect_intent_text


def intent(event, vk_api):
    text = detect_intent_text(
        project_id=env.str('PROJECT_ID'),
        session_id=event.user_id,
        text=event.text,
        language_code='ru'
    )
    vk_api.messages.send(
        user_id=event.user_id,
        message=text,
        random_id=random.randint(1,1000)
    )


def main():
    vk_session = vk.VkApi(token=env.str('VK_GROUP_TOKEN'))
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            print('Новое сообщение:')
            if event.to_me:
                intent(event, vk_api)
                print('Для меня от: ', event.user_id)
            else:
                print('От меня для: ', event.user_id)
            print('Текст:', event.text)


if __name__ == '__main__':
    env = Env()
    env.read_env()
    main()
