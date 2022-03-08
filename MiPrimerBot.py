import logging
#from telegram.constants import CHATACTION_UPLOAD_DOCUMENT
from telegram.ext import Updater, CallbackContext, CommandHandler, MessageHandler, Filters
from telegram import Update
#Añadimos clases para el modo inline.
from telegram import InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import InlineQueryHandler

from constantes import CYBERMITOTOKEN
#from telegram.ext import CallbackContext
#from telegram.ext import CommandHandler

#TOKEN = CYBERMITOTOKEN#Poner el Token en un archivo independiente que no
#se suba a github, metiendo el archivo en el .gitignore.

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

updater = Updater(token=CYBERMITOTOKEN, use_context=True)
dispatcher = updater.dispatcher

def start(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hola, soy un bot, por favor habla conmigo")

def adios(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="¿Ya te vas? ¡Quedate un ratito más!")

def echo(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)

def caps(update: Update, context: CallbackContext):
    text_caps =' '. join(context.args).upper()
    if text_caps == 'HOLA' or  text_caps == '¿QUÉ TAL?':
        context.bot.send_message(chat_id=update.effective_chat.id, text="Hola, soy bot")
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)

#definimos una función para tratar el modo inline. Ver más información en la documentación del módulo
#Aquí hay que definir que es lo que queremos mostrar cuando nos lo soliciten desde
#cualquier chat. Ver documentación módulo y API Telegram. 
def inline_caps(update: Update, context: CallbackContext):
    query = update.inline_query.query
    if not query:
        return
    results = []
    results.append(
        InlineQueryResultArticle(
            id=query.upper(),
            title="Caps",
            input_message_content=InputTextMessageContent(query.upper())

        )
    )
    context.bot.answer_inline_query(update.inline_query.id, results )

#Con esta función creamos un handler al final del programa para que responda cuando el comando no exista. 
def unknown(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Lo siento, ese comando no está activo")

def parada(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Voy a proceder a desconectarme, hasta pronto")
    updater.stop()

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

adios_handler = CommandHandler('adios', adios)
dispatcher.add_handler(adios_handler)

echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
dispatcher.add_handler(echo_handler)

caps_handler = CommandHandler('caps', caps)
dispatcher.add_handler(caps_handler)

inline_caps_handler = InlineQueryHandler(inline_caps)
dispatcher.add_handler(inline_caps_handler)

parada_handler = CommandHandler('stop', parada)
dispatcher.add_handler(parada_handler)

unknown_handler = MessageHandler(Filters.command, unknown)
dispatcher.add_handler(unknown_handler)

updater.start_polling()
updater.idle()

