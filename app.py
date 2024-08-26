from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Database setup
def init_db():
    with sqlite3.connect('noticeboard.db') as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS notices
                        (id INTEGER PRIMARY KEY AUTOINCREMENT,
                         title TEXT NOT NULL,
                         content TEXT NOT NULL,
                         date TEXT NOT NULL);''')
    conn.close()

# Home route to display notices
@app.route('/')
def index():
    conn = sqlite3.connect('noticeboard.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM notices ORDER BY id DESC')
    notices = cursor.fetchall()
    conn.close()
    return render_template('index.html', notices=notices)

# Route to post a new notice
@app.route('/post', methods=['GET', 'POST'])
def post_notice():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        date = request.form['date']
        
        conn = sqlite3.connect('noticeboard.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO notices (title, content, date) VALUES (?, ?, ?)",
                       (title, content, date))
        conn.commit()
        conn.close()
        
        return redirect(url_for('index'))
    
    return render_template('post_notice.html')

# Initialize the database
if __name__ == '__main__':
    init_db()
    app.run(debug=True)
 
