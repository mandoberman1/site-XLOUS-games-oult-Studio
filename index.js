const express = require('express')
const fs = require('fs');
const ejs = require('ejs');
const { emitWarning } = require('process');
const sqlite3 = require('sqlite3').verbose();
const db = new sqlite3.Database('./mybase.db'); // создаст файл, если нет

// создаём таблицу, если не существует
db.run(`CREATE TABLE IF NOT EXISTS comments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    comment TEXT,
    ip TEXT
)`);

const app = express()

app.set('view engine', 'ejs')
app.set('trust proxy', true); // ОБЯЗАТЕЛЬНО, если есть прокси (например, Nginx)
app.use(express.urlencoded({extended: false}))
app.use(express.static('static'))

const base = fs.readFileSync('./views/base.ejs', 'utf8');
const routes = {
    'murder': {view: 'murder', title: 'Murder Time'},
    'bertatap': {view: 'bertatap', title: 'Bezhik-Tap'},
}

app.get('/', (req,res)=>{
    res.render('index')
})

app.get('/favicon.ico', (req, res) => res.status(204).end());
let url
let flash

app.get('/:url', (req, res) =>{
    url = req.params.url
    let title = routes[url]?.title
    let body =fs.readFileSync(`views/${url}.ejs`, 'utf-8')
    let base = fs.readFileSync(`views/base.ejs`, 'utf-8')
    let ip = req.ip
    console.log(ip);
    
    db.all('SELECT * FROM comments', (err,rows) =>{
        console.log(rows);
        let length = rows.length
        if(flash =''){
            flash = 'Нет'
        }
        const html = ejs.render(base, {
            title: title,   // Передаём заголовок в layout
            body: body,     // Вставляем отрендеренный шаблон внутрь layout
            comments: rows,
            length: length,
            flash: flash
        });
        res.send(html)
    })
    
})

app.post('/add', (req, res) =>{
    let ip = req.ip
    let { username, comment } = req.body;
    console.log(username, comment, ip);
    db.run('INSERT INTO comments (username, comment, ip) VALUES (?, ?, ?)', [username, comment, ip], () =>{res.redirect(url)})
    flash = "Добавлен комментарий"
    
})

const PORT = 3000
app.listen(PORT, () =>{
    console.log(`Сервер запущен: http://localhost:${PORT}`);
    
})