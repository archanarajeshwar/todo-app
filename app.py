from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL

app = Flask(__name__, template_folder="templates")

# Configure MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'  # Replace with your MySQL username
app.config['MYSQL_PASSWORD'] = 'Aesthetic@0610'  # Replace with your MySQL password
app.config['MYSQL_DB'] = 'todos'  # Replace with your database name

# Initialize MySQL
mysql = MySQL(app)


@app.route("/")
def index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM todos")
    todos = list(cur.fetchall())
    cur.close()
    print(todos)
    return render_template("index.html", todos=todos)


@app.route("/add", methods=["POST"])
def add():
    if request.method == "POST":
        task = request.form['todo']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO todos (task) VALUES (%s)", (task,))
        mysql.connection.commit()
        cur.close()
    return redirect(url_for("index"))


@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM todos WHERE id = %s", (id,))
    todo = cur.fetchone()
    cur.close()

    if request.method == "POST":
        task = request.form['todo']
        cur = mysql.connection.cursor()
        cur.execute("UPDATE todos SET task = %s WHERE id = %s", (task, id))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for("index"))
    else:
        return render_template("edit.html", todo=todo)


@app.route("/check/<int:id>")
def check(id):
    cur = mysql.connection.cursor()
    cur.execute("UPDATE todos SET done = NOT done WHERE id = %s", (id,))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for("index"))


@app.route("/delete/<int:id>")
def delete(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM todos WHERE id = %s", (id,))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for("index"))


if __name__ == '__main__':
    app.run(debug=True)
