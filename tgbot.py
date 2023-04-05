import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
from telegram.ext import (
    Updater,
    CommandHandler,
    CallbackQueryHandler,
    ConversationHandler, filters, MessageHandler
)
import inspect

b = []
a = 1
# Ведение журнала логов
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

F, S = range(2)
updater = Updater("5967081389:AAFT5LDp9ppIUfGYgBcv7SGzxx3spo4BwC0")


def button(update, _):
    query = update.callback_query
    variant = query.data
    query.answer()
    if variant == '100':
        query.edit_message_text(text=f"Об ошибках и пожеланиях Вы можете написать в ЛС @gvetrof")
    elif variant == '99':
        query.edit_message_text(text=f"Часто художники не знают где найти референс для нужной ситуации.\nБот будет "
                                     f"пополняться. Всё будет в одном месте и это очень удобно, ведь Вы сможете "
                                     f"одновременно и найти идею и узнать о правильном рисовании определенных "
                                     f"моментов.")


def say(update, context):
    if not update.edited_message:
        update.message.reply_text(f"Привет, я бот-помощник для начинающих и опытных художников.\nМоей основной "
                                  f"задачей "
                                  f"является подбор референсов для удобства в рисовании"
                                  f"\nЧтобы использовать мой функционал введи /help или /start")


def get_help(update, context):
    keyboard = [[
        InlineKeyboardButton("Задать вопрос", callback_data='100'),
        InlineKeyboardButton("О боте", callback_data='99')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Пожалуйста, выберите нужный раздел:', reply_markup=reply_markup)


def start(update, _):
    global a
    global b
    if b:
        for i in b:
            updater.bot.delete_message(update.effective_chat.id, i)
    b = []
    a = 1
    user = update.message.from_user
    logger.info("Пользователь %s начал разговор", user.first_name)
    keyboard = [
        [
            InlineKeyboardButton("Природа", callback_data='nature')
        ], [InlineKeyboardButton("Цивилизация", callback_data='modern')],
        [InlineKeyboardButton("Человек и прочее", callback_data='human'),
         InlineKeyboardButton("Завершить работу", callback_data='stop')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Вы в главном меню!\nПожалуйста, выберите нужный раздел:', reply_markup=reply_markup)
    return F


def start_over(update, _):
    global a
    global b
    a = 1
    if b:
        for i in b:
            updater.bot.delete_message(update.effective_chat.id, i)
    b = []
    query = update.callback_query
    query.answer()
    keyboard = [
        [
            InlineKeyboardButton("Природа", callback_data='nature')
        ], [InlineKeyboardButton("Цивилизация", callback_data='modern')],
        [InlineKeyboardButton("Человек и прочее", callback_data='human'),
         InlineKeyboardButton("Завершить работу", callback_data='stop')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text='Вы в главном меню!\nПожалуйста, выберите нужный раздел:', reply_markup=reply_markup)
    return F


def modern(update, _):
    """Показ нового выбора кнопок"""
    query = update.callback_query
    query.answer()
    keyboard = [
        [
            InlineKeyboardButton("Техника", callback_data='tech'),
            InlineKeyboardButton("Фоны", callback_data='city'),
        ], [InlineKeyboardButton("Главное меню", callback_data='start_over')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text="Пожалуйста, выберите нужную подкатегорию:", reply_markup=reply_markup
    )
    return F


def city(update, _):
    global a
    global b
    if str(update.callback_query.data) == 'citynext':
        if a < 3:
            a += 1
        else:
            a = 1
    elif str(update.callback_query.data) == 'cityprev':
        if a > 1:
            a -= 1
        else:
            a = 3
    if b:
        for i in b:
            updater.bot.delete_message(update.effective_chat.id, i)
    b = []
    query = update.callback_query
    query.answer()
    keyboard = [
        [
            InlineKeyboardButton("Назад", callback_data='cityprev'),
            InlineKeyboardButton("Вперед", callback_data='citynext'),
        ],
        [InlineKeyboardButton("В главное меню", callback_data='start_over')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text=f"Надеемся вам понравится!\nСтраница {a} из 3.", reply_markup=reply_markup
    )
    ndef = inspect.getframeinfo(
        inspect.currentframe()).function  # Название функции и папки в которой хранится нужный файл (str)
    with open(f'{ndef}/{a}/1.png', 'rb') as f1, open(f'{ndef}/{a}/2.png', 'rb') as f2, \
            open(f'{ndef}/{a}/3.png', 'rb') as f3:
        b = updater.bot.send_media_group(update.effective_chat.id,
                                         [InputMediaPhoto(f1), InputMediaPhoto(f2), InputMediaPhoto(f3)])
    for i in range(len(b)):
        b[i] = b[i].message_id
    return F


def priroda(update, _):
    """Показ нового выбора кнопок"""
    query = update.callback_query
    query.answer()
    keyboard = [
        [
            InlineKeyboardButton("Животные", callback_data='pzhiv'),
            InlineKeyboardButton("Фоны", callback_data='pfon'),
        ], [InlineKeyboardButton("Главное меню", callback_data='start_over')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text="Пожалуйста, выберите нужную подкатегорию:", reply_markup=reply_markup
    )
    return F


def pzhiv(update, _):
    global a
    global b
    if str(update.callback_query.data) == 'pzhivnext':
        if a < 3:
            a += 1
        else:
            a = 1
    elif str(update.callback_query.data) == 'pzhivprev':
        if a > 1:
            a -= 1
        else:
            a = 3
    if b:
        for i in b:
            updater.bot.delete_message(update.effective_chat.id, i)
    b = []
    query = update.callback_query
    query.answer()
    keyboard = [
        [
            InlineKeyboardButton("Назад", callback_data='pzhivprev'),
            InlineKeyboardButton("Вперед", callback_data='pzhivnext'),
        ],
        [InlineKeyboardButton("В главное меню", callback_data='start_over')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text=f"Надеемся вам понравится!\nСтраница {a} из 3.", reply_markup=reply_markup
    )
    ndef = inspect.getframeinfo(
        inspect.currentframe()).function  # Название функции и папки в которой хранится нужный файл (str)
    with open(f'{ndef}/{a}/1.png', 'rb') as f1, open(f'{ndef}/{a}/2.png', 'rb') as f2, \
            open(f'{ndef}/{a}/3.png', 'rb') as f3:
        b = updater.bot.send_media_group(update.effective_chat.id,
                                         [InputMediaPhoto(f1), InputMediaPhoto(f2), InputMediaPhoto(f3)])
    for i in range(len(b)):
        b[i] = b[i].message_id
    return F


def pfon(update, _):
    global a
    global b
    if str(update.callback_query.data) == 'pfonnext':
        if a < 3:
            a += 1
        else:
            a = 1
    elif str(update.callback_query.data) == 'pfonprev':
        if a > 1:
            a -= 1
        else:
            a = 3
    if b:
        for i in b:
            updater.bot.delete_message(update.effective_chat.id, i)
    b = []
    query = update.callback_query
    query.answer()
    keyboard = [
        [
            InlineKeyboardButton("Назад", callback_data='pfonprev'),
            InlineKeyboardButton("Вперед", callback_data='pfonnext'),
        ],
        [InlineKeyboardButton("В главное меню", callback_data='start_over')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text=f"Надеемся вам понравится!\nСтраница {a} из 3.", reply_markup=reply_markup
    )
    ndef = inspect.getframeinfo(
        inspect.currentframe()).function  # Название функции и папки в которой хранится нужный файл (str)
    with open(f'{ndef}/{a}/1.png', 'rb') as f1, open(f'{ndef}/{a}/2.png', 'rb') as f2, \
            open(f'{ndef}/{a}/3.png', 'rb') as f3:
        b = updater.bot.send_media_group(update.effective_chat.id,
                                         [InputMediaPhoto(f1), InputMediaPhoto(f2), InputMediaPhoto(f3)])
    for i in range(len(b)):
        b[i] = b[i].message_id
    return F


def tech(update, _):
    global a
    global b
    if str(update.callback_query.data) == 'tnext':
        if a < 3:
            a += 1
        else:
            a = 1
    elif str(update.callback_query.data) == 'tprev':
        if a > 1:
            a -= 1
        else:
            a = 3
    if b:
        for i in b:
            updater.bot.delete_message(update.effective_chat.id, i)
    b = []
    query = update.callback_query
    query.answer()
    keyboard = [
        [
            InlineKeyboardButton("Назад", callback_data='tprev'),
            InlineKeyboardButton("Вперед", callback_data='tnext'),
        ],
        [InlineKeyboardButton("В главное меню", callback_data='start_over')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text=f"Надеемся вам понравится!\nСтраница {a} из 3.", reply_markup=reply_markup
    )
    ndef = inspect.getframeinfo(
        inspect.currentframe()).function  # Название функции и папки в которой хранится нужный файл (str)
    with open(f'{ndef}/{a}/1.png', 'rb') as f1, open(f'{ndef}/{a}/2.png', 'rb') as f2, \
            open(f'{ndef}/{a}/3.png', 'rb') as f3:
        b = updater.bot.send_media_group(update.effective_chat.id,
                                         [InputMediaPhoto(f1), InputMediaPhoto(f2), InputMediaPhoto(f3)])
    for i in range(len(b)):
        b[i] = b[i].message_id
    return F


def hairs(update, _):
    global a
    global b
    if str(update.callback_query.data) == 'hnext':
        if a < 3:
            a += 1
        else:
            a = 1
    elif str(update.callback_query.data) == 'hprev':
        if a > 1:
            a -= 1
        else:
            a = 3
    if b:
        for i in b:
            updater.bot.delete_message(update.effective_chat.id, i)
    b = []
    query = update.callback_query
    query.answer()
    keyboard = [
        [
            InlineKeyboardButton("Назад", callback_data='hprev'),
            InlineKeyboardButton("Вперед", callback_data='hnext'),
        ],
        [InlineKeyboardButton("В главное меню", callback_data='start_over')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text=f"Надеемся вам понравится!\nСтраница {a} из 3.", reply_markup=reply_markup
    )
    ndef = inspect.getframeinfo(
        inspect.currentframe()).function  # Название функции и папки в которой хранится нужный файл (str)
    with open(f'{ndef}/{a}/1.png', 'rb') as f1, open(f'{ndef}/{a}/2.png', 'rb') as f2, \
            open(f'{ndef}/{a}/3.png', 'rb') as f3:
        b = updater.bot.send_media_group(update.effective_chat.id,
                                         [InputMediaPhoto(f1), InputMediaPhoto(f2), InputMediaPhoto(f3)])
    for i in range(len(b)):
        b[i] = b[i].message_id
    return F


def emot(update, _):
    global a
    global b
    if str(update.callback_query.data) == 'emotnext':
        if a < 3:
            a += 1
        else:
            a = 1
    elif str(update.callback_query.data) == 'emotprev':
        if a > 1:
            a -= 1
        else:
            a = 3
    if b:
        for i in b:
            updater.bot.delete_message(update.effective_chat.id, i)
    b = []
    query = update.callback_query
    query.answer()
    keyboard = [
        [
            InlineKeyboardButton("Назад", callback_data='emotprev'),
            InlineKeyboardButton("Вперед", callback_data='emotnext'),
        ],
        [InlineKeyboardButton("В главное меню", callback_data='start_over')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text=f"Надеемся вам понравится!\nСтраница {a} из 3.", reply_markup=reply_markup
    )
    ndef = inspect.getframeinfo(
        inspect.currentframe()).function  # Название функции и папки в которой хранится нужный файл (str)
    with open(f'{ndef}/{a}/1.png', 'rb') as f1, open(f'{ndef}/{a}/2.png', 'rb') as f2, \
            open(f'{ndef}/{a}/3.png', 'rb') as f3:
        b = updater.bot.send_media_group(update.effective_chat.id,
                                         [InputMediaPhoto(f1), InputMediaPhoto(f2), InputMediaPhoto(f3)])
    for i in range(len(b)):
        b[i] = b[i].message_id
    return F


def cloths(update, _):
    global a
    global b
    if str(update.callback_query.data) == 'cnext':
        if a < 3:
            a += 1
        else:
            a = 1
    elif str(update.callback_query.data) == 'cprev':
        if a > 1:
            a -= 1
        else:
            a = 3
    if b:
        for i in b:
            updater.bot.delete_message(update.effective_chat.id, i)
    b = []
    query = update.callback_query
    query.answer()
    keyboard = [
        [
            InlineKeyboardButton("Назад", callback_data='cprev'),
            InlineKeyboardButton("Вперед", callback_data='cnext'),
        ],
        [InlineKeyboardButton("В главное меню", callback_data='start_over')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text=f"Надеемся вам понравится!\nСтраница {a} из 3.", reply_markup=reply_markup
    )
    ndef = inspect.getframeinfo(
        inspect.currentframe()).function  # Название функции и папки в которой хранится нужный файл (str)
    with open(f'{ndef}/{a}/1.png', 'rb') as f1, open(f'{ndef}/{a}/2.png', 'rb') as f2, \
            open(f'{ndef}/{a}/3.png', 'rb') as f3:
        b = updater.bot.send_media_group(update.effective_chat.id,
                                         [InputMediaPhoto(f1), InputMediaPhoto(f2), InputMediaPhoto(f3)])
    for i in range(len(b)):
        b[i] = b[i].message_id
    return F


def poses(update, _):
    global a
    global b
    if str(update.callback_query.data) == 'pnext':
        if a < 3:
            a += 1
        else:
            a = 1
    elif str(update.callback_query.data) == 'pprev':
        if a > 1:
            a -= 1
        else:
            a = 3
    if b:
        for i in b:
            updater.bot.delete_message(update.effective_chat.id, i)
    b = []
    query = update.callback_query
    query.answer()
    keyboard = [
        [
            InlineKeyboardButton("Назад", callback_data='pprev'),
            InlineKeyboardButton("Вперед", callback_data='pnext'),
        ],
        [InlineKeyboardButton("В главное меню", callback_data='start_over')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text=f"Надеемся вам понравится!\nСтраница {a} из 3.", reply_markup=reply_markup
    )
    ndef = inspect.getframeinfo(
        inspect.currentframe()).function  # Название функции и папки в которой хранится нужный файл (str)
    with open(f'{ndef}/{a}/1.png', 'rb') as f1, open(f'{ndef}/{a}/2.png', 'rb') as f2, \
            open(f'{ndef}/{a}/3.png', 'rb') as f3:
        b = updater.bot.send_media_group(update.effective_chat.id,
                                         [InputMediaPhoto(f1), InputMediaPhoto(f2), InputMediaPhoto(f3)])
    for i in range(len(b)):
        b[i] = b[i].message_id
    return F


def bparts(update, _):
    global a
    global b
    if str(update.callback_query.data) == 'bnext':
        if a < 3:
            a += 1
        else:
            a = 1
    elif str(update.callback_query.data) == 'bprev':
        if a > 1:
            a -= 1
        else:
            a = 3
    if b:
        for i in b:
            updater.bot.delete_message(update.effective_chat.id, i)
    b = []
    query = update.callback_query
    query.answer()
    keyboard = [
        [
            InlineKeyboardButton("Назад", callback_data='bprev'),
            InlineKeyboardButton("Вперед", callback_data='bnext'),
        ],
        [InlineKeyboardButton("В главное меню", callback_data='start_over')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text=f"Надеемся вам понравится!\nСтраница {a} из 3.", reply_markup=reply_markup
    )
    ndef = inspect.getframeinfo(
        inspect.currentframe()).function  # Название функции и папки в которой хранится нужный файл (str)
    with open(f'{ndef}/{a}/1.png', 'rb') as f1, open(f'{ndef}/{a}/2.png', 'rb') as f2, \
            open(f'{ndef}/{a}/3.png', 'rb') as f3:
        b = updater.bot.send_media_group(update.effective_chat.id,
                                         [InputMediaPhoto(f1), InputMediaPhoto(f2), InputMediaPhoto(f3)])
    for i in range(len(b)):
        b[i] = b[i].message_id
    return F


def sh(update, _):
    global a
    global b
    if str(update.callback_query.data) == 'snext':
        if a < 3:
            a += 1
        else:
            a = 1
    elif str(update.callback_query.data) == 'sprev':
        if a > 1:
            a -= 1
        else:
            a = 3
    if b:
        for i in b:
            updater.bot.delete_message(update.effective_chat.id, i)
    b = []
    query = update.callback_query
    query.answer()
    keyboard = [
        [
            InlineKeyboardButton("Назад", callback_data='sprev'),
            InlineKeyboardButton("Вперед", callback_data='snext'),
        ],
        [InlineKeyboardButton("В главное меню", callback_data='start_over')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text=f"Надеемся вам понравится!\nСтраница {a} из 3.", reply_markup=reply_markup
    )
    ndef = inspect.getframeinfo(
        inspect.currentframe()).function  # Название функции и папки в которой хранится нужный файл (str)
    with open(f'{ndef}/{a}/1.png', 'rb') as f1, open(f'{ndef}/{a}/2.png', 'rb') as f2, \
            open(f'{ndef}/{a}/3.png', 'rb') as f3:
        b = updater.bot.send_media_group(update.effective_chat.id,
                                         [InputMediaPhoto(f1), InputMediaPhoto(f2), InputMediaPhoto(f3)])
    for i in range(len(b)):
        b[i] = b[i].message_id
    return F


def human(update, _):
    query = update.callback_query
    query.answer()
    keyboard = [
        [
            InlineKeyboardButton("Эмоции", callback_data='emot'),
            InlineKeyboardButton("Волосы", callback_data='hairs'),
            InlineKeyboardButton("Одежда", callback_data='cloths'),
        ],
        [InlineKeyboardButton("Позы", callback_data='poses'),
         InlineKeyboardButton("Части тела", callback_data='bparts')],
        [InlineKeyboardButton("Шаблоны/Идеи", callback_data='sh')],
        [InlineKeyboardButton("В меню", callback_data='start_over')
         ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text="Пожалуйста, выберите нужную подкатегорию:", reply_markup=reply_markup
    )
    return F


def end(update, _):
    global b
    global a
    a = 1
    query = update.callback_query
    query.answer()
    if b:
        for i in b:
            updater.bot.delete_message(update.effective_chat.id, i)
    b = []
    query.edit_message_text(text="Удачи! Надеемся, что помогли Вам!")
    return ConversationHandler.END


if __name__ == '__main__':
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            F: [
                CallbackQueryHandler(priroda, pattern='^' + 'nature' + '$'),
                CallbackQueryHandler(modern, pattern='^' + 'modern' + '$'),
                CallbackQueryHandler(tech, pattern='^' + 'tech' + '$'),
                CallbackQueryHandler(human, pattern='^' + 'human' + '$'),
                CallbackQueryHandler(start_over, pattern='^' + 'start_over' + '$'),
                CallbackQueryHandler(pfon, pattern='^' + 'pfon' + '$'),
                CallbackQueryHandler(pzhiv, pattern='^' + 'pzhiv' + '$'),
                CallbackQueryHandler(pzhiv, pattern='^' + 'pzhivnext' + '$'),
                CallbackQueryHandler(emot, pattern='^' + 'emot' + '$'),
                CallbackQueryHandler(bparts, pattern='^' + 'bparts' + '$'),
                CallbackQueryHandler(bparts, pattern='^' + 'bnext' + '$'),
                CallbackQueryHandler(bparts, pattern='^' + 'bprev' + '$'),
                CallbackQueryHandler(poses, pattern='^' + 'poses' + '$'),
                CallbackQueryHandler(poses, pattern='^' + 'pnext' + '$'),
                CallbackQueryHandler(poses, pattern='^' + 'pprev' + '$'),
                CallbackQueryHandler(city, pattern='^' + 'city' + '$'),
                CallbackQueryHandler(cloths, pattern='^' + 'cloths' + '$'),
                CallbackQueryHandler(cloths, pattern='^' + 'cnext' + '$'),
                CallbackQueryHandler(cloths, pattern='^' + 'cprev' + '$'),
                CallbackQueryHandler(sh, pattern='^' + 'sprev' + '$'),
                CallbackQueryHandler(sh, pattern='^' + 'snext' + '$'),
                CallbackQueryHandler(sh, pattern='^' + 'sh' + '$'),
                CallbackQueryHandler(hairs, pattern='^' + 'hairs' + '$'),
                CallbackQueryHandler(hairs, pattern='^' + 'hnext' + '$'),
                CallbackQueryHandler(hairs, pattern='^' + 'hprev' + '$'),
                CallbackQueryHandler(city, pattern='^' + 'citynext' + '$'),
                CallbackQueryHandler(city, pattern='^' + 'cityprev' + '$'),
                CallbackQueryHandler(emot, pattern='^' + 'emotnext' + '$'),
                CallbackQueryHandler(emot, pattern='^' + 'emotprev' + '$'),
                CallbackQueryHandler(pzhiv, pattern='^' + 'pzhivprev' + '$'),
                CallbackQueryHandler(pfon, pattern='^' + 'pfonnext' + '$'),
                CallbackQueryHandler(pfon, pattern='^' + 'pfonprev' + '$'),
                CallbackQueryHandler(tech, pattern='^' + 'tnext' + '$'),
                CallbackQueryHandler(tech, pattern='^' + 'tprev' + '$'),
                CallbackQueryHandler(end, pattern='^' + 'stop' + '$')
            ],
            S: [

            ],
        },
        fallbacks=[CommandHandler('start', start), CommandHandler('help', get_help)],
    )
    updater.dispatcher.add_handler(conv_handler)
    updater.dispatcher.add_handler(CallbackQueryHandler(button))

    updater.dispatcher.add_handler(CommandHandler('help', get_help))

updater.dispatcher.add_handler(MessageHandler(filters.text, say))

updater.start_polling()
updater.idle()
