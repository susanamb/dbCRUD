from flask import Flask, render_template,request
import sqlite3



conn = sqlite3.connect('users.db')

c = conn.cursor()
#c.execute("""
#    CREATE TABLE user(
#        name text,
#        last_name text,
#        email text,
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
    return render_template("secon.html")

@app.route("/ver")
def ver():
    conn = sqlite3.connect("users.db")
    conn.row_factory = sqlite3.Row  
    cur = conn.cursor()
    cur.execute("SELECT * FROM user")
   
    rows = cur.fetchall(); 

    return render_template("ver.html", rows = rows)


@app.route('/save', methods = ['POST'])
def save():
    if request.method == 'POST':
        try:
            name = request.form['name']
            last_name = request.form['ln']
            email = request.form['email']
            age = request.form['age']
            print('first step')
            with sqlite3.connect("users.db") as conn:
                c = conn.cursor()
                c.execute("INSERT INTO user (name,last_name,email,age) VALUES(?,?,?,?)",(name,last_name,email,age))
                conn.commit()
        except:
            conn.rollback()
            print('valiendo')
        finally:
            conn.close()
    return "<h1>inserted</h1>"

@app.route('/deleted/<mail>', methods = ['POST'])
def deleted(mail):
        try:
            print(mail)
            with sqlite3.connect("users.db") as conn:
                c = conn.cursor()
                c.execute(f"DELETE FROM user WHERE email = {mail}")
                conn.commit()
                print("deletado")
        except:
            conn.rollback()      
            print('valiendo')
        finally:
            conn.close()

        return """<h1>Deleted</h1>
    <a href='/' style='width: 100%;' class='btn btn-primary btn-lg btn-block' role='button'>Regresar</a>
    """


if __name__ == "__main__":
    print("running....")
    #app.run()
    app.run(debug = True)

