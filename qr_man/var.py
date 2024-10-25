import os

# Nombre del proyecto
PROYECTO = 'Quick_QrBot'

# Mensaje de error personalizado
MENSAJE_ERROR = '❌ ¡Oops! No se pudo leer el código QR. 📷🚫.\nPor favor, intenta de nuevo enviando una imagen clara y nítida del código. 😊🔍'

# Variable para indicar si estamos en producción o no
produccion = False  # Puedes cambiar esto a True directamente o usar una variable de entorno

# Directorios por defecto
photos_dir = 'photos/'
output_dir = 'output/'
proccessors_dir = 'image_proccessor/'

# Si estamos en producción, ajustar las rutas con el nombre del proyecto
if produccion:
    photos_dir = f'{PROYECTO}/{photos_dir}'
    output_dir = f'{PROYECTO}/{output_dir}'
    proccessors_dir = f'{PROYECTO}/{proccessors_dir}'


