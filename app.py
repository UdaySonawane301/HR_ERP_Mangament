from flask import Flask, render_template, request
import psycopg2

app = Flask(__name__)
app.secret_key = 'india'

# ---------------------------
# PostgreSQL Connection
# ---------------------------
def get_connection():
    return psycopg2.connect(
        host="dpg-d3elv43uibrs73cc7830-a.singapore-postgres.render.com",   
        database="crud_dashboard_db",          # your db name
        user="crud_dashboard_db_user",
        password="myTECBRRyf6VUadvVxAmYvQTy7oqyuvM",
        port="5432"
     )

@app.route('/')
def welcome():
    return render_template('welcome.html')


@app.route('/home', methods=["GET", "POST"])
def home():
    if request.method == 'POST':
        username = request.form['username']   
        password = request.form['password']   
        flag = 0

        cur = con.connection.cursor()
        cur.execute('SELECT * FROM regi_info')
        emp_list = cur.fetchall()

        for i in emp_list:
            if i[0] == username and i[1] == password:
                flag = 1
                break
        
        if flag == 1:
            return render_template("das.html")
        else:
            return "<h2>Username And Password Is Invalid</h2>"

@app.route('/add')
def add():
    return render_template('registration.html')

@app.route('/regi_emp', methods=['GET', 'POST'])
def regi_emp():
    if request.method == 'POST':
        name = request.form['Username']
        passwo = request.form['Password']

        cur = con.connection.cursor()
        cur.execute(
            'INSERT INTO regi_info(username, pin) VALUES (%s, %s)',
            (name, passwo)
        )
        con.connection.commit()
        cur.close()

        
        return render_template('login.html')

    
    return render_template('registration.html')


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

    cur.execute(
        'INSERT INTO registration(empid, empname, email, department, phoneno) VALUES (%s, %s, %s, %s, %s)',
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
    cur.execute('select empid, empname, department, email from registration')
    emp_list = cur.fetchall()
    cur.close()
    con.close()
    return render_template("show_emp.html", record=emp_list)


@app.route('/emp_profile')
def emp_profile():
    emp_id = request.args.get('eid')
    con = get_connection()
    cur = con.cursor()
    cur.execute('select * from registration where empid=%s', (emp_id,))
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
        'update registration set empname=%s, email=%s, department=%s, phoneno=%s where empid=%s',
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
    cur.execute('delete from registration where empid=%s', (emp_id,))
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
    cur.execute("select * from registration where empname like %s", (name + '%',))
    emp_list = cur.fetchall()
    cur.close()
    con.close()
    return render_template('seacher_emp_list.html', record=emp_list)


if __name__ == '__main__':
    app.run(debug=True)








