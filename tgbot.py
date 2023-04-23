import logging
from google_images_search import GoogleImagesSearch
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
from telegram.ext import (
    Updater,
    CommandHandler,
    CallbackQueryHandler,
    ConversationHandler, Filters, MessageHandler
)


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

updater = Updater("5967081389:AAFT5LDp9ppIUfGYgBcv7SGzxx3spo4BwC0")


def button(update, _):
    query = update.callback_query
    variant = query.data
    query.answer()
    if variant == '100':
        query.edit_message_text(text=f"Об ошибках и пожеланиях Вы можете написать @byoumeiwaaidatta")
    elif variant == '99':
        query.edit_message_text(f"Привет, я бот-помощник для начинающих и опытных художников.\nМоей основной "
                                  f"задачей "
                                  f"является подбор референсов для удобства в рисовании"
                                  f"\nЧтобы использовать мой функционал введи /search *аргумент*")


def say(update, context):
    if not update.edited_message:
        update.message.reply_text(f"Привет, я бот-помощник для начинающих и опытных художников.\nМоей основной "
                                  f"задачей "
                                  f"является подбор референсов для удобства в рисовании"
                                  f"\nЧтобы использовать мой функционал введи /search *аргумент*")


def get_help(update, context):
    keyboard = [[
        InlineKeyboardButton("Задать вопрос", callback_data='100'),
        InlineKeyboardButton("О боте", callback_data='99')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Пожалуйста, выберите нужный раздел:', reply_markup=reply_markup)


def start(update, _):
    user = update.message.from_user
    logger.info("Пользователь %s начал разговор", user.first_name)
    update.message.reply_text('Чтобы использовать мой функционал введи /search *аргумент*"')


def search(update, context):
    if context.args:
        text_caps = ' '.join(context.args).lower()
        text = 'как нарисовать ' + text_caps
        gis = GoogleImagesSearch('AIzaSyDFsOELU4yrrOTJM2fa4hvgGD1IgaxgCnQ', '8411be3e0f0464f42')
        _search_params = {
            'q': text,
            'num': 9,
            'fileType': 'jpg',
            'imgSize': 'huge|large|medium|',
        }
        gis.search(search_params=_search_params)
        media_group = []
        for image in gis.results():
            media_group.append(InputMediaPhoto(media=image.url, caption="Источник:" + image.url))
        sndmediagroup = updater.bot.send_media_group(chat_id=update.effective_chat.id, media=media_group)
        for i in range(len(sndmediagroup)):
            sndmediagroup[i] = sndmediagroup[i].message_id
    else:

        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text='Не указан запрос')
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text='Попробуйте: /search argument')


if __name__ == '__main__':
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            F: [
                CallbackQueryHandler(end, pattern='^' + 'stop' + '$')
            ]
        },
        fallbacks=[CommandHandler('start', start), CommandHandler('help', get_help)],
    )
    updater.dispatcher.add_handler(conv_handler)
    updater.dispatcher.add_handler(CallbackQueryHandler(button))

    updater.dispatcher.add_handler(CommandHandler('help', get_help))
    caps_handler = CommandHandler('search', search)
    updater.dispatcher.add_handler(caps_handler)

updater.dispatcher.add_handler(MessageHandler(Filters.text, say))

updater.start_polling()
updater.idle()
