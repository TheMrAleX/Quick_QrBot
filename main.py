# importaciones
import telebot
from telebot import types
from qr_man.image_proccessor import insertar_logo
from qr_man.tools import detectar_url
from qr_man.manager import crear_qr, leer_qr
import os
# importando dotenv para obtener el token del archivo .env
from dotenv import load_dotenv
# importando variables de var.py
from qr_man.var import MENSAJE_ERROR, photos_dir, proccessors_dir
# cargando dotenv y obteniendo TOKEN
load_dotenv()
TOKEN = os.getenv('TOKEN')

# instanciando el bot con el TOKEN
bot = telebot.TeleBot(TOKEN)

# diccionario para rastrear la ultima imagen
user_data = {}

# funcion que dice que hara el bot con el comando start
@bot.message_handler(commands=['start'])
def start(message):
    # da la bienvenida
    texto = '👋 ¡Bienvenido/a al Generador de QR!\nSimplemente envíame cualquier enlace y te devolveré una imagen con el código QR. ¡Así de sencillo! 🎯✨'
    bot.send_message(message.chat.id, texto)

# funcion que reacciona a cualquier mensaje que le envie el usuario
@bot.message_handler(func=lambda message: True)
def message_qr(message):
    # asumimos que el mensaje es una URL y la ponemos en minusculas
    url = message.text.lower()
    
    # con la funcion detectar url verificamos que sea una url
    if detectar_url(url) == False:
        # si no es una url le hacemos saber al usuario que no lo es
        bot.send_message(message.chat.id, 'Lo que enviaste no parece ser un enlace. 📎 Intenta copiarlo y pegarlo desde el navegador o asegúrate de agregar "www" o "http://" al principio. 🌐')
    else:
        # pero si es una url creamos el codigo qr con la funcion crear qr
        qr = crear_qr(url)
        # guardamos en el diccionario user data informacion de la imagen y el estado para despues trabajar con ellos al añadir una foto o editar el QR
        user_data[message.chat.id] = {'image': qr, 'state': 'waiting_action'}
        # aqui guardamos la imagen del qr en la ruta
        with open(qr, 'rb') as file:
            # creamos el marcador que contendra los botones para editar la foto
            markup = types.InlineKeyboardMarkup()
            add_photo_btn = types.InlineKeyboardButton('Agregar foto al QR', callback_data='add_photo')
            markup.add(add_photo_btn)
            # enviamos la foto con los marcadores
            bot.send_photo(message.chat.id, file, reply_markup=markup)

# funcion que recoge la llamada del marcador add_photo y demas
@bot.callback_query_handler(func=lambda call: True)
def handle_callback_query(call):
    # si la llamada es = a add_photo como lo programamos anteriormente significa que el usuario quiere agregar foto al qr
    if call.data == 'add_photo':
        # cambiar el estado para esperar la foto y avisamos al usuario para que envie la foto o el logo para insertarlo
        user_data[call.message.chat.id]['state'] = 'awaiting_photo'
        bot.send_message(call.message.chat.id, 'Envia la foto que quieras agregar al centro del QR, ("Escribe /cancel para cancelar esta operacion")')

# esta funcion se complementa con la anterior, esta esperando la foto para redondearla y agregarla al QR
@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get('state') == 'awaiting_photo', content_types='photo')
def add_photo_to_image(message):
    # detecta si no es una foto y es un mensaje que dice '/cancel' para cancelar la operacion
    if message.text == '/cancel':
        user_data[message.chat.id]['state'] = 'waiting_action'
        bot.send_message(message.chat.id, 'Accion cancelada')
    else:
        # vamos a trabajar sobre la imagen, obtenemos su ruta desde el diccionario
        image_data = user_data[message.chat.id]['image']
        # se obteine la informacion de la foto que el usuario mando
        file_info = bot.get_file(message.photo[-1].file_id)

        # se descarga el archivo que el usuario envia
        download_file = bot.download_file(file_info.file_path)

        # se crea un nombre para la foto quitando el /
        photo_name = file_info.file_path.split('/')[-1]

        # se crea la ruta para guardar la foto
        ruta = f'{proccessors_dir}{photo_name}'

        # se guarda la foto en la ruta
        with open(ruta, 'wb') as new_photo:
            new_photo.write(download_file)

        # redondeamos la foto y la inseratmos con nuestra funcion
        imagen_redondeada = insertar_logo(ruta, image_data)

        # guardamos la foto para enviarla al usuario
        with open(imagen_redondeada, 'rb') as image_rounded:
            bot.send_photo(message.chat.id, image_rounded)

        bot.send_message(message.chat.id, 'Nuevo codigo QR con imagen personalizada a sido creada correctamente')

        user_data[message.chat.id]['state'] = 'waiting_action'

        # eliminamos la foto que nos mando el usuario para optimizar espacio
        os.remove(ruta)
        os.remove(imagen_redondeada)


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