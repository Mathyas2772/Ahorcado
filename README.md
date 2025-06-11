# Juego del Ahorcado Multilingüe

Este proyecto implementa el juego del ahorcado con soporte para múltiples idiomas (español e inglés), categorías, niveles de dificultad y un sistema de puntuación. Las palabras están organizadas en archivos locales por idioma y categoría, y el programa crea automáticamente los directorios y archivos si no existen. Soporta palabras con tildes en español.

## Habilidades Demostradas
- Manejo avanzado de archivos y directorios.
- Internacionalización (i18n) con mensajes en múltiples idiomas.
- Lógica de juego con niveles de dificultad y puntuación.
- Manejo de caracteres especiales (tildes) con `unicodedata`.

## Categorías Disponibles
- **Animales** (Animals): Nombres de animales.
- **Comida** (Food): Tipos de alimentos, como frutas, platos y postres.

## Estructura del Proyecto
- `words/english/`: Palabras en inglés por categoría (`animals.txt`, `food.txt`).
- `words/spanish/`: Palabras en español por categoría (`animales.txt`, `comida.txt`).
- `high_scores.txt`: Almacena las puntuaciones más altas.

## Cómo Ejecutarlo
1. Asegúrate de que la carpeta `words/` esté en el mismo directorio que `hangman.py`.
2. Ejecuta el script:
```
python hangman.py
```
