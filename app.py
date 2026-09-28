from flask import Flask, render_template, request, redirect, url_for,session
import sqlite3
import os
app=Flask(__name__)
app.secret_key =os.environ.get("FLASK_SECRET_KEY")or os.urandom(32)
conn = sqlite3.connect("employees.db")
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS employees(
emp_id TEXT PRIMARY KEY,
emp_name TEXT,
department TEXT,
salary INTEGER
        )
""")
conn.commit()
conn.close()
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if username == "admin" and password == "admin123":
            session["logged_in"] = True
            return redirect(url_for("dashboard"))
        else:
            return "Invalid Username or Password"

    return render_template("login.html")
@app.route("/dashboard")
def dashboard():
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    return render_template("dashboard.html")
@app.route("/add_employee", methods=["GET", "POST"])
def add_employee():
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    if request.method == "POST":
        emp_id = request.form["emp_id"]
        emp_name = request.form["emp_name"]
        department = request.form["department"]
        salary = request.form["salary"]

        conn = sqlite3.connect("employees.db")
        cursor = conn.cursor()
        cursor.execute(
            "SELECT 1 FROM employees WHERE emp_id = ?", (emp_id,)
        )
        if cursor.fetchone():
            conn.close()
            return "This Employee ID already exists. Go back and use another ID.", 409

        cursor.execute(
    "INSERT INTO employees VALUES (?, ?, ?, ?)",
    (emp_id, emp_name, department, salary)
)
        conn.commit()
        conn.close()
        return redirect(url_for("dashboard"))
    return render_template("add_employee.html")
@app.route("/view_employees")
def view_employees():
    if not session.get("logged_in"):
         return redirect(url_for("login"))
    conn = sqlite3.connect("employees.db")
    cursor = conn.cursor()
    cursor.execute("SELECT emp_id, emp_name, department, salary FROM employees")
    employees = cursor.fetchall()
    conn.close()
    return render_template("view_employees.html", employees=employees)
@app.route("/update_employee", methods=["GET", "POST"])
def update_employee():
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    if request.method == "POST":
        emp_id = request.form["emp_id"]
        emp_name = request.form["emp_name"]
        department = request.form["department"]
        salary = request.form["salary"]

        conn = sqlite3.connect("employees.db")
        cursor = conn.cursor()
        cursor.execute(
            """UPDATE employees
               SET emp_name = ?, department = ?, salary = ?
               WHERE emp_id = ?""",
            (emp_name, department, salary, emp_id)
        )
        updated = cursor.rowcount
        conn.commit()
        conn.close()

        if updated == 0:
            return "Employee ID not found. Go back and check the ID."
        return redirect(url_for("view_employees"))

    return render_template("update_employee.html")
@app.route("/delete_employee", methods=["GET", "POST"])
def delete_employee():
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    if request.method == "POST":
        emp_id = request.form["emp_id"]

        conn = sqlite3.connect("employees.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM employees WHERE emp_id = ?", (emp_id,))
        deleted = cursor.rowcount
        conn.commit()
        conn.close()

        if deleted == 0:
            return "Employee ID not found. Go back and check the ID."
        return redirect(url_for("view_employees"))

    return render_template("delete_employee.html")
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

if __name__=="__main__":
    app.run(debug=True)

