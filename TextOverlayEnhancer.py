import os
import numpy as np
import cv2
from PIL import Image
import glob

def solicitar_rutas():
    """Solicita al usuario las rutas de entrada y salida."""
    ruta_entrada = input("Por favor, ingresa la ruta completa del directorio de entrada: ")
    ruta_salida = input("Por favor, ingresa la ruta completa del directorio de salida: ")
    
    # Verifica que la ruta de entrada exista
    if not os.path.exists(ruta_entrada):
        print(f"Error: La carpeta de entrada '{ruta_entrada}' no existe.")
        return None, None
    
    # Crea la carpeta de salida si no existe
    if not os.path.exists(ruta_salida):
        try:
            os.makedirs(ruta_salida)
            print(f"Se ha creado la carpeta de salida: {ruta_salida}")
        except Exception as e:
            print(f"Error al crear la carpeta de salida: {e}")
            return None, None
    
    return ruta_entrada, ruta_salida

def recortar_cuadrado(imagen):
    """Recorta un cuadrado centrado de la imagen."""
    ancho, alto = imagen.size
    
    if ancho > alto:
        # Imagen más ancha que alta
        izquierda = (ancho - alto) // 2
        superior = 0
        derecha = izquierda + alto
        inferior = alto
    else:
        # Imagen más alta que ancha
        izquierda = 0
        superior = (alto - ancho) // 2
        derecha = ancho
        inferior = superior + ancho
    
    return imagen.crop((izquierda, superior, derecha, inferior))

def redimensionar_imagen(imagen, tamano=(1080, 1080)):
    """Redimensiona la imagen al tamaño especificado."""
    return imagen.resize(tamano, Image.Resampling.LANCZOS)

def apply_color_overlay(imagen, overlay_color=(0, 0, 0), alpha=0.5):
    """Aplica una superposición de color a la imagen."""
    imagen_rgba = imagen.convert("RGBA")
    overlay = Image.new("RGBA", imagen.size, overlay_color + (int(255 * alpha),))
    return Image.alpha_composite(imagen_rgba, overlay)

def apply_vignette(imagen_pil, vignette_intensity=-50):
    """Aplica un efecto de viñeta a la imagen."""
    # Convertir de PIL a OpenCV
    imagen_np = np.array(imagen_pil)
    imagen_cv = cv2.cvtColor(imagen_np, cv2.COLOR_RGBA2BGR)
    
    rows, cols = imagen_cv.shape[:2]
    X_resultant_kernel = cv2.getGaussianKernel(cols, cols / 2)
    Y_resultant_kernel = cv2.getGaussianKernel(rows, rows / 2)
    kernel = Y_resultant_kernel * X_resultant_kernel.T
    mask = 255 * kernel / np.linalg.norm(kernel)
    
    vignette = np.zeros_like(imagen_cv, dtype=np.uint8)
    for i in range(3):
        vignette[:, :, i] = imagen_cv[:, :, i] * (1 + vignette_intensity / 100 * mask)
    
    # Convertir de OpenCV a PIL
    vignette_pil = Image.fromarray(cv2.cvtColor(vignette, cv2.COLOR_BGR2RGB))
    return vignette_pil

def procesar_imagen(ruta_imagen, ruta_salida):
    """Procesa una imagen aplicando todos los efectos requeridos."""
    nombre_archivo = os.path.basename(ruta_imagen)
    ruta_salida_completa = os.path.join(ruta_salida, nombre_archivo)
    
    try:
        # Cargar la imagen
        imagen = Image.open(ruta_imagen)
        
        # Recortar cuadrado centrado
        imagen_cuadrada = recortar_cuadrado(imagen)
        
        # Redimensionar a 1080x1080
        imagen_redimensionada = redimensionar_imagen(imagen_cuadrada)
        
        # Aplicar superposición de color negro con opacidad 50%
        imagen_con_overlay = apply_color_overlay(imagen_redimensionada)
        
        # Aplicar efecto de viñeta
        imagen_final = apply_vignette(imagen_con_overlay)
        
        # Guardar la imagen con compresión del 90%
        imagen_final.convert("RGB").save(ruta_salida_completa, "JPEG", quality=90)
        
        return True
    except Exception as e:
        print(f"Error al procesar la imagen {nombre_archivo}: {e}")
        return False

def procesar_directorio(ruta_entrada, ruta_salida):
    """Procesa todas las imágenes JPG en el directorio de entrada."""
    # Obtener todas las imágenes JPG en la carpeta de entrada
    extensiones = ['*.jpg', '*.jpeg', '*.JPG', '*.JPEG']
    archivos_imagen = []
    for extension in extensiones:
        patron = os.path.join(ruta_entrada, extension)
        archivos_imagen.extend(glob.glob(patron))
    
    if not archivos_imagen:
        print(f"No se encontraron imágenes JPG en {ruta_entrada}")
        return 0
    
    # Contador para el seguimiento
    contador_exitosos = 0
    total_imagenes = len(archivos_imagen)
    
    print(f"Procesando {total_imagenes} imágenes...")
    
    # Procesar cada imagen
    for i, ruta_imagen in enumerate(archivos_imagen, 1):
        print(f"Procesando imagen {i}/{total_imagenes}: {os.path.basename(ruta_imagen)}")
        if procesar_imagen(ruta_imagen, ruta_salida):
            contador_exitosos += 1
    
    return contador_exitosos

def main():
    print("=== PROCESADOR DE IMÁGENES ===")
    print("Este script procesará todas las imágenes JPG en la carpeta especificada:")
    print("1. Recortará un cuadrado centrado de cada imagen")
    print("2. Redimensionará cada imagen a 1080x1080 píxeles")
    print("3. Aplicará una superposición de color negro con 50% de opacidad")
    print("4. Aplicará un efecto de viñeta")
    print("5. Guardará las imágenes procesadas con 90% de compresión JPG")
    print()
    
    # Solicitar rutas
    ruta_entrada, ruta_salida = solicitar_rutas()
    if not ruta_entrada or not ruta_salida:
        print("Proceso cancelado debido a rutas inválidas.")
        return
    
    # Procesar directorio
    imagenes_procesadas = procesar_directorio(ruta_entrada, ruta_salida)
    
    # Mostrar resumen
    print("\n=== RESUMEN ===")
    print(f"Imágenes procesadas con éxito: {imagenes_procesadas}")
    print(f"Las imágenes procesadas se guardaron en: {ruta_salida}")

if __name__ == "__main__":
    main()