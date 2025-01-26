from flask import Flask, request, render_template, redirect, flash, url_for
import os
from datetime import datetime
from html import escape
import re

def utility_processor():
    return dict(enumerate=enumerate)

# Уникальные матерные слова
bad_words = [
"ебал", "хохол", "fuck", "shit", "bitch", "asshole", "bastard", "dick", "pussy", "cock", 
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
    "дрислоподрыв", "пукловест", "трахорезка", "залупонос", "пердолюк", "очкозавод", 
    "обосранство", "жиропылесос", "трахофеер", "пуклопуть", "залупокосарь", "пердозвукарь", "ебать", "ебанный", "ебаный", "тупой", "шлюха", "проститука", "гандон"
]

app = Flask(__name__, static_folder='static')
app.secret_key = 'supersecretkey123456'
filename = 'comments.txt'
additional_profanity = [
    "пенис", "член", "вагина", "писька", "сиськи", "сосок", "клитор", "мастурбация", "пипи", 
    "сосать", "членосос", "фалос", "пикса", "долбежка", "членяка", "подрочить", "членушка", 
    "пере*ать", "сосатель", "членососатель", "жопа", "жопошник", "п*ца", "петух", "кукольник", 
    "стр**чить", "вульва", "трахать", "пор*а", "дебил", "трахаться", "п*диш"
]
# Объединяем списки
bad_words_combined = bad_words + additional_profanity

# Генерация шаблонов регулярных выражений
profanity_patterns = [r'\b' + re.escape(word) + r'\b' for word in bad_words_combined]

# Проверка на наличие запрещенных слов
def contains_profanity(text):
    # Убираем лишние символы
    text = re.sub(r'[^a-zA-Zа-яА-Я0-9ёЁ\s]+', '', text)
    for pattern in profanity_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            return True
    return False

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
@app.route('/')
def index():
    context = {'active': 'index'}
    return render_template('index.html', **context)

@app.route('/murder/', methods=['GET', 'POST'])
def murder():
    # Чтение комментариев
    comments = read_comments()
    comment_count = len(comments)  # Считаем количество комментариев
    ip = request.headers.get('X-Forwarded-For', request.remote_addr).split(',')[0].strip()  # Получаем IP пользователя

    if request.method == 'POST':
        username = escape(request.form['username'].strip())
        comment = escape(request.form['comment'].strip())

        # Проверка, был ли уже комментарий от этого IP
        if check_ip(ip):
            flash('Вы уже оставили комментарий.', 'error')
            return redirect(url_for('murder'))
         # Проверка на одинаковые имена
        if check_duplicate_name(username):
            flash('Пользователь с таким именем уже оставил комментарий.', 'error')
            return redirect(url_for('murder'))
        
        # Проверка на пустое имя и комментарий
        if not username:
            flash('Имя не может быть пустым.', 'error')
        elif contains_profanity(username):
            flash('Имя содержит запрещенные слова.', 'error')
        elif not comment:
            flash('Комментарий не может быть пустым.', 'error')
        elif contains_profanity(comment):
            flash('Комментарий содержит запрещенные слова.', 'error')
        else:
            # Добавляем новый комментарий
            new_comment = f"{ip}|{username}|{comment}|{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            with open(filename, 'a') as f:
                f.write(new_comment)

            flash('Комментарий успешно добавлен.', 'success')
            return redirect(url_for('murder'))

    # Отдаем IP для проверки в шаблоне
    return render_template('murder.html', comments=comments, comment_count=comment_count, user_ip=ip)


@app.route('/berta-tap/', methods=['GET', 'POST'])
def berta():
    # Чтение комментариев
    comments = read_comments()
    comment_count = len(comments)
    ip = request.headers.get('X-Forwarded-For', request.remote_addr).split(',')[0].strip()

    if request.method == 'POST':
        username = escape(request.form['username'].strip())
        comment = escape(request.form['comment'].strip())

        if check_ip(ip):
            flash('Вы уже оставили комментарий.', 'error')
            return redirect(url_for('berta'))
         # Проверка на одинаковые имена
        if check_duplicate_name(username):
            flash('Пользователь с таким именем уже оставил комментарий.', 'error')
            return redirect(url_for('berta'))
        if not username:
            flash('Имя не может быть пустым.', 'error')
        elif contains_profanity(username):
            flash('Имя содержит запрещенные слова.', 'error')
        elif not comment:
            flash('Комментарий не может быть пустым.', 'error')
        elif contains_profanity(comment):
            flash('Комментарий содержит запрещенные слова.', 'error')
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

    # Получаем IP пользователя
    ip = request.headers.get('X-Real-IP') or \
         request.headers.get('X-Forwarded-For', '').split(',')[0].strip() or \
         request.remote_addr

    # Проверяем сохраненный IP в комментарии
    stored_ip, _, _, _ = comments[comment_id].strip().split('|')

    if stored_ip != ip:
        flash('Вы не можете удалять чужие комментарии.', 'error')
        return redirect(request.referrer or '/')

    del comments[comment_id]

    with open(filename, 'w') as f:
        f.writelines(comments)

    flash('Комментарий успешно удален.', 'success')
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

    # Получаем IP пользователя
    ip = request.headers.get('X-Real-IP') or \
         request.headers.get('X-Forwarded-For', '').split(',')[0].strip() or \
         request.remote_addr

    # Проверяем сохранённый IP в комментарии
    stored_ip, _, _, _ = comments[comment_id].strip().split('|')

    if stored_ip != ip:
        flash('Вы не можете редактировать чужие комментарии.', 'error')
        return redirect(request.referrer or '/')

    new_comment = escape(request.form['comment'].strip())

    if not new_comment:
        flash('Комментарий не может быть пустым.', 'error')
        return redirect(request.referrer or '/')

    if contains_profanity(new_comment):
        flash('Комментарий содержит запрещённые слова.', 'error')
        return redirect(request.referrer or '/')

    # Обновляем комментарий
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