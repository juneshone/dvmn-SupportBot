import logging

from environs import Env
from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

from dialogflow import detect_intent_text
from logs import TelegramLogsHandler

logger = logging.getLogger('telegram_bot')


def start(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Привет {user.mention_markdown_v2()}\! Чем можем помочь?',
        reply_markup=ForceReply(selective=True),
    )


def perform_intent(update: Update, context: CallbackContext) -> None:
    chat_id = update.message.chat_id
    text, _ = detect_intent_text(
        project_id=env.str('PROJECT_ID'),
        session_id=chat_id,
        text=update.message.text,
        language_code='ru'
    )

    context.bot.send_message(
        chat_id=chat_id,
        text=text,
    )


if __name__ == '__main__':
    env = Env()
    env.read_env()
    tg_token = env.str('TELEGRAM_BOT_TOKEN')
    tg_chat_id = env.int('TELEGRAM_CHAT_ID')
    logging.basicConfig(
        format='%(asctime)s - %(funcName)s -  %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )
    logger.setLevel(logging.DEBUG)
    logger.addHandler(TelegramLogsHandler(tg_token, tg_chat_id))
    logger.info('Telegram Бот запущен')
    try:
        updater = Updater(token=tg_token)
        dispatcher = updater.dispatcher
        dispatcher.add_handler(CommandHandler('start', start))
        dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, perform_intent))

        updater.start_polling()
        updater.idle()
    except Exception as err:
        logging.error(err, exc_info=True)
