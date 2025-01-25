from flask import Flask, request, render_template, redirect, flash, url_for
import os
from datetime import datetime
from html import escape
import re

def utility_processor():
    return dict(enumerate=enumerate)

# Исходные матерные слова
bad_words = ["fuck"]
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

@app.route('/')
def index():
    context = {'active': 'index'}
    return render_template('index.html', **context)

@app.route('/murder/', methods=['GET', 'POST'])
def murder():
    # Чтение комментариев
    comments = read_comments()
    comment_count = len(comments)  # Считаем количество комментариев
    if request.method == 'POST':
        username = escape(request.form['username'].strip())
        comment = escape(request.form['comment'].strip())
        ip = request.remote_addr  # Получаем IP пользователя

        # Проверка, был ли уже комментарий от этого IP
        if check_ip(ip):
            flash('Вы уже оставили комментарий.', 'error')
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

            # Перенаправляем на тот же маршрут, чтобы избежать повторной отправки формы
            return redirect(url_for('murder'))

    return render_template('murder.html', comments=comments, comment_count=comment_count)


@app.route('/berta-tap/', methods=['GET', 'POST'])
def berta():
    # Чтение комментариев
    comments = read_comments()
    comment_count = len(comments)  # Считаем количество комментариев


    if request.method == 'POST':
        username = escape(request.form['username'].strip())
        comment = escape(request.form['comment'].strip())
        ip = request.remote_addr  # Получаем IP пользователя

        # Проверка, был ли уже комментарий от этого IP
        if check_ip(ip):
            flash('Вы уже оставили комментарий.', 'error')
            return redirect(url_for('berta'))

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

            # Логируем комментарий в консоль
            print(f"New comment from {ip}: {username} - {comment} at {datetime.now()}")

            # Перенаправляем на тот же маршрут, чтобы избежать повторной отправки формы
            return redirect(url_for('berta'))

    return render_template('bertatap.html', comments=comments, comment_count=comment_count)

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

    stored_ip, _, _, _ = comments[comment_id].strip().split('|')

    if stored_ip != request.remote_addr:
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

    stored_ip, _, _, _ = comments[comment_id].strip().split('|')

    if stored_ip != request.remote_addr:
        flash('Вы не можете редактировать чужие комментарии.', 'error')
        return redirect(request.referrer or '/')

    new_comment = escape(request.form['comment'].strip())

    if not new_comment:
        flash('Комментарий не может быть пустым.', 'error')
        return redirect(request.referrer or '/')

    if contains_profanity(new_comment):
        flash('Комментарий содержит запрещенные слова.', 'error')
        return redirect(request.referrer or '/')

    parts = comments[comment_id].strip().split('|')
    parts[2] = new_comment
    parts[3] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    comments[comment_id] = '|'.join(parts) + '\n'

    with open(filename, 'w') as f:
        f.writelines(comments)

    flash('Комментарий успешно обновлен.', 'success')
    return redirect(request.referrer or '/')

if __name__ == '__main__':
    app.run(debug=True)
