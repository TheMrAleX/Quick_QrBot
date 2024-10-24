PROYECTO = 'Quick_QrBot'

MENSAJE_ERROR = '❌ ¡Oops! No se pudo leer el código QR. 📷🚫.\nPor favor, intenta de nuevo enviando una imagen clara y nítida del código. 😊🔍'

produccion = False

photos_dir = 'photos/'

output_dir = 'output/'

produccion = False

if produccion:
    photos_dir = f'{PROYECTO}/{photos_dir}'
    output_dir = f'{PROYECTO}/{output_dir}'