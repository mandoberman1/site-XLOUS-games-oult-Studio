import re
import profanity

def normalize(text):
    """Функция нормализации текста: убирает пробелы и приводит к нижнему регистру"""
    return text.replace(" ", "").lower()

def replace_chars(word, replacements):
    """Функция для замены символов в словах на разрешённые"""
    pattern = ""
    for c in word:
        # Если символ есть в replacements, заменяем его на допустимые варианты
        if c in replacements:
            pattern += f"[{''.join(replacements[c])}]"
        else:
            # Если символ не имеет замен, оставляем его как есть
            pattern += c
    return pattern

def check_profanity(comment, banned_words, replacements):
    """Проверяет комментарий на запрещенные слова, используя обе проверки."""
    # Приводим весь текст к нижнему регистру и убираем пробелы
    normalized_comment = normalize(comment)
    
    # Разбиваем комментарий на слова
    words = normalized_comment.split()
    
    # Для каждого слова проверяем, есть ли запрещенные
    for word in words:
        # Для каждого запрещённого слова генерируем паттерн
        for banned_word in banned_words:
            # Генерируем регулярное выражение для запрещенного слова
            pattern = replace_chars(banned_word, replacements)
            
            # Проверяем, совпадает ли слово с запрещенным
            if re.search(pattern, word):
                print(f"Мат: {word}")  # Выводим слово, если оно совпало
                return True

    # Проверяем с помощью библиотеки better_profanity
    if profanity.contains_profanity(normalized_comment):  # Используем better_profanity для проверки
        return True

    return False

# Пример использования:
banned_words = ["пенис", "мат"]
replacements = {
    "е": ["е", "3"],  # Замена на 'е' или '3'
    "и": ["и", "1"],  # Замена на 'и' или '1'
}

comment = "пенис аааааа"
if check_profanity(comment, banned_words, replacements):
    print("Комментарий содержит мат")
else:
    print("Комментарий не содержит мата")
