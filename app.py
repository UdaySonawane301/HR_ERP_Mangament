from flask import Flask, render_template, request
import sqlite3  # Changed from psycopg2

app = Flask(__name__)
app.secret_key = 'india'

# ---------------------------
# SQLite Connection to local SQL file
# ---------------------------
def get_connection():
    # This file will store your database
    return sqlite3.connect("hr_erp_db.sqlite3")

# Optional: ensure rows return as dictionaries for templates
def get_dict_connection():
    con = sqlite3.connect("hr_erp_db.sqlite3")
    con.row_factory = sqlite3.Row
    return con

# ---------------------------
# Create table if not exists
# ---------------------------
con = get_connection()
cur = con.cursor()
cur.execute("""
CREATE TABLE IF NOT EXISTS registration (
    empid TEXT PRIMARY KEY,
    empname TEXT,
    email TEXT,
    department TEXT,
    phoneno TEXT
)
""")
con.commit()
cur.close()
con.close()

# ---------------------------
# Routes (same as your original)
# ---------------------------

@app.route('/')
def welcome():
    return render_template('welcome.html')


@app.route('/home', methods=["POST"])
def home():
    username = request.form['username']
    password = request.form['password']

    if username == "uday" and password == "123":
        return render_template('home.html')
    else:
        return "ERROR"


@app.route('/login')
def login():
    return render_template("login.html")


@app.route('/add_emp')
def add_emp():
    return render_template("add_emp.html")


@app.route('/save', methods=['POST'])
def save():
    emp_id = request.form['emp_id']
    name = request.form['name']
    email = request.form['email']
    department = request.form['department']
    phone = request.form['phone']

    con = get_connection()
    cur = con.cursor()
    # SQLite uses ? instead of %s
    cur.execute(
        'INSERT INTO registration(empid, empname, email, department, phoneno) VALUES (?, ?, ?, ?, ?)',
        (emp_id, name, email, department, phone)
    )
    con.commit()
    cur.close()
    con.close()

    return render_template('add_emp_success.html')


@app.route('/show_emp')
def show_emp():
    con = get_connection()
    cur = con.cursor()
    cur.execute('SELECT empid, empname, department, email FROM registration')
    emp_list = cur.fetchall()
    cur.close()
    con.close()
    return render_template("show_emp.html", record=emp_list)


@app.route('/emp_profile')
def emp_profile():
    emp_id = request.args.get('eid')
    con = get_connection()
    cur = con.cursor()
    cur.execute('SELECT * FROM registration WHERE empid=?', (emp_id,))
    emp_list = cur.fetchall()
    cur.close()
    con.close()
    return render_template("emp_profile.html", li=emp_list)


@app.route('/update', methods=['POST'])
def update():
    emp_id = request.form['emp_id']
    name = request.form['name']
    email = request.form['email']
    department = request.form['department']
    phone = request.form['phone']

    con = get_connection()
    cur = con.cursor()
    cur.execute(
        'UPDATE registration SET empname=?, email=?, department=?, phoneno=? WHERE empid=?',
        (name, email, department, phone, emp_id)
    )
    con.commit()
    cur.close()
    con.close()

    return render_template('update.html')


@app.route('/delete')
def delete():
    emp_id = request.args.get('id')
    con = get_connection()
    cur = con.cursor()
    cur.execute('DELETE FROM registration WHERE empid=?', (emp_id,))
    con.commit()
    cur.close()
    con.close()
    return render_template("delete.html")


@app.route('/search')
def search():
    return render_template('search_emp.html')


@app.route('/search_list', methods=['POST'])
def search_list():
    name = request.form['emp_n']
    con = get_connection()
    cur = con.cursor()
    cur.execute("SELECT * FROM registration WHERE empname LIKE ?", (name + '%',))
    emp_list = cur.fetchall()
    cur.close()
    con.close()
    return render_template('seacher_emp_list.html', record=emp_list)


if __name__ == '__main__':
    app.run(debug=True)

