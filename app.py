from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)


def init_db():
    with sqlite3.connect('expenses.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS expenses
                          (id INTEGER PRIMARY KEY, date TEXT, category TEXT, amount REAL, description TEXT)''')
        conn.commit()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/add', methods=['GET', 'POST'])
def add_expense():
    if request.method == 'POST':
        date = request.form['date']
        category = request.form['category']
        amount = request.form['amount']
        description = request.form['description']

        with sqlite3.connect('expenses.db') as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO expenses (date, category, amount, description) VALUES (?, ?, ?, ?)",
                           (date, category, amount, description))
            conn.commit()
        return redirect(url_for('view_expenses'))

    return render_template('add_expense.html')


@app.route('/view')
def view_expenses():
    with sqlite3.connect('expenses.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM expenses")
        expenses = cursor.fetchall()
    return render_template('view_expenses.html', expenses=expenses)


@app.route('/delete/<int:id>')
def delete_expense(id):
    with sqlite3.connect('expenses.db') as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM expenses WHERE id=?", (id,))
        conn.commit()
    return redirect(url_for('view_expenses'))


if __name__ == '__main__':
    init_db()
    app.run(debug=True)
