import logging
import requests
from google_images_search import GoogleImagesSearch
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
from telegram.ext import (
    Updater,
    CommandHandler,
    CallbackQueryHandler, Filters, MessageHandler
)
import sqlite3

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
                                f"\nЧтобы использовать мой функционал введи /search *аргумент*"
                                f"\nИсточник изображений: ru.pinterest.com")


def say(update, context):
    if not update.edited_message:
        update.message.reply_text(f"Привет, я бот-помощник для начинающих и опытных художников.\nМоей основной "
                                  f"задачей "
                                  f"является подбор референсов для удобства в рисовании"
                                  f"\nЧтобы использовать мой функционал введи /search *аргумент*"
                                  f"\nИсточник изображений: ru.pinterest.com")


def get_help(update, context):
    keyboard = [[
        InlineKeyboardButton("Задать вопрос", callback_data='100'),
        InlineKeyboardButton("О боте", callback_data='99')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Пожалуйста, выберите нужный раздел:', reply_markup=reply_markup)


def start(update, _):
    update.message.reply_text('Чтобы использовать мой функционал введи /search *аргумент*"')


def search(update, context):
    if context.args:
        text_caps = ' '.join(context.args).lower()
        text = 'как нарисовать ' + text_caps
        gis = GoogleImagesSearch('AIzaSyDFsOELU4yrrOTJM2fa4hvgGD1IgaxgCnQ', '8411be3e0f0464f42')
        _search_params = {
            'q': text,
            'num': 9,
            'fileType': 'jpg|png',
            'imgSize': 'large',
        }
        gis.search(search_params=_search_params)
        media_group = []
        for image in gis.results():
            if len(media_group) <= 9:
                media_group.append(InputMediaPhoto(media=image.url, caption="Источник:" + image.url))
            else:
                break
        if media_group:
            updater.bot.send_media_group(chat_id=update.effective_chat.id, media=media_group)
        else:
            update.message.reply_text("Ничего не найдено :(")

    else:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text='Не указан запрос')
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text='Попробуйте: /search argument')


def is_url_image(image_url):
    try:
        image_formats = ("image/png", "image/jpeg", "image/jpg")
        r = requests.head(image_url)
        if r.headers["content-type"] in image_formats:
            return True
    except Exception:
        return False


def add_fav(update, context):
    if context.args:
        user = update.message.from_user
        user_id = str(user.id)
        url = ' '.join(context.args)
        con = sqlite3.connect("data.db")
        con.row_factory = lambda cursor, row: row[0]
        cur = con.cursor()
        favs = cur.execute("""SELECT fav FROM data WHERE id = ?""", (user_id,)).fetchall()
        if url not in favs and is_url_image(url):
            cur.execute("""INSERT INTO data (id, fav) VALUES (?, ?)""", (user_id, url))
            update.message.reply_text("Успешно добавлено в понравившиеся!")
        else:
            update.message.reply_text("Кажется, это не ссылка на картинку...")
        con.commit()
        con.close()
    else:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text='Не указан url')


def get_fav(update, _):
    user = update.message.from_user
    media_group = []
    user_id = str(user.id)
    con = sqlite3.connect("data.db")
    con.row_factory = lambda cursor, row: row[0]
    cur = con.cursor()
    favs = cur.execute("""SELECT fav FROM data WHERE id = ?""", (user_id,)).fetchall()
    for i in favs:
        media_group.append(InputMediaPhoto(media=i, caption="Источник:" + i))
    if media_group:
        updater.bot.send_media_group(chat_id=update.effective_chat.id, media=media_group)
    else:
        update.message.reply_text("Ничего нету :(")


if __name__ == '__main__':
    updater.dispatcher.add_handler(CallbackQueryHandler(button))
    updater.dispatcher.add_handler(CommandHandler('help', get_help))
    updater.dispatcher.add_handler(CommandHandler('add_fav', add_fav))
    updater.dispatcher.add_handler(CommandHandler('fav', get_fav))
    caps_handler = CommandHandler('search', search)
    updater.dispatcher.add_handler(caps_handler)

updater.dispatcher.add_handler(MessageHandler(Filters.text, say))

updater.start_polling()
updater.idle()
