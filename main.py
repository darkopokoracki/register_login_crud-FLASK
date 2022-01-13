from flask import Flask, render_template, redirect, url_for, session, request
import mysql.connector

app = Flask(__name__)
app.config['SECRET_KEY'] = '#!afgJ76Trdscm836sHsdjns!?'

mydb = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    password = '',
    database = 'priprema'
)

@app.route('/')
@app.route('/index')
def index():
    return 'Hello World'

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template(
            'register.html'
        )

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        confirm = request.form['confirm']
        privilegija = request.form['vrsta']
        godina = request.form['godina']

        cursor = mydb.cursor(prepared = True)
        sql = "SELECT * FROM korisnik WHERE email = ?"
        value = (email, )
        cursor.execute(sql, value)

        res = cursor.fetchone()

        if res != None:
            return render_template(
                'register.html',
                email_error = 'Email je zauzet!'
            )
        
        if password != confirm:
            return render_template(
                'register.html',
                password_error = 'Lozinke se ne poklapaju!'
            )

        cursor = mydb.cursor(prepared = True)
        sql = "INSERT INTO korisnik VALUES(null,?,?,?,?,0)"
        # Stanje na racunu se podrazumevano stvara sa 0 dinara
        values = (email, password, privilegija, godina)
        cursor.execute(sql, values)
        mydb.commit()

        return 'Uspesno ste se registrovali!'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template(
            'login.html'
        )

    else:
        email = request.form['email']
        password = request.form['password']

        cursor = mydb.cursor(prepared = True)
        sql = "SELECT * FROM korisnik WHERE email = ?"
        value = (email, )
        cursor.execute(sql, value)

        res = cursor.fetchone()

        if res == None:
            return render_template(
                'login.html',
                email_error = 'Nalog sa ovim email-om ne postoji.'
            )

        res = dekodiraj(res)

        if password != res[2]:
            return render_template(
                'login.html',
                password_error = 'Pogresna lozinka!'
            )

        session['email'] = email
        session['privilegija'] = res[3]
        
        return redirect(
            url_for('users')
        )


def dekodiraj(data):
    data = list(data)
    n = len(data)
    for i in range(n):
        if isinstance(data[i], bytearray):
            data[i] = data[i].decode()
        
    return data
        

@app.route('/logout')
def logout():
    if 'email' in session:
        session.pop('email')
        session.pop('privilegija')
        return redirect(
            url_for('login')
        )

    else:
        return 'Niste ni bili ulogovani!'


@app.route('/users')
def users():
    cursor = mydb.cursor(prepared = True)
    sql = "SELECT * FROM korisnik"
    cursor.execute(sql)

    res = cursor.fetchall()

    n = len(res)
    for i in range(n):
        res[i] = list(res[i])
        res[i] = dekodiraj(res[i])
    
    return render_template(
        'users.html',
        users = res
    )

@app.route('/profil/<email>')
def profil(email):
    if 'email' not in session or session['email'] != email:
        return redirect(
            url_for('users')
        )

    cursor = mydb.cursor(prepared = True)
    sql = "SELECT * FROM korisnik WHERE email = ?"
    value = (email, )
    cursor.execute(sql, value)

    res = cursor.fetchone()
    if res == None:
        return 'ne postoji taj profil'

    return render_template(
        'profil.html',
        user = dekodiraj(res)
    )

@app.route('/update/<email>', methods=['GET', 'POST'])
def update(email):
    cursor = mydb.cursor(prepared = True)
    sql = "SELECT * FROM korisnik WHERE email = ?"
    value = (email, )
    cursor.execute(sql, value)

    res = cursor.fetchone()
    res = dekodiraj(res)

    if res == None:
        return redirect(
            url_for('users')
        )

    if request.method == 'GET':
        return render_template(
            'update.html',
            user = res
        )

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        confirm = request.form['confirm']
        godina = request.form['godina']
        stanje = request.form['stanje']

        cursor = mydb.cursor(prepared = True)
        cursor.execute(sql, value)

        res = cursor.fetchone()
        res = dekodiraj(res)

        #Prvo proveravamo lozinku iz baze:
        if password != res[2]:
            return render_template(
                'update.html',
                user = res,
                password_error = 'Pogresna Lozinka'
            )

        #Zatim proveravamo da li se lozinke poklapaju, kao vid potvrde
        if password != confirm:
            return render_template(
                'update.html',
                user = res,
                confirm_error = 'Lozinke se ne poklapaju!'
            )

        cursor = mydb.cursor(prepared = True)
        sql = "UPDATE korisnik SET godina_rodjenja = ?, stanje_na_racunu = ? WHERE email = ?"
        values = (godina, stanje, email)
        cursor.execute(sql, values)
        mydb.commit()

        return redirect(
            url_for('users')
        )

@app.route('/delete/<email>')
def delete(email):
    cursor = mydb.cursor(prepared = True)
    sql = "DELETE FROM korisnik WHERE email = ?"
    value = (email, )
    cursor.execute(sql, value)
    mydb.commit()

    return redirect(
        url_for('users')
    )


class Korisnik:
    id: int
    email: str
    password: str
    vrsta_korisnika: int
    godina_rodjenja: int
    stanje_na_racunu: int

    def __init__(self, id, email, password, vrsta_korisnika, godina_rodjenja, stanje_na_racunu) -> None:
        self.id = id
        self.email = email
        self.password = password
        self.vrsta_korisnika = vrsta_korisnika
        self.godina_rodjenja = godina_rodjenja
        self.stanje_na_racunu = stanje_na_racunu

    #Getteri i setteri
    def __str__(self) -> str:
        res = ""

        res += f"ID: {self.id}\n"
        res += f"Email: {self.email}\n"
        res += f"Password: {self.password}\n"
        res += f"Vrsta korisnika: {self.vrsta_korisnika}\n"
        res += f"Godina rodjenja: {self.godina_rodjenja}\n"
        res += f"Stanje na racunu: {self.stanje_na_racunu}\n"

        return res

@app.route('/users_klase')
def klase():
    cursor = mydb.cursor(prepared = True)
    sql = "SELECT * FROM korisnik"
    cursor.execute(sql)

    res = cursor.fetchall()
    n = len(res)
    korisnici = []
    for i in range(n):
        res[i] = list(res[i])
        res[i] = dekodiraj(res[i])
        id = res[i][0]
        email = res[i][1]
        password = res[i][2]
        vrsta_korisnika = res[i][3]
        godina_rodjenja = res[i][4]
        stanje = res[i][5]

        korisnik = Korisnik(id, email, password, vrsta_korisnika, godina_rodjenja, stanje)
        korisnici.append(korisnik)

    return render_template(
        'klase.html',
        users = korisnici
    )



app.run(debug = True)