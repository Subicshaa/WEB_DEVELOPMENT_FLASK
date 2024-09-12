
from flask import Flask, render_template, request, redirect, url_for,flash
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)
app.secret_key = 'your_secret_key' 


    
def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="employee"
        )
        return conn
    except Error as e:
        print(f"Error connecting to database: {e}")
        return None

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/user', methods=['POST'])
def user():
    email = request.form['email']
    password = request.form['password']

    if email == "admin@gmail.com" and password == "Admin@1234":
        return redirect(url_for('demo'))
    else:
        flash("Invalid user")
        return redirect(url_for('login'),message="Invalid User")
    
@app.route('/demo',methods=['GET'])
def demo():
    conn = get_db_connection()
    if conn is None:
        return render_template('Demo.html', message="Connection Failed", result=[])

    try:
        mycursor = conn.cursor()
        mycursor.execute("SELECT * FROM empl")
        result = mycursor.fetchall()
        conn.close()
        return render_template('Demo.html', message="Successfully Connected", result=result)
    except Error as e:
        print(f"Error fetching data: {e}")
        return render_template('Demo.html', message=f"Error: {e}", result=[])

@app.route('/addnew')
def addnew():
    return render_template('addnew.html')

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    email = request.form['email']
    contact = request.form['contact']

    conn = get_db_connection()
    if conn is None:
        return "Error connecting to database"

    try:
        mycursor = conn.cursor()
        mycursor.execute("INSERT INTO empl (name, email, contact) VALUES (%s, %s, %s)", (name, email, contact))
        conn.commit()
        conn.close()
        return redirect(url_for('demo'))
    except Error as e:
        conn.close()
        return f"Error: {str(e)}"

if __name__ == '__main__':
    app.run(port="5000",debug=True)
