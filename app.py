from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

app = Flask(__name__)
app.secret_key = 'india'

# Use PostgreSQL (Render connection string)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://hr_erp_db_8xas_user:21KI8UbPkKhjHzbRniqlegAlF37pU6JH@dpg-d3dug9umcj7s73cu4s10-a/hr_erp_db_8xas"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ---------------------- ROUTES ----------------------

@app.route('/')
def welcome():
    return render_template('home.html')

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
    
    sql = text('INSERT INTO registration (empid, empname, email, department, phoneno) VALUES (:empid, :empname, :email, :department, :phoneno)')
    db.session.execute(sql, {
        'empid': emp_id,
        'empname': name,
        'email': email,
        'department': department,
        'phoneno': phone
    })
    db.session.commit()

    return render_template('add_emp_success.html')

@app.route('/show_emp', methods=['GET'])
def show_emp():
    sql = text('SELECT empid, empname, department, email FROM registration')
    emp_list = db.session.execute(sql).fetchall()
    return render_template("show_emp.html", record=emp_list)

@app.route('/emp_profile')
def emp_profile():
    emp_id = request.args.get('eid')
    sql = text('SELECT * FROM registration WHERE empid = :empid')
    emp_list = db.session.execute(sql, {'empid': emp_id}).fetchall()
    return render_template("emp_profile.html", li=emp_list)

@app.route('/update', methods=['POST'])
def update():
    emp_id = request.form['emp_id']
    name = request.form['name']
    email = request.form['email']
    department = request.form['department']
    phone = request.form['phone']

    sql = text('UPDATE registration SET empname = :empname, email = :email, department = :department, phoneno = :phoneno WHERE empid = :empid')
    db.session.execute(sql, {
        'empname': name,
        'email': email,
        'department': department,
        'phoneno': phone,
        'empid': emp_id
    })
    db.session.commit()

    return render_template('update.html')

@app.route('/delete')
def delete():
    emp_id = request.args.get('id')
    sql = text('DELETE FROM registration WHERE empid = :empid')
    db.session.execute(sql, {'empid': emp_id})
    db.session.commit()
    return render_template("delete.html")

@app.route('/search')
def search():
    return render_template('search_emp.html')

@app.route('/search_list', methods=['POST'])
def search_list():
    name = request.form['emp_n']
    sql = text("SELECT * FROM registration WHERE empname ILIKE :empname")
    emp_list = db.session.execute(sql, {'empname': name + '%'}).fetchall()
    return render_template('seacher_emp_list.html', record=emp_list)

# ---------------------- MAIN ----------------------
if __name__ == '__main__':
    app.run(debug=True)
