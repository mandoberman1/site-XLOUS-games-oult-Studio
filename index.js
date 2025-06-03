const express = require('express');
const fs = require('fs');
const ejs = require('ejs');
const { Pool } = require('pg');

const app = express();
app.set('view engine', 'ejs');
app.set('trust proxy', true);
app.use(express.urlencoded({ extended: false }));
app.use(express.static('static'));

// Подключение к PostgreSQL
const pool = new Pool({
  connectionString: process.env.DATABASE_URL, // Railway задаёт это переменной окружения
  ssl: process.env.NODE_ENV === 'production' ? { rejectUnauthorized: false } : false,
});

// Создание таблицы, если не существует
pool.query(`
  CREATE TABLE IF NOT EXISTS comments (
    id SERIAL PRIMARY KEY,
    username TEXT,
    comment TEXT,
    ip TEXT
)`).catch(console.error);

const routes = {
  'murder': { view: 'murder', title: 'Murder Time' },
  'bertatap': { view: 'bertatap', title: 'Bezhik-Tap' },
};

app.get('/', (req, res) => {
  res.render('index');
});

app.get('/favicon.ico', (req, res) => res.status(204).end());

let url;
let flash = '';

app.get('/:url', async (req, res) => {
  url = req.params.url;
  const title = routes[url]?.title;

  try {
    const body = fs.readFileSync(`views/${url}.ejs`, 'utf-8');
    const base = fs.readFileSync(`views/base.ejs`, 'utf-8');
    const ip = req.ip;

    const result = await pool.query('SELECT * FROM comments');
    const rows = result.rows;
    const length = rows.length;

    if (!flash) flash = 'Нет';

    const html = ejs.render(base, {
      title,
      body,
      comments: rows,
      length,
      flash,
    });

    res.send(html);
  } catch (err) {
    console.error(err);
    res.status(500).send('Ошибка на сервере');
  }
});

app.post('/add', async (req, res) => {
  const ip = req.ip;
  const { username, comment } = req.body;

  try {
    await pool.query(
      'INSERT INTO comments (username, comment, ip) VALUES ($1, $2, $3)',
      [username, comment, ip]
    );
    flash = 'Добавлен комментарий';
    res.redirect(`/${url}`);
  } catch (err) {
    console.error(err);
    res.status(500).send('Ошибка при добавлении');
  }
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Сервер запущен: http://localhost:${PORT}`);
});
