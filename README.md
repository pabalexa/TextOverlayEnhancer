# Procesador de Imágenes con Efectos y Ajustes de Contraste

## Objetivo del Código

Este código tiene como objetivo procesar imágenes JPG en un directorio especificado por el usuario. El procesamiento incluye varios efectos visuales que mejoran la imagen para su uso posterior, especialmente cuando se requiere colocar texto sobre ella con buen contraste. Los efectos aplicados a cada imagen son:

1. Recorte centrado en un cuadrado.
2. Redimensionamiento a un tamaño de 1080x1080 píxeles.
3. Aplicación de una superposición de color negro con opacidad del 50%.
4. Adición de un efecto de viñeta.

El resultado final es una imagen optimizada para insertar texto blanco de manera que el texto resalte adecuadamente sobre la imagen debido al contraste.

## Instrucciones de Uso

1. **Requisitos Previos**:
   - Tener instalado Python 3.x.
   - Instalar las siguientes bibliotecas de Python:
     - `numpy`: `pip install numpy`
     - `opencv-python`: `pip install opencv-python`
     - `Pillow`: `pip install Pillow`
2. **Ejecutar el Script**:

   - Guarda el código en un archivo llamado `procesador_imagenes.py`.
   - Ejecuta el script desde la terminal o consola de comandos con el siguiente comando:
     ```bash
     python procesador_imagenes.py
     ```
   - El script solicitará dos rutas:
     - **Ruta de entrada**: El directorio donde se encuentran las imágenes a procesar.
     - **Ruta de salida**: El directorio donde se guardarán las imágenes procesadas.

3. **Proceso de Ejecución**:
   - El script buscará todas las imágenes con extensión `.jpg`, `.jpeg`, `.JPG` y `.JPEG` en la carpeta de entrada.
   - Procesará cada imagen aplicando los efectos mencionados.
   - Guardará las imágenes procesadas con una compresión del 90% en formato JPG en la carpeta de salida.

## Explicación del Funcionamiento

El código está diseñado para trabajar de manera automática con todas las imágenes en un directorio. A continuación, se describe el flujo de trabajo:

1. **Solicitud de Rutas**: Se le pide al usuario que ingrese las rutas de los directorios de entrada y salida a través de la consola.
2. **Verificación de Rutas**: El script verifica que la carpeta de entrada exista. Si la carpeta de salida no existe, se crea automáticamente.
3. **Procesamiento de Imágenes**: El script recorre todas las imágenes en el directorio de entrada:
   - **Recorte Cuadrado**: Si la imagen es rectangular, se recorta a un cuadrado centrado.
   - **Redimensionamiento**: Se cambia el tamaño de la imagen a 1080x1080 píxeles.
   - **Superposición de Color**: Se aplica un filtro de superposición de color negro con opacidad del 50%.
   - **Viñeta**: Se agrega un efecto de viñeta a la imagen para mejorar el contraste y enfocar la atención en el centro de la imagen.
4. **Guardado de Imágenes**: Las imágenes procesadas se guardan en el directorio de salida con un nivel de compresión del 90% en formato JPG.

## Detalles de los Algoritmos

### Recorte Cuadrado

Este algoritmo toma una imagen rectangular y la recorta a un cuadrado centrado. Si la imagen es más ancha que alta, el recorte se realiza en el centro horizontal, manteniendo la altura completa. Si la imagen es más alta que ancha, el recorte se hace en el centro vertical, manteniendo el ancho completo.

### Redimensionamiento

El redimensionamiento cambia el tamaño de la imagen a 1080x1080 píxeles utilizando el algoritmo de reescalado de alta calidad `LANCZOS`, que es conocido por producir una reducción de tamaño sin pérdida significativa de calidad.

### Superposición de Color

Se aplica una capa de color sobre la imagen con una opacidad del 50%. Esto se logra combinando la imagen original con una capa semi-transparente del color deseado. El valor de opacidad es configurable y el color por defecto es negro `(0, 0, 0)`.

### Efecto de Viñeta

Se genera un filtro de viñeta mediante un kernel gaussiano, el cual atenúa progresivamente los bordes de la imagen, creando un efecto de oscurecimiento en las esquinas. Este efecto mejora el contraste para que el contenido central de la imagen sea el foco principal.

## Explicación Técnica de los Algoritmos

### Complejidad y Rendimiento

- **Recorte Cuadrado**: Este algoritmo tiene una complejidad constante `O(1)` ya que simplemente calcula los bordes del recorte de acuerdo con el tamaño de la imagen.
- **Redimensionamiento**: El redimensionamiento tiene una complejidad de `O(n*m)`, donde `n` es la altura de la imagen y `m` es el ancho, ya que requiere cambiar el tamaño de cada píxel de la imagen.
- **Superposición de Color**: La superposición de color también tiene una complejidad `O(n*m)`, ya que se debe combinar cada píxel de la imagen con la capa de color.
- **Efecto de Viñeta**: La creación de la máscara gaussiana y su aplicación tiene una complejidad de `O(n*m)`.

El rendimiento es adecuado para procesar imágenes de tamaño moderado en una máquina común, pero si se planea procesar un gran número de imágenes de alta resolución, es recomendable ejecutar el código en un entorno optimizado.

## Estructura del Código

El código está organizado en funciones independientes, cada una encargada de una tarea específica:

- **solicitar_rutas()**: Solicita las rutas de entrada y salida del usuario, validándolas.
- **recortar_cuadrado(imagen)**: Recorta la imagen a un cuadrado centrado.
- **redimensionar_imagen(imagen, tamano=(1080, 1080))**: Redimensiona la imagen a 1080x1080 píxeles.
- **apply_color_overlay(imagen, overlay_color=(0, 0, 0), alpha=0.5)**: Aplica una superposición de color sobre la imagen con opacidad configurable.
- **apply_vignette(imagen_pil, vignette_intensity=-50)**: Aplica un efecto de viñeta a la imagen.
- **procesar_imagen(ruta_imagen, ruta_salida)**: Procesa una imagen aplicando todos los efectos.
- **procesar_directorio(ruta_entrada, ruta_salida)**: Procesa todas las imágenes en el directorio de entrada.
- **main()**: Controla el flujo del programa, gestionando las rutas de entrada y salida y procesando las imágenes.

## Ejemplos de Entrada y Salida

### Entrada

- **Ruta de Entrada**: `C:/imagenes/entrada/`
- **Ruta de Salida**: `C:/imagenes/salida/`
- **Imágenes en Entrada**:
  - `imagen1.jpg`
  - `imagen2.jpeg`

### Salida

- **Imágenes Procesadas**:
  - `imagen1.jpg` (con recorte cuadrado, redimensionada, con superposición de color y viñeta aplicada)
  - `imagen2.jpeg` (similar al anterior)

## Manejo de Errores

El código maneja varios tipos de errores y excepciones:

- **Error de Ruta**: Si la ruta de entrada no existe o la de salida no se puede crear, se muestra un mensaje de error y el proceso se detiene.
- **Error en Procesamiento de Imagen**: Si ocurre un error durante la carga o el procesamiento de una imagen (por ejemplo, si el archivo está dañado), se captura la excepción y se muestra un mensaje de error sin detener el procesamiento de las demás imágenes.

## Dependencias y Requisitos

- **Python 3.x**.
- **Bibliotecas**:
  - `numpy`: `pip install numpy`
  - `opencv-python`: `pip install opencv-python`
  - `Pillow`: `pip install Pillow`

## Notas sobre Rendimiento y Optimización

El código está diseñado para ser flexible y fácil de usar en proyectos pequeños y medianos. La optimización principal se ha centrado en garantizar que el procesamiento de las imágenes sea de calidad y que los efectos visuales sean aplicados de manera eficiente.

## Comentarios Dentro del Código

Los comentarios dentro del código explican cada función y su propósito. También se detallan los pasos dentro de las funciones complejas, como el cálculo de las coordenadas para el recorte cuadrado y la aplicación de la viñeta.

Este código es fácilmente ampliable, y puedes añadir más efectos visuales o ajustes según sea necesario.
