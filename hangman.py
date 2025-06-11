import random
import os
import unicodedata

# Mensajes en diferentes idiomas
MESSAGES = {
    "english": {
        "welcome": "Welcome to the Hangman Game!",
        "choose_language": "Choose a language (english/spanish): ",
        "choose_category": "Choose a category (animals, food): ",
        "choose_difficulty": "Choose difficulty (easy/medium/hard): ",
        "tries_left": "You have {} tries left.",
        "guessed_letters": "Guessed letters: {}",
        "word": "Word: {}",
        "guess_letter": "Guess a letter: ",
        "invalid_letter": "Please enter a valid letter.",
        "already_guessed": "You already guessed that letter. Try another one.",
        "correct_guess": "Good! That letter is in the word.",
        "incorrect_guess": "Sorry, that letter is not in the word.",
        "you_won": "You won! The word was: {}",
        "you_lost": "You lost! The word was: {}",
        "score": "Your score: {}",
        "high_scores": "High Scores:\n{}",
        "play_again": "Do you want to play again? (Y/N): ",
        "file_not_found": "Error: Word file not found for category '{}'. Creating default file.",
        "no_words": "Error: No valid words found for the selected category and difficulty (min_length={}, max_length={}). Using default words.",
        "debug_reading_file": "Reading file '{}': found words: {}",
        "debug_filtered_words": "After filtering (min_length={}, max_length={}): {}"
    },
    "spanish": {
        "welcome": "¡Bienvenido al Juego del Ahorcado!",
        "choose_language": "Elige un idioma (english/spanish): ",
        "choose_category": "Elige una categoría (animales, comida): ",
        "choose_difficulty": "Elige la dificultad (facil/medio/dificil): ",
        "tries_left": "Te quedan {} intentos.",
        "guessed_letters": "Letras adivinadas: {}",
        "word": "Palabra: {}",
        "guess_letter": "Adivina una letra: ",
        "invalid_letter": "Por favor, ingresa una letra válida.",
        "already_guessed": "Ya has adivinado esa letra. Intenta otra.",
        "correct_guess": "¡Bien! Esa letra está en la palabra.",
        "incorrect_guess": "Lo siento, esa letra no está en la palabra.",
        "you_won": "¡Ganaste! La palabra era: {}",
        "you_lost": "¡Perdiste! La palabra era: {}",
        "score": "Tu puntuación: {}",
        "high_scores": "Puntuaciones más altas:\n{}",
        "play_again": "¿Quieres jugar de nuevo? (S/N): ",
        "file_not_found": "Error: No se encontró el archivo de palabras para la categoría '{}'. Creando archivo predeterminado.",
        "no_words": "Error: No se encontraron palabras válidas para la categoría y dificultad seleccionadas (min_length={}, max_length={}). Usando palabras predeterminadas.",
        "debug_reading_file": "Leyendo archivo '{}': palabras encontradas: {}",
        "debug_filtered_words": "Después de filtrar (min_length={}, max_length={}): {}"
    }
}

# Configuración de niveles de dificultad
DIFFICULTY_LEVELS = {
    "easy": {"min_length": 4, "max_length": 6, "tries": 8},
    "medium": {"min_length": 7, "max_length": 9, "tries": 6},
    "hard": {"min_length": 10, "max_length": 15, "tries": 4}
}

# Traducciones de dificultades (español a inglés)
DIFFICULTY_TRANSLATIONS = {
    "facil": "easy",
    "medio": "medium",
    "dificil": "hard",
    "easy": "easy",
    "medium": "medium",
    "hard": "hard"
}

# Categorías por idioma
CATEGORIES = {
    "english": ["animals", "food"],
    "spanish": ["animales", "comida"]
}

# Palabras predeterminadas por idioma y categoría
DEFAULT_WORDS = {
    "english": {
        "animals": ["dog", "cat", "elephant", "tiger", "lion"],
        "food": ["bread", "apple", "pizza", "taco", "cheese"]
    },
    "spanish": {
        "animales": ["perro", "gato", "elefante", "tigre", "leon"],
        "comida": ["pan", "manzana", "pizza", "taco", "queso"]
    }
}

def normalize_word(word):
    """Normaliza una palabra eliminando tildes y convirtiendo a mayúsculas."""
    # Normalizar la palabra para descomponer tildes (por ejemplo, á -> a + tilde)
    normalized = unicodedata.normalize('NFKD', word)
    # Eliminar los caracteres diacríticos (tildes) y mantener solo las letras base
    without_diacritics = ''.join(c for c in normalized if not unicodedata.combining(c))
    return without_diacritics.upper()

def load_words(language, category, min_length, max_length):
    """Carga palabras desde un archivo según idioma, categoría y longitud."""
    filename = os.path.join("words", language, f"{category}.txt")
    
    # Crear directorio y archivo predeterminado si no existen
    if not os.path.exists(os.path.dirname(filename)):
        os.makedirs(os.path.dirname(filename))
    
    if not os.path.exists(filename):
        print(MESSAGES[language]["file_not_found"].format(category))
        with open(filename, "w", encoding="utf-8") as file:
            for word in DEFAULT_WORDS[language][category]:
                file.write(word + "\n")
    
    # Leer palabras del archivo
    with open(filename, "r", encoding="utf-8") as file:
        words = [line.strip() for line in file if line.strip()]
    
    # Depuración: Mostrar palabras leídas
    print(MESSAGES[language]["debug_reading_file"].format(filename, words))
    
    # Filtrar palabras por longitud
    # Normalizamos las palabras para el filtrado, pero mantenemos la versión original para mostrar
    filtered_words = []
    for word in words:
        normalized_word = normalize_word(word)
        if min_length <= len(normalized_word) <= max_length:
            filtered_words.append(word.upper())  # Guardamos la palabra original en mayúsculas
    
    # Depuración: Mostrar palabras después de filtrar
    print(MESSAGES[language]["debug_filtered_words"].format(min_length, max_length, filtered_words))
    
    # Si no hay palabras válidas, usar las predeterminadas
    if not filtered_words:
        print(MESSAGES[language]["no_words"].format(min_length, max_length))
        default_words = [word.upper() for word in DEFAULT_WORDS[language][category] if min_length <= len(word) <= max_length]
        print(MESSAGES[language]["debug_filtered_words"].format(min_length, max_length, default_words))
        return default_words
    
    return filtered_words

def get_word(words):
    """Elige una palabra al azar de la lista."""
    return random.choice(words)

def display_hangman(tries, max_tries):
    """Muestra el dibujo del ahorcado según los intentos restantes."""
    stages = [
        # 8 intentos (inicio para dificultad fácil) - Ahorcado vacío
        """
           --------
           |      |
           |
           |
           |
           |
           -
        """,
        # 7 intentos
        """
           --------
           |      |
           |
           |
           |
           |
           -
        """,
        # 6 intentos
        """
           --------
           |      |
           |      O
           |
           |
           |
           -
        """,
        # 5 intentos
        """
           --------
           |      |
           |      O
           |      |
           |      |
           |
           -
        """,
        # 4 intentos
        """
           --------
           |      |
           |      O
           |     \\|
           |      |
           |
           -
        """,
        # 3 intentos
        """
           --------
           |      |
           |      O
           |     \\|/
           |      |
           |
           -
        """,
        # 2 intentos
        """
           --------
           |      |
           |      O
           |     \\|/
           |      |
           |     /
           -
        """,
        # 1 intento
        """
           --------
           |      |
           |      O
           |     \\|/
           |      |
           |     / \\
           -
        """,
        # 0 intentos (perdido) - Ahorcado completo
        """
           --------
           |      |
           |      O
           |     \\|/
           |      |
           |     / \\
           -
        """
    ]
    # Calcular el índice: cuando tries es max_tries, mostramos el ahorcado vacío (índice 0)
    # Cuando tries es 0, mostramos el ahorcado completo (índice len(stages) - 1)
    index = int(((max_tries - tries) / max_tries) * (len(stages) - 1))
    print(f"Debug: tries={tries}, max_tries={max_tries}, index={index}")
    return stages[index]

def save_score(score, language, category, difficulty):
    """Guarda la puntuación en un archivo."""
    with open("high_scores.txt", "a", encoding="utf-8") as file:
        file.write(f"{language},{category},{difficulty},{score}\n")

def load_high_scores():
    """Carga las puntuaciones más altas."""
    scores = []
    try:
        with open("high_scores.txt", "r", encoding="utf-8") as file:
            for line in file:
                language, category, difficulty, score = line.strip().split(",")
                scores.append((language, category, difficulty, int(score)))
        scores.sort(key=lambda x: x[3], reverse=True)
        return scores[:5]
    except FileNotFoundError:
        return []

def play_hangman():
    # Elegir idioma
    language = input(MESSAGES["english"]["choose_language"]).lower()
    while language not in ["english", "spanish"]:
        print("Please choose 'english' or 'spanish'.")
        language = input(MESSAGES["english"]["choose_language"]).lower()

    # Elegir categoría
    print(MESSAGES[language]["choose_category"])
    category = input().lower()
    while category not in CATEGORIES[language]:
        print(f"Please choose one of: {', '.join(CATEGORIES[language])}")
        category = input(MESSAGES[language]["choose_category"]).lower()

    # Elegir dificultad
    print(MESSAGES[language]["choose_difficulty"])
    difficulty_input = input().lower()
    while difficulty_input not in DIFFICULTY_TRANSLATIONS:
        print("Please choose a valid difficulty.")
        difficulty_input = input(MESSAGES[language]["choose_difficulty"]).lower()
    
    # Mapear la entrada del usuario a la clave en inglés
    difficulty = DIFFICULTY_TRANSLATIONS[difficulty_input]

    # Configurar según la dificultad
    min_length = DIFFICULTY_LEVELS[difficulty]["min_length"]
    max_length = DIFFICULTY_LEVELS[difficulty]["max_length"]
    max_tries = DIFFICULTY_LEVELS[difficulty]["tries"]
    tries = max_tries

    # Cargar palabras
    words = load_words(language, category, min_length, max_length)
    if not words:
        print(MESSAGES[language]["no_words"].format(min_length, max_length))
        return

    word = get_word(words)
    word_letters = set(normalize_word(word))  # Normalizar para comparar letras
    alphabet = set("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    guessed_letters = set()

    # Bucle principal del juego
    while len(word_letters) > 0 and tries > 0:
        print(MESSAGES[language]["tries_left"].format(tries))
        print(display_hangman(tries, max_tries))
        print(MESSAGES[language]["guessed_letters"].format(" ".join(guessed_letters)))
        word_display = [letter if normalize_word(letter) in guessed_letters else "_" for letter in word]
        print(MESSAGES[language]["word"].format(" ".join(word_display)))

        guess = input(MESSAGES[language]["guess_letter"]).upper()
        if guess not in alphabet:
            print(MESSAGES[language]["invalid_letter"])
        elif guess in guessed_letters:
            print(MESSAGES[language]["already_guessed"])
        else:
            guessed_letters.add(guess)
            if guess in word_letters:
                word_letters.remove(guess)
                print(MESSAGES[language]["correct_guess"])
            else:
                tries -= 1
                print(MESSAGES[language]["incorrect_guess"])

    # Fin del juego
    if tries == 0:
        print(display_hangman(tries, max_tries))
        print(MESSAGES[language]["you_lost"].format(word))
        score = 0
    else:
        difficulty_factor = {"easy": 1, "medium": 2, "hard": 3}
        score = len(word) * tries * difficulty_factor[difficulty]
        print(MESSAGES[language]["you_won"].format(word))
        print(MESSAGES[language]["score"].format(score))

    # Guardar puntuación
    save_score(score, language, category, difficulty)

    # Mostrar puntuaciones más altas
    high_scores = load_high_scores()
    high_scores_display = "\n".join(
        f"{lang} - {cat} ({diff}): {score}" for lang, cat, diff, score in high_scores
    )
    print(MESSAGES[language]["high_scores"].format(high_scores_display))

if __name__ == "__main__":
    print(MESSAGES["english"]["welcome"])
    play_hangman()
    while input(MESSAGES["english"]["play_again"]).upper() in ["Y", "S"]:
        play_hangman()