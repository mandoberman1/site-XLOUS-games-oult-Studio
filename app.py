from flask import Flask, request, render_template, redirect, flash, url_for
import os
from datetime import datetime
from html import escape
from itertools import permutations
from better_profanity import profanity  # Здесь используем better_profanity
from profanity import profanity as profan  # Дополнительно для фильтрации других слов
import re
# Настройка better-profanity
profanity.load_censor_words()

app = Flask(__name__, static_folder='static')
app.secret_key = 'supersecretkey123476'
filename = 'comments.txt'
# Уникальные матерные слова
banned_words = [
"ебал", "хохол","пенис", "fuck", "shit", "bitch", "asshole", "bastard", "dick", "pussy", "cock", 
    "cunt", "slut", "whore", "fag", "gay", "nigger", "chink", "spic", "retard", "motherfucker", 
    "goddamn", "sonofabitch", "cocksucker", "shithead", "prick", "twat", "wanker", "fucker", 
    "dipshit", "jackass", "douchebag", "cockhead", "asshat", "shitbag", "faggot", "shitstain", 
    "pussylicker", "bastardize", "mothereffer", "dickhead", "fuckhead", "cuntface", "douche", 
    "skank", "whorebag", "slutty", "shitfaced", "tits", "boobs", "vagina", "penis", "fisting", 
    "blowjob", "handjob", "rimjob", "spank", "fucktard", "cumdumpster", "cumrag", "cocktease", 
    "bitchass", "dickweed", "shitlord", "asswipe", "bitchslap", "crackwhore", "gash", "turd", 
    "fudgepacker", "blowjobber", "cockblock", "spunk", "ejaculate", "testicle", "buttsex", 
    "bukkake", "dildo", "strapon", "gangbang", "horny", "pervert", "freak", "kinky", "wetdream", 
    "мат", "сука", "блядь", "хуй", "пизда", "ебать", "жопа", "гондон", "урод", "козел", 
    "сучка", "тварь", "пидор", "пидорас", "мразь", "гнида", "хуйня", "еблан", "блядский", 
    "пиздец", "ссать", "хуесос", "уродливый", "залупа", "пошел нахуй", "заебал", "шлюха", 
    "ебаться", "сукина", "бля", "пидар", "хач", "говно", "осел", "хрень", "срака", 
    "пошел в жопу", "дибил", "тупой", "дурак", "сучара", "пидорасик", "херачить", "пиздить", 
    "долбоеб", "мудила", "сосать", "пиздун", "попа", "пиздец", "придурок", "голубой", 
    "тварь", "чертов", "чмо", "идиот", "отбитый", "скотина", "псих", "пиздюк", "соси", 
    "жена-хуи", "тыжпидор", "заморочить", "фак", "срань", "секс", "педрила", "жополиз", 
    "хуячить", "гондон", "сучить", "дура", "сволочь", "хуйловод", "вздрочить", "ебу", 
    "плоть", "дебил", "шлюшка", "гнидить", "дебильный", "питух", "пиздобол", "сукин сын", 
    "поебень", "барак", "пендаль", "козлина", "попердеть", "ебанина", "досить", "пестить", 
    "залупить", "срам", "порнуха", "говноед", "люйка", "жопоед", "чучело", "отсосать", 
    "залупать", "туз", "петушок", "хрюкать", "манда", "петушарник", "песюк", "пиздолиз", "долбаеб", "сука",
    "пердосбор", "очкоклеп", "залупопот", "траходон", "дрислопадло", "пуклятинка", "сракокрай", 
    "пердохрюк", "говнобайтер", "жироплюх", "залупофлекс", "очкокрут", "дрислодыр", "трахогон", 
    "говнокрут", "пердозахват", "сракобомб", "пукосрач", "залупокос", "мозгофейспалм", "обосрос", 
    "пердозавр", "очкодавилка", "сракопукарь", "залупорванец", "траходед", "жиросвин", "пуклопот", 
    "дрисломес", "залупоскок", "говнобой", "сракоканон", "пердодел", "пукляшок", "обосранка", 
    "жиромразь", "трахоплав", "залупоклон", "пердослава", "дрислотень", "очкометатель", 
    "пукопоток", "сракогром", "пердозатоп", "говноклинер", "залупогрей", "трахосвет", "пукоскоп", 
    "обдрочунчик", "соплекус", "пердосектор", "жирозавр", "дрисловоз", "сракокумар", 
    "залупоган", "очкочертила", "пердодемон", "сракотроль", "обосратень", "залупокороль", 
    "трахорез", "мозгоклев", "пердодух", "говномудрец", "сракопадло", "пуклягрант", 
    "залупоруб", "дрислопрыск", "очковёрт", "жиромяс", "трахозвучок", "сракочлен", 
    "пердохмур", "пукодыр", "залуповерт", "говнолаз", "дрислопадик", "мозгофил", 
    "пердомразь", "обосрачник", "сракопых", "жирослон", "пуклопрыск", "залупофикс", 
    "трахолоб", "очкомешок", "дрислофейл", "пердокорм", "говнокритик", "залупоцарь", 
    "сракозлыдень", "обосрун", "пердолоб", "очкомастер", "трахобахнутый", "жиродыр", 
    "дрислотун", "мозгоклюв", "сракодух", "пуклячек", "пердопетля", "очкострах", 
    "залуповозка", "трахопот", "сракозвук", "обдриська", "жирометатель", "пукогром", 
    "залупозон", "дрислопляс", "пердокнязь", "очкопых", "сракокуча", "залупоквак", 
    "обсирунчик", "жиропупс", "пердоквакарь", "мозгохрюк", "очкомётчик", "сракопуш", 
    "дрислоподрыв","сука", "сучка","пукловест", "трахорезка", "залупонос", "пердолюк", "очкозавод", 
    "дрочка","обосранство", "жиропылесос", "трахофеер", "пуклопуть", "залупокосарь", "пердозвукарь", "ебать", "ебанный", "ебаный", "тупой", "шлюха", "проститука", "гандон"
]
profanity.load_censor_words(banned_words)  # Загружаем твой список в better_profanity

# Функция для чтения комментариев
def read_comments():
    comments = []
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            comments = f.readlines()
    return comments

# Проверка, был ли уже комментарий от этого IP
def check_ip(ip):
    comments = read_comments()
    for comment in comments:
        stored_ip, _, _, _ = comment.strip().split('|')
        if stored_ip == ip:
            return True
    return False

# Проверка на одинаковые имена
def check_duplicate_name(username):
    comments = read_comments()
    for comment in comments:
        _, stored_username, _, _ = comment.strip().split('|')
        if stored_username.lower() == username.lower():
            return True
    return False


# Полный список замен символов на буквы
replacements = {
    'а': ["аa@4",'а', '№', ';', '%', ':', '?', '*', '(', ')', '!', '@', '/', '*', '-', '+', "'", '[', ']'],
    'б': ['б', '№', ';', '%', ':', '?', '*', '(', ')', '!', '@', '/', '*', '-', '+', "'", '[', ']'],
    'в': ['в', '№', ';', '%', ':', '?', '*', '(', ')', '!', '@', '/', '*', '-', '+', "'", '[', ']'],
    'г': ['г', '№', ';', '%', ':', '?', '*', '(', ')', '!', '@', '/', '*', '-', '+', "'", '[', ']'],
    'д': ['д', '№', ';', '%', ':', '?', '*', '(', ')', '!', '@', '/', '*', '-', '+', "'", '[', ']'],
    'е': ['е', '№', ';', '%', ':', '?', '*', '(', ')', '!', '@', '/', '*', '-', '+', "'", '[', ']'],
    'ж': ['ж', '№', ';', '%', ':', '?', '*', '(', ')', '!', '@', '/', '*', '-', '+', "'", '[', ']'],
    'з': ['з', '№', ';', '%', ':', '?', '*', '(', ')', '!', '@', '/', '*', '-', '+', "'", '[', ']'],
    'и': ['и', '№', ';', '%', ':', '?', '*', '(', ')', '!', '@', '/', '*', '-', '+', "'", '[', ']'],
    'й': ['й', '№', ';', '%', ':', '?', '*', '(', ')', '!', '@', '/', '*', '-', '+', "'", '[', ']'],
    'к': ['к', '№', ';', '%', ':', '?', '*', '(', ')', '!', '@', '/', '*', '-', '+', "'", '[', ']'],
    'л': ['л', '№', ';', '%', ':', '?', '*', '(', ')', '!', '@', '/', '*', '-', '+', "'", '[', ']'],
    'м': ['м', '№', ';', '%', ':', '?', '*', '(', ')', '!', '@', '/', '*', '-', '+', "'", '[', ']'],
    'н': ['н', '№', ';', '%', ':', '?', '*', '(', ')', '!', '@', '/', '*', '-', '+', "'", '[', ']'],
    'о': ['о','0', '№', ';', '%', ':', '?', '*', '(', ')', '!', '@', '/', '*', '-', '+', "'", '[', ']'],
    'п': ['п', '№', ';', '%', ':', '?', '*', '(', ')', '!', '@', '/', '*', '-', '+', "'", '[', ']'],
    'р': ['р', '№', ';', '%', ':', '?', '*', '(', ')', '!', '@', '/', '*', '-', '+', "'", '[', ']'],
    'с': ['с', '№', ';', '%', ':', '?', '*', '(', ')', '!', '@', '/', '*', '-', '+', "'", '[', ']'],
    'т': ['т', '№', ';', '%', ':', '?', '*', '(', ')', '!', '@', '/', '*', '-', '+', "'", '[', ']'],
    'у': ['у', '№', ';', '%', ':', '?', '*', '(', ')', '!', '@', '/', '*', '-', '+', "'", '[', ']'],
    'ф': ['ф', '№', ';', '%', ':', '?', '*', '(', ')', '!', '@', '/', '*', '-', '+', "'", '[', ']'],
    'х': ['х', '№', ';', '%', ':', '?', '*', '(', ')', '!', '@', '/', '*', '-', '+', "'", '[', ']'],
    'ц': ['ц', '№', ';', '%', ':', '?', '*', '(', ')', '!', '@', '/', '*', '-', '+', "'", '[', ']'],
    'ч': ['ч', '№', ';', '%', ':', '?', '*', '(', ')', '!', '@', '/', '*', '-', '+', "'", '[', ']'],
    'ш': ['ш', '№', ';', '%', ':', '?', '*', '(', ')', '!', '@', '/', '*',]
}
def normalize(text):
    """Функция нормализации текста: убирает пробелы и приводит к нижнему регистру"""
    return text.replace(" ", "").lower()


def check_duplicate_name(username):
    """Проверка на одинаковые имена с учётом замены символов"""
    comments = read_comments()
    for comment in comments:
        _, stored_username, _, _ = comment.strip().split('|')
        # Проверяем как нормализованные версии, так и с учётом замены символов
        normalized_username = normalize(username)
        normalized_stored_username = normalize(stored_username)
        if normalized_username == normalized_stored_username:
            return True
    return False

def remove_repeated_letters(text):
    return re.sub(r'(.)\1+', r'\1', text)


def generate_permutations(text):
    """Создаёт всевозможные перестановки частей текста"""
    words = text.split()
    all_permutations = set()
    for i in range(1, len(words) + 1):
        for perm in permutations(words, i):
            all_permutations.add(''.join(perm))
    return all_permutations

def replace_chars(word, replacements):
    """Заменяет символы на возможные альтернативы"""
    pattern = ''.join([f"[{''.join(re.escape(c) for c in replacements.get(char, char))}]" for char in word])
    return pattern

def check_profanity(comment, banned_words, replacements):
    """Проверяет комментарий на запрещённые слова с учётом повторяющихся букв и разбивки"""
    normalized_comment = remove_repeated_letters(comment)
    variations = generate_permutations(normalized_comment)
    variations.add(normalized_comment)  # Добавляем исходный текст
    
    for variation in variations:
        words = variation.split()
        for word in words:
            for banned_word in banned_words:
                pattern = replace_chars(banned_word, replacements)
                if re.search(pattern, word, re.IGNORECASE):
                    print(f"Мат найден: {word}")
                    return True
    
    if any(profanity.contains_profanity(variation) for variation in variations):
        return True
    
    return False

@app.route('/')
def index():
    context = {'active': 'index'}
    return render_template('index.html', **context)

@app.route('/berta-game/')
def bertagame():
    context = {'active': 'berta-game'}
    return render_template('berta-game.html', **context)

@app.route('/murder/', methods=['GET', 'POST'])
def murder():
    comments = read_comments()
    comment_count = len(comments)  # Считаем количество комментариев
    ip = request.headers.get('X-Forwarded-For', request.remote_addr).split(',')[0].strip()  # Получаем IP пользователя

    if request.method == 'POST':
        username = escape(request.form['username'].strip())
        comment = escape(request.form['comment'].strip())

        if check_ip(ip):
            flash('Вы уже оставили комментарий.', 'error')
            return redirect(url_for('murder'))

        if check_duplicate_name(username):
            flash('Пользователь с таким именем уже оставил комментарий.', 'error')
            return redirect(url_for('murder'))

        if not username:
            flash('Имя не может быть пустым.', 'error')
        elif check_profanity(username, banned_words, replacements):
            flash('Имя содержит запрещённые слова.', 'error')
        elif not comment:
            flash('Комментарий не может быть пустым.', 'error')
        elif check_profanity(comment, banned_words, replacements):
            flash('Комментарий содержит запрещённые слова.', 'error')
        else:
            # Добавляем новый комментарий
            new_comment = f"{ip}|{username}|{comment}|{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            with open(filename, 'a') as f:
                f.write(new_comment)

            flash('Комментарий успешно добавлен.', 'success')
            return redirect(url_for('murder'))

    return render_template('murder.html', comments=comments, comment_count=comment_count, user_ip=ip)

@app.route('/berta-tap/', methods=['GET', 'POST'])
def berta():
    comments = read_comments()
    comment_count = len(comments)
    ip = request.headers.get('X-Forwarded-For', request.remote_addr).split(',')[0].strip()

    if request.method == 'POST':
        username = escape(request.form['username'].strip())
        comment = escape(request.form['comment'].strip())

        if check_ip(ip):
            flash('Вы уже оставили комментарий.', 'error')
            return redirect(url_for('berta'))

        if check_duplicate_name(username):
            flash('Пользователь с таким именем уже оставил комментарий.', 'error')
            return redirect(url_for('berta'))

        if not username:
            flash('Имя не может быть пустым.', 'error')
        elif check_profanity(username, banned_words, replacements):
            flash('Имя содержит запрещённые слова.', 'error')
        elif not comment:
            flash('Комментарий не может быть пустым.', 'error')
        elif check_profanity(comment, banned_words, replacements):
            flash('Комментарий содержит запрещённые слова.', 'error')
        else:
            new_comment = f"{ip}|{username}|{comment}|{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            with open(filename, 'a') as f:
                f.write(new_comment)

            flash('Комментарий успешно добавлен.', 'success')
            return redirect(url_for('berta'))

    return render_template('bertatap.html', comments=comments, comment_count=comment_count, user_ip=ip)

@app.route('/delete_comment/<int:comment_id>', methods=['POST'])
def delete_comment(comment_id):
    if not os.path.exists(filename):
        flash('Файл комментариев отсутствует.', 'error')
        return redirect(request.referrer or '/')

    with open(filename, 'r') as f:
        comments = f.readlines()

    if comment_id < 0 or comment_id >= len(comments):
        flash('Комментарий не найден.', 'error')
        return redirect(request.referrer or '/')

    ip = request.headers.get('X-Real-IP') or \
         request.headers.get('X-Forwarded-For', '').split(',')[0].strip() or \
         request.remote_addr

    stored_ip, _, _, _ = comments[comment_id].strip().split('|')

    if stored_ip != ip:
        flash('Вы не можете удалять чужие комментарии.', 'error')
        return redirect(request.referrer or '/')

    del comments[comment_id]

    with open(filename, 'w') as f:
        f.writelines(comments)

    flash('Комментарий успешно удалён.', 'success')
    return redirect(request.referrer or '/')

@app.route('/edit_comment/<int:comment_id>', methods=['POST'])
def edit_comment(comment_id):
    if not os.path.exists(filename):
        flash('Файл комментариев отсутствует.', 'error')
        return redirect(request.referrer or '/')

    with open(filename, 'r') as f:
        comments = f.readlines()

    if comment_id < 0 or comment_id >= len(comments):
        flash('Комментарий не найден.', 'error')
        return redirect(request.referrer or '/')

    ip = request.headers.get('X-Real-IP') or \
         request.headers.get('X-Forwarded-For', '').split(',')[0].strip() or \
         request.remote_addr

    stored_ip, _, _, _ = comments[comment_id].strip().split('|')

    if stored_ip != ip:
        flash('Вы не можете редактировать чужие комментарии.', 'error')
        return redirect(request.referrer or '/')

    new_comment = escape(request.form['comment'].strip())

    if not new_comment:
        flash('Комментарий не может быть пустым.', 'error')
        return redirect(request.referrer or '/')

    if check_profanity(new_comment, banned_words, replacements):
        flash('Комментарий содержит запрещённые слова.', 'error')
        return redirect(request.referrer or '/')

    parts = comments[comment_id].strip().split('|')
    parts[2] = new_comment
    parts[3] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    comments[comment_id] = '|'.join(parts) + '\n'

    with open(filename, 'w') as f:
        f.writelines(comments)

    flash('Комментарий успешно обновлён.', 'success')
    return redirect(request.referrer or '/')

if __name__ == '__main__':
    app.run(debug=True)