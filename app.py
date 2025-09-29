from flask import Flask, render_template,request
from flask_mysqldb import MySQL


app = Flask(__name__)

app.secret_key ='india'
app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']='uday'
app.config['MYSQL_DB']='hr_erp_db'

con = MySQL(app)

@app.route('/')
def welcome():
    return render_template('home.html')

@app.route('/home',methods=["GET","POST"])
def home():

    username = request.form['username']
    password = request.form['password']

    if username=="uday" and password=="123":
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
    
    cur = con.connection.cursor()

    cur.execute(
        'INSERT INTO registration(empid, empname, email, department, phoneno) VALUES (%s, %s, %s, %s, %s)',
        (emp_id, name, email, department, phone)
    )

    con.connection.commit()
    
    cur.close()

    return render_template('add_emp_success.html')

@app.route('/show_emp',methods=['GET'])
def show_emp():

    cur = con.connection.cursor()

    cur.execute(
        'select empid, empname, department, email from registration'
    )
    
    emp_list = cur.fetchall()
    return render_template("show_emp.html",record=emp_list)


@app.route('/emp_profile')
def emp_profile():
    id=request.args.get('eid')

    cur = con.connection.cursor()

    cur.execute(
        'select * from registration where empid= '+id
    )
    emp_list = cur.fetchall()
    return render_template("emp_profile.html",li=emp_list)

@app.route('/update',methods=['GET','POST'])
def update():
    emp_id = request.form['emp_id']
    name = request.form['name']
    email = request.form['email']
    department = request.form['department']
    phone = request.form['phone']

    cur = con.connection.cursor()

    cur.execute(
        'update registration set empname=%s, email=%s, department=%s, phoneno=%s where empid=%s',(name,email,department,phone,emp_id)
    )

    con.connection.commit()
    
    cur.close()

    return render_template('update.html')


@app.route('/delete')
def delete():

    emp_id=request.args.get('id')

    cur = con.connection.cursor()

    cur.execute(
        'delete from registration where empid='+emp_id
    )

    con.connection.commit()
    
    cur.close()

    return render_template("delete.html")

@app.route('/search')
def search():

    return render_template('search_emp.html')

@app.route('/search_list',methods=['POST'])
def search_list():

    name=request.form['emp_n']

    cur = con.connection.cursor()

    cur.execute(
        "select * from registration where empname like '"+name+"%'"  )
    emp_list = cur.fetchall()
    
    cur.close()
  
    return render_template('seacher_emp_list.html',record=emp_list)


if __name__ == '__main__':
    app.run(debug=True)


