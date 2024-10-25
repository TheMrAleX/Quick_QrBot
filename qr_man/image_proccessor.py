from PIL import Image, ImageDraw
from .tools import nombre_unico
from .var import proccessors_dir

def redondear_imagen(ruta_logo, ruta_imagen_original):
    # Abrir la imagen original
    original_image = Image.open(ruta_imagen_original)
    
    # Redimensionar el logo al 20% del tamaño de la imagen original
    logo = Image.open(ruta_logo)
    nuevo_ancho = int(0.2 * original_image.size[0])
    nuevo_alto = int(0.2 * original_image.size[1])
    logo = logo.resize((nuevo_ancho, nuevo_alto))

    # Crear una máscara para redondear el logo
    msk = Image.new('L', logo.size, 0)
    draw = ImageDraw.Draw(msk)
    draw.ellipse((0, 0, logo.size[0], logo.size[1]), fill=255)

    # Crear la imagen redondeada
    logo_rounded = Image.new('RGBA', logo.size)
    logo_rounded.paste(logo, (0, 0), msk)

    return logo_rounded, original_image

def insertar_logo(ruta_logo, ruta_imagen_original):
    logo, original_image = redondear_imagen(ruta_logo, ruta_imagen_original)

    # Calcular las coordenadas para centrar el logo
    x = (original_image.size[0] - logo.size[0]) // 2
    y = (original_image.size[1] - logo.size[1]) // 2

    # Pegar el logo redondeado en la imagen original
    original_image.paste(logo, (x, y), logo)
    
    ruta =f'{proccessors_dir}{nombre_unico()}'
    # Guardar la imagen resultante
    original_image.save(ruta)
    return ruta

# Uso de la función
# insertar_logo('ruta/al/logo.png', 'ruta/a/la/imagen/original.png')