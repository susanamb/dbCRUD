from flask import Flask, render_template,request
import sqlite3



conn = sqlite3.connect('data.db')

c = conn.cursor()
#c.execute("""
#    CREATE TABLE people(
#        name text,
#        last_name text,
#        phone text,
#        age integer
#    ) 
#""")

app = Flask(__name__)

# default route

@app.route("/")
def home():
    return render_template("index.html")
    #return "Hello! this is a FLASK server! <h1>HOLAMUNDO</h1>"


@app.route("/second")
def second():
    return render_template("secon.html", user = 0)

@app.route("/ver")
def ver():
    conn = sqlite3.connect("data.db")
    conn.row_factory = sqlite3.Row  
    cur = conn.cursor()
    cur.execute("SELECT * FROM people")
   
    rows = cur.fetchall(); 

    return render_template("ver.html", rows = rows)


@app.route('/save', methods = ['POST'])
def save():
    if request.method == 'POST':
        try:
            name = request.form['name']
            last_name = request.form['ln']
            phone = request.form['phone']
            age = request.form['age']
            with sqlite3.connect("data.db") as conn:
                c = conn.cursor()
                c.execute("INSERT INTO people (name,last_name,phone,age) VALUES(?,?,?,?)",(name,last_name,phone,age))
                conn.commit()
                task = "Insertado exitosamente"
        except:
            conn.rollback()
            task = "valiendo"
        finally:
            conn.close()
    return f"""<h1>{task}</h1>
    <a href='/' style='width: 100%;' class='btn btn-primary btn-lg btn-block' role='button'>Regresar</a>
    """

@app.route('/update/<cel_phone>/<lname>', methods = ['POST'])
def update(cel_phone,lname):
    if request.method == 'POST':
        try:
            name = request.form['name']
            last_name = request.form['ln']
            phone = request.form['phone']
            age = request.form['age']
            with sqlite3.connect("data.db") as conn:
                c = conn.cursor()
                c.execute("UPDATE people SET name =? ,last_name =? ,phone=? ,age=? WHERE phone =? and last_name =?",(name,last_name,phone,age,cel_phone,lname))
                conn.commit()
                task = "Updateado exitosamente"
        except:
            conn.rollback()
            task = "valiendo"
        finally:
            conn.close()
    return f"""<h1>{task}</h1>
    <a href='/' style='width: 100%;' class='btn btn-primary btn-lg btn-block' role='button'>Regresar</a>
    """

@app.route('/delete/<phone>', methods = ['POST'])
def delete(phone):
    if request.method == 'POST':
        try:
            print(phone)
            with sqlite3.connect("data.db") as conn:
                c = conn.cursor()
                c.execute(f"DELETE FROM people WHERE phone = {phone} ")
                conn.commit()
                task = "Eliminado exitosamente"
        except:
            conn.rollback()
            task = "valiendo"
        finally:
            conn.close()

        return f"""<h1>{task}</h1>
    <a href='/' style='width: 100%;' class='btn btn-primary btn-lg btn-block' role='button'>Regresar</a>
    """

@app.route("/edit/<phone>", methods = ['POST'])
def edit(phone):

    conn = sqlite3.connect("data.db")
    #conn.row_factory = sqlite3.Row  
    c = conn.cursor()
    c.execute(f"SELECT * FROM people WHERE phone = {phone}")
   
    row = c.fetchone(); 
    user = []
    for i in row:
        x= i
        user.append(x)

    
    return render_template("secon.html", user = user)

if __name__ == "__main__":
    print("running....")
    #app.run()
    app.run(debug = True)

