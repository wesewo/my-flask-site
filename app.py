from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# --- Создание базы данных (если её нет) ---
def init_db():
    conn = sqlite3.connect('messages.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            message TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()


# --- Главная страница ---
@app.route('/')
def home():
    return render_template('index.html')


# --- Страница с формой ---
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        message = request.form['message']

        conn = sqlite3.connect('messages.db')
        c = conn.cursor()
        c.execute("INSERT INTO messages (name, message) VALUES (?, ?)", (name, message))
        conn.commit()
        conn.close()

        return redirect('/')  # После отправки — на главную
    return render_template('contact.html')


# --- Просмотр всех сообщений ---
@app.route('/messages')
def messages():
    conn = sqlite3.connect('messages.db')
    c = conn.cursor()
    c.execute("SELECT name, message FROM messages ORDER BY id DESC")
    data = c.fetchall()
    conn.close()
    return render_template('messages.html', messages=data)


if __name__ == "__main__":
    app.run(debug=True)
