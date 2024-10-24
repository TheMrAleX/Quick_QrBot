import telebot
from tools import detectar_url
from qr_man import crear_qr, leer_qr
import os

from dotenv import load_dotenv

from var import MENSAJE_ERROR, photos_dir

load_dotenv()
TOKEN = os.getenv('TOKEN')

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
        qr = crear_qr(url)
        print(qr)
        with open(qr, 'rb') as file:
            bot.send_photo(message.chat.id, file)
        os.remove(qr)

# funcion que detecta si se recibe una imagen si es asi se ejecuta
@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    # le avisa al usuario que puede tardadr en procesar unos segundos
    bot.send_message(message.chat.id, 'Dame un momento para leer tu codigo QR')

    # se obteine la informacion de la foto
    file_info = bot.get_file(message.photo[-1].file_id)

    # se descarga el archivo
    download_file = bot.download_file(file_info.file_path)

    # se crea un nombre para la foto quitando el /
    photo_name = file_info.file_path.split('/')[-1]

    # se crea la ruta para guardar la foto
    ruta = f'{photos_dir}{photo_name}'

    # se guarda la foto en la ruta
    with open(ruta, 'wb') as new_photo:
        new_photo.write(download_file)

    # se le envia al usuario el resultado
    resultado = leer_qr(ruta)
    if not resultado:
        bot.send_message(message.chat.id, MENSAJE_ERROR)
        os.remove(ruta)
    else:
        bot.send_message(message.chat.id, f'Enlace: {resultado}')
        os.remove(ruta)
        
    

        

if __name__ == '__main__':
    bot.infinity_polling()