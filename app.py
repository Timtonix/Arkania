from flask import Flask, render_template, request, redirect, make_response
import subprocess
import hashlib
import sqlite3

app = Flask(__name__)
app.secret_key = "886f8b70484617eb26264d2b9c95574b20ccbe864571c22d1a993ef8ed492a383afde51fdaf18ba79f899581f0b730d9"
con = sqlite3.connect('./database.db', check_same_thread=False)
cur = con.cursor()

# cur.execute('''CREATE TABLE user (id INTEGER PRIMARY KEY, username text, adresse_email text, password text, id_cookie text, permission text)''') #création de la table pour les utilisateur.
# cur.execute('''INSERT INTO user(username, adresse_email, password, permission) VALUES ("matbe", "degueurce.mathieu@gmail.com", "e9cac7f23c0ff27bb3a4e6e7a4662c01", "d259a3dfbd71ec6c5c118abfee72de33")''')
con.commit()
print(cur.execute('''SELECT * FROM user''').fetchall())


def hash_perso(passwordtohash):
    passww = passwordtohash.encode()
    passw2 = hashlib.md5(passww).hexdigest()
    passww2 = passw2.encode()
    passw3 = hashlib.sha256(passww2).hexdigest()
    passww3 = passw3.encode()
    passw4 = hashlib.sha512(passww3).hexdigest()
    passww4 = passw4.encode()
    passwfinal = hashlib.md5(passww4).hexdigest()
    return passwfinal


# d259a3dfbd71ec6c5c118abfee72de33 = permission admin


@app.route('/')
def home():  # put application's code here
    if request.cookies.get('login') == "True":
        return render_template("index.html")
    else:
        return render_template("login.html")


@app.route('/login', methods=['POST'])
def do_admin_login():
    if request.method == 'POST':
        user = request.form['nm']
        passw = request.form['pw']
        if passw == "" or user == "":
            return "Merci de remplir tout les champs"

        password = hash_perso(passw)

        patate = cur.execute("""SELECT password FROM user WHERE username=?""", [user])
        if str(patate.fetchall()) == password:
            print("Error!")
        else:
            print(patate.fetchall())
            print(password)
            print('Error')
        perm_allowed = cur.execute("""SELECT permission FROM user WHERE username=?""", [user]).fetchone()
        perm_allowed1 = str(perm_allowed).replace("[", '')
        perm_allowed2 = perm_allowed1.replace("(", '')
        perm_allowed3 = perm_allowed2.replace(")", '')
        perm_allowed4 = perm_allowed3.replace(")", '')
        perm_allowed5 = perm_allowed4.replace("'", '')
        perm_allowed6 = perm_allowed5.replace(",", '')
        perm_allowed = perm_allowed6

        resp = make_response(redirect("/"))
        resp.set_cookie("username", user)
        resp.set_cookie("login", "True")
        resp.set_cookie("permission", f"{perm_allowed}")
        return resp
    else:
        return "ERROR"


@app.route("/logout")
def logout():
    resp = make_response(redirect("/"))
    resp.delete_cookie("login")
    resp.delete_cookie("permission")
    resp.delete_cookie("username")
    return resp


@app.route("/admin/add_user")
def add_user_page():
    if request.cookies.get("login") != "True":
        return redirect("/")

    return render_template("admin/adduser.html")


@app.route("/admin/add_user_exec", methods=['POST'])
def add_user_exec():
    if request.cookies.get("login") == "True":
        if request.method == 'POST':
            user = request.form['nm']
            mail = request.form['em']
            passw = request.form['pw']
            permi = request.form['pm']

            passw = hash_perso(passw)
            # ici création de l'utilisateur avec l'input user
            cur.execute(f'''INSERT INTO user(username, adresse_email, password, permission) VALUES ("{user}", "{mail}", "{passw}", "d259a3dfbd71ec6c5c118abfee72de33")''')
            con.commit()
            return "C'est bon"
        else:
            return "C'est pas bon"

    elif request.cookies.get("login") != "True":
        return redirect("/")


@app.route("/admin/show_user")
def show_user():
    if request.cookies.get("login") == "True":
        for row in cur.execute('''SELECT * FROM user ORDER BY id'''):
            print(row)

        return render_template("admin/show_user.html", cur=cur)

if __name__ == '__main__':
    app.run()
