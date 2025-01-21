from flask import Flask, request, Response, render_template, url_for
import os
from datetime import datetime
from html import escape

app = Flask(__name__, static_folder='static')
filename = 'comments.txt'

@app.route('/')
def index():
    context = {'active': 'index'}
    return render_template('index.html', **context)

@app.route('/murder/', methods=['GET', 'POST'])
def murder():
    ip_address = request.remote_addr
    comments = []

    # Чтение комментариев
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            comments = f.readlines()

    # Проверка на дублирование комментариев с одного IP
    user_comment = None
    for line in comments:
        stored_ip, username, comment, created_at = line.strip().split('|')
        if stored_ip == ip_address:
            user_comment = (username, comment, created_at)
            break

    error_message = None

    if request.method == 'POST':
        username = escape(request.form['username'].strip())
        comment = escape(request.form['comment'].strip())

        # Проверка на пустое имя и комментарий
        if not username:
            error_message = 'Имя не может быть пустым.'
        if username.lower() in [
            'negr',
            'penis',
            'pizda',
            'pidor',
            'govno',
            'mudak',
            'blyad',
            'suka',
            'eblan',
            'durak',
            'idiot',
            'chmo',
            'davun',
            'gandon',
            'zhopa',
            'mraz',
            'skotina',
            'tvar',
            'zasranec',
            'merzavec',
            'podonok',
            'xyu',
            'хуй',
            'пизда',
            'пидор',
            'говноед',
            'мудак',
            'блядь',
            'сука',
            'еблан',
            'дурак',
            'идиот',
            'чмо',
            'даун',
            'гондон',
            'жопа',
            'мразь',
            'скотина',
            'тварь',
            'засранец',
            'мерзавец',
            'подонок',
        ]:
            error_message = 'Имя содержит оскорбление.'
        elif not comment:
            error_message = 'Комментарий не может быть пустым.'
        else:
            # Проверка на дублирование имени
            for line in comments:
                stored_ip, stored_username, _, _ = line.strip().split('|')
                if stored_username == username:
                    error_message = 'Имя уже используется. Пожалуйста, выберите другое имя.'
                    break

            # Если комментарий уже был оставлен с этого IP
            if user_comment:
                error_message = 'Вы уже оставили комментарий.'

        # Если ошибок нет, сохраняем комментарий
        if error_message is None:
            new_comment = f"{ip_address}|{username}|{comment}|{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            with open(filename, 'a') as f:
                f.write(new_comment)

            # Перечитываем файл с комментариями
            with open(filename, 'r') as f:
                comments = f.readlines()

            # Сбрасываем user_comment, чтобы форма была пустой
            user_comment = None

        # Отображаем страницу с новыми данными
        return render_template('murder.html', comments=comments, user_comment=None, error_message=error_message)

    # Отображаем страницу при GET запросе (или если не было ошибок при POST)
    context = {'active': 'murder'}
    return render_template('murder.html', comments=comments, user_comment=None, error_message=error_message, **context)
    

if __name__ == '__main__':
    app.run(debug=True)
