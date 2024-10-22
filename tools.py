# importaciones
from PIL import Image, ImageOps, ImageDraw
import uuid

# funcion que crea el degradado, se pide altura y ancho mas los 2 colores
def degradado(width, height, color1, color2):
    # creamos una imagen con el degradado del tamano de la imagen original
    gradient = Image.new('RGB', (width, height))
    draw = ImageDraw.Draw(gradient)

    # asignamos cada valor de color a su respectivo tono rgb
    r1, g1, b1 = color1
    r2, g2, b2 = color2

    for x in range(height):
        # dibujamos el degradado en el bucle for
        r= int(r1 + (r2 - r1) * (x / height))
        g= int(g1 + (g2 - g1) * (x / height))
        b= int(b1 + (b2 - b1) * (x / height))

        draw.line((0, x, width, x), fill=(r, g, b))

    # retornamos el degradado para trabajarlo despues
    return gradient

# funcion que aplica y exporta el degradado, pide ruta de entrada y salida
def gradient(img_path, outpu_path="qr_deg.png"):
    # abre la imagen original sin estilos
    image = Image.open(img_path)
    # la convierte a escala de grises para mejor deteccion (eso dice google)
    gray_image = ImageOps.grayscale(image)
    # esta es la tolerancia para deteccion de pixeles negros
    threshold = 100
    # mascara convierte la imagen a una mascara de capa 
    mask = gray_image.point(lambda p : 255 if p < threshold else 0)
    # los dos colores para degradado el rosa y el verde
    color1 = (0, 128, 255)
    color2 = (44, 187, 47)
    # obtenemos el ancho y alto del qr original con esta funcion
    width, height = image.size
    # creamos el degradado con los datos creados
    deg = degradado(width, height, color1, color2)
    # se compone todo y se guarda
    qr_dregaded = Image.composite(deg, image.convert('RGB'), mask)
    qr_dregaded.save(outpu_path)

# funcion que crea y devuelve un nombre unico con la extension png (no hay misterio)
def nombre_unico(extension='png'):
    nombre_unico = str(uuid.uuid4())

    return f'{nombre_unico}.{extension}'

def detectar_url(url):
    import re
    patron_url = re.compile(
        r'^(https?|ftp)://'        # Protocolo (http, https o ftp)
        r'|^www\.'                 # O que comiencen por 'www.'
        r'([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}'  # Dominio
        r'(:\d+)?'                 # Puerto (opcional)
        r'(\/[^\s]*)?$'            # Ruta (opcional)
    )

    x= re.match(patron_url, url)
    
    if x is not None:
        print('es url')
        return url
    else:
        return False