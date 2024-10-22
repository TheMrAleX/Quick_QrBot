import telebot
from tools import detectar_url
from qr_gen import crear_qr
import os

from var import TOKEN

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    texto = '👋 ¡Bienvenido/a al Generador de QR!\nSimplemente envíame cualquier enlace y te devolveré una imagen con el código QR. ¡Así de sencillo! 🎯✨'
    bot.send_message(message.chat.id, texto)

@bot.message_handler(func=lambda message: True)
def message_qr(message):
    url = message.text
    
    if detectar_url(url) == False:
        bot.send_message(message.chat.id, 'Lo que enviaste no parece ser un enlace. 📎 Intenta copiarlo y pegarlo desde el navegador o asegúrate de agregar "www" o "http://" al principio. 🌐')
    else:
        bot.send_message(message.chat.id, 'Procesando...')
        qr = crear_qr(url)
        print(qr)
        with open(qr, 'rb') as file:
            bot.send_photo(message.chat.id, file)
        os.remove(qr)
        

if __name__ == '__main__':
    bot.infinity_polling()