from flask import Flask, render_template, request, redirect, url_for, abort
import mysql.connector

app = Flask(__name__)


db_config = {
    'user': '',
    'password': '',
    'host': '',
    'database': ''
}


@app.route('/hello')
def hello():
    return "Hello, World!"

def get_db_connection():
    return mysql.connector.connect(**db_config)

@app.route('/')
def index():
    return redirect(url_for('user_list'))

@app.route('/user_list')
def user_list():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, email, role FROM users")
    users = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('user_list.html', users=users)


@app.route('/new_user', methods=['GET', 'POST'])
def new_user():
    if request.method == 'POST':
        user_id = request.form['id']
        name = request.form['name']
        email = request.form['email']
        role = request.form['role']
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (id, name, email, role) VALUES (%s, %s, %s, %s)", (user_id, name, email, role))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('user_list'))
    return render_template('user_entry_screen.html')


@app.route('/users/<id>')
def get_user(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, email, role FROM users WHERE id = %s", (id,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    if user:
        return render_template('user_detail.html', user=user)
    else:
        abort(404, description="User not found")
if __name__ == '__main__':
    app.run(debug=True)
