from flask import Flask,render_template,request,redirect,url_for
from flask_mysqldb import MySQL

app = Flask(__name__)

# MySQL Config
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'trisha'
app.config['MYSQL_DB'] = 'CrudFlask'

mysql = MySQL(app)

@app.route('/',methods=["GET","POST"])
def todo():
    
    if request.method == "POST":
        task=request.form['task']
        print(task)
        cur=mysql.connection.cursor()
        cur.execute("Insert into tasks (task) values (%s)",(task,))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for("todo"))
    
    if request.method == "GET":
        cur=mysql.connection.cursor()
        cur.execute("select * from tasks")
        data=cur.fetchall()
        mysql.connection.commit()
        cur.close()
        tasks = [{"id": d[0], "task": d[1], "done": d[2]} for d in data]
        return render_template("home.html", tasks=tasks)

@app.route("/delete", methods=["POST"])
def deleteTask():
    task_id = request.form['id']  
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM tasks WHERE id = %s", (task_id,))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for("todo"))

@app.route("/taskDone",methods=["POST"])
def taskDone():
    id=request.form['id']
    cur = mysql.connection.cursor()
    cur.execute("UPDATE tasks SET done = 1 WHERE id = %s", (id,))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for("todo"))

if __name__ == "__main__":
    app.run(debug=True)
