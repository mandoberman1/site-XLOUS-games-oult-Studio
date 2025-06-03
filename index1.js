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
    cookie: { secure: false }
}));

const COMMENTS_FILE = './comments.txt';
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
const transporter = nodemailer.createTransport({
    service: 'gmail',
    auth: {
        user: process.env.EMAIL,
        pass: process.env.EMAIL_PASS,
    }
});
let url, flash;

app.post('/register', async (req, res) => {
    const { email, username, Password, "Con-Password": confirmPassword } = req.body;
    if (!email || !username || !Password || Password !== confirmPassword) {
        flash = "Ошибка: заполните все поля корректно";
        return res.redirect(url);
    }

    const users = readUsers();
    if (users.find(u => u.email === email)) {
        flash = "Email уже зарегистрирован";
        return res.redirect(url);
    }
    if (users.find(u => u.username === username)) {
        flash = "Имя уже занято";
        return res.redirect(url);
    }

    const hashedPassword = await bcrypt.hash(Password, 10);
    const verifyToken = uuidv4();

    const newUser = {
        email,
        username,
        password: hashedPassword,
        verified: false,
        token: verifyToken
    };

    users.push(newUser);
    saveUsers(users);

    const link = `https://${req.get('host')}/verify?token=${verifyToken}`;
await transporter.sendMail({
    from: `"Railway Auth" <${process.env.EMAIL}>`,
    to: email,
    subject: "Подтверждение регистрации",
    html: `
        <p>Привет! Подтверди регистрацию, кликнув по ссылке ниже:</p>
        <p><a href="${link}">${link}</a></p>
        <p>Если ты не регистрировался — просто проигнорируй это письмо.</p>
    `
});


    flash = "Письмо отправлено. Проверьте почту.";
    res.redirect(url);
});

app.get('/verify', (req, res) => {
    const { token } = req.query;
    const users = readUsers();
    const user = users.find(u => u.token === token);
    if (!user) return res.send('Неверная или устаревшая ссылка');
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
        console.error('Ошибка чтения комментариев:', err);
        return [];
    }
}
function saveComment(comment) {
    const comments = readComments();
    comments.push(comment);
    fs.writeFileSync(COMMENTS_FILE, JSON.stringify(comments, null, 2), 'utf8');
}

app.get('/', (req, res) => {
    url = 'index';
    const comments = readComments();
    res.render('index', {
        comments,
        length: comments.length,
        flash: flash || 'нет',
        user: req.session.user
    });
    flash = '';
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
    req.session.user = { email: user.email, username: user.username };
    flash = `Вы вошли как ${user.username}`;
    res.redirect(url);
});

app.post('/add', (req, res) => {
    const ip = req.ip;
    const { comment } = req.body;
    if (!req.session.user || !comment) {
        flash = "Вы должны быть авторизованы и ввести комментарий";
        return res.redirect(url);
    }
    const username = req.session.user.username;
    const newComment = { username, comment, ip };
    saveComment(newComment);
    flash = "Комментарий добавлен";
    res.redirect(url);
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log(`Сервер запущен: http://localhost:${PORT}`);
});
