const express = require('express');
const fs = require('fs');
const ejs = require('ejs');
const app = express();
const nodemailer = require('nodemailer');
const { v4: uuidv4 } = require('uuid');
const bcrypt = require('bcrypt');
const session = require('express-session');

const USERS_FILE = './users.json';
app.set('view engine', 'ejs');
app.set('trust proxy', true);
app.use(express.urlencoded({ extended: false }));
app.use(express.static('static'));
app.use(session({
    secret: process.env.SESSION_SECRET || 'keyboard cat',
    resave: false,
    saveUninitialized: true,
    cookie: { secure: false } // В Railway можно сделать true с HTTPS
}));

const COMMENTS_FILE = './comments.txt';
const routes = {
    'murder': { view: 'murder', title: 'Murder Time' },
    'bertatap': { view: 'bertatap', title: 'Bezhik-Tap' },
};
function readUsers() {
    if (!fs.existsSync(USERS_FILE)) return [];
    try {
        const data = fs.readFileSync(USERS_FILE, 'utf8');
        return JSON.parse(data);
    } catch (err) {
        console.error('Ошибка чтения users:', err);
        return [];
    }
}

function saveUsers(users) {
    fs.writeFileSync(USERS_FILE, JSON.stringify(users, null, 2), 'utf8');
}

// Транспорт для письма — укажи свою почту (например, Gmail SMTP)
const transporter = nodemailer.createTransport({
    service: 'gmail',
    auth: {
        user: process.env.EMAIL,        // Укажи в Railway переменные
        pass: process.env.EMAIL_PASS,   // Пароль приложения Gmail
    }
});

// 📩 Обработка регистрации
app.post('/register', async (req, res) => {
    const { email, Password, "Con-Password": confirmPassword } = req.body;
    if (!email || !Password || Password !== confirmPassword) {
        flash = "Ошибка: заполните все поля корректно";
        return res.redirect(url);
    }

    const users = readUsers();
    if (users.find(u => u.email === email)) {
        flash = "Email уже зарегистрирован";
        return res.redirect(url);
    }

    const hashedPassword = await bcrypt.hash(Password, 10);
    const verifyToken = uuidv4();

    const newUser = {
        email,
        password: hashedPassword,
        verified: false,
        token: verifyToken
    };

    users.push(newUser);
    saveUsers(users);

    const link = `https://${req.headers.host}/verify?token=${verifyToken}`;
    await transporter.sendMail({
        from: `"Railway Auth" <${process.env.EMAIL}>`,
        to: email,
        subject: "Подтверждение регистрации",
        html: `<p>Привет! Подтверди регистрацию по ссылке: <a href="${link}">${link}</a></p>`
    });

    flash = "Письмо отправлено. Проверьте почту.";
    res.redirect(url);
});

// ✅ Подтверждение почты
app.get('/verify', (req, res) => {
    const { token } = req.query;
    const users = readUsers();
    const user = users.find(u => u.token === token);

    if (!user) {
        return res.send('Неверная или устаревшая ссылка');
    }

    user.verified = true;
    user.token = null;
    saveUsers(users);

    res.send('Email подтвержден! Теперь можно авторизоваться.');
});
function readComments() {
    if (!fs.existsSync(COMMENTS_FILE)) return [];
    try {
        const data = fs.readFileSync(COMMENTS_FILE, 'utf8');
        return JSON.parse(data);
    } catch (err) {
        console.error('Ошибка чтения файла комментариев:', err);
        return [];
    }
}

function saveComment(comment) {
    const comments = readComments();
    comments.push(comment);
    fs.writeFileSync(COMMENTS_FILE, JSON.stringify(comments, null, 2), 'utf8');
}

app.get('/', (req, res) => {
    res.render('index');
});

app.get('/favicon.ico', (req, res) => res.status(204).end());

let url;
let flash;

app.get('/:url', (req, res) => {
    url = req.params.url;
    const route = routes[url];

    if (!route) {
        return res.status(404).send('Страница не найдена');
    }

    const title = route.title;
    const body = fs.readFileSync(`views/${url}.ejs`, 'utf-8');
    const base = fs.readFileSync(`views/base.ejs`, 'utf-8');
    const ip = req.ip;

    console.log(ip);

    const comments = readComments();
    const html = ejs.render(base, {
        title,
        body,
        comments,
        length: comments.length,
        flash: flash || ' нет',
        user: req.session.user
    });

    flash = '';
    res.send(html);
});
app.post('/login', async (req, res) => {
    const { email, Password } = req.body;
    const users = readUsers();
    const user = users.find(u => u.email === email);

    if (!user) {
        flash = 'Пользователь не найден';
        return res.redirect(url);
    }

    if (!user.verified) {
        flash = 'Email не подтверждён';
        return res.redirect(url);
    }

    const match = await bcrypt.compare(Password, user.password);
    if (!match) {
        flash = 'Неверный пароль';
        return res.redirect(url);
    }

    req.session.user = { email: user.email };
    flash = `Вы вошли как ${user.email}`;
    res.redirect(url);
});

app.post('/add', (req, res) => {
    const ip = req.ip;
    const { username, comment } = req.body;

    if (!username || !comment) {
        flash = "Заполните все поля";
        return res.redirect(url);
    }

    const newComment = { username, comment, ip };
    saveComment(newComment);
    flash = "Добавлен комментарий";
    res.redirect(url);
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log(`Сервер запущен: http://localhost:${PORT}`);
});
