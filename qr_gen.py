# importaciones 
import qrcode
import os
from tools import gradient, nombre_unico
from qrcode.image.styledpil import StyledPilImage
import qrcode.constants
from qrcode.image.styles.moduledrawers import RoundedModuleDrawer

base_dir ='output/'
# funcion que crea el QR sin agregados
def crear_qr(url):
    # creamos el objeto qr con estos datos estandar que vu en la documentacion
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=2)

    qr.add_data(url)
    qr.make(fit=True)

    # creamos a imagen de qr ligeramente redondeada que tambie vi en la documentacion jaja
    image = qr.make_image(fill_color="black",
        back_color="white",
        image_factory=StyledPilImage,
        module_drawer=RoundedModuleDrawer(radius_ratio=1),
        eye_drawer= RoundedModuleDrawer(radius_ratio=1))
        
    # creamos un nombre unico para este QR original
    nombre = nombre_unico()
    # salvamos el QR original con el nombre unico
    image.save(f'{base_dir}{nombre}')

    # creamos nombre nuevo para el output que ya tendra los estilos aplicados
    nombre_nuevo = nombre_unico()

    # aplicamos el gradiente con la funcion del archivo tools.py
    gradient(f'{base_dir}{nombre}', f'{base_dir}{nombre_nuevo}')

    # borramos el original
    os.remove(f'{base_dir}{nombre}')

    # retornamos la ruta del estilizado
    return f'{base_dir}{nombre_nuevo}'  