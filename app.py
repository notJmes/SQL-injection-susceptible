from flask import Flask, render_template, request, redirect, url_for, session, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from archive import Archive, get_archive_stats
import os


#config
app = Flask(__name__)
app.config["DEBUG"] = True
app.config["TESTING"] = True
app.config['SECRET_KEY'] = 'ilovekali'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app_db.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

#SQL
db = SQLAlchemy(app)

class Users(db.Model):
    email = db.Column(db.String(50), primary_key=True)
    pwd = db.Column(db.String(50))
    username = db.Column(db.String(50))

host = '127.0.0.1'
port = 5000
archive_dict = {}

@app.before_request
def before_request():
    if 'username' not in request.cookies and request.endpoint != 'login':
        return redirect(url_for('login'))

@app.route('/')
def home():

    username = request.cookies.get('username')
    querystatement = request.cookies.get('querystatement')
    

    return render_template('home.html', username=username, querystatement=querystatement, archive_dict=archive_dict)

@app.route('/login', methods=['GET', 'POST'])
def login():
    string = ""
    if request.method == 'POST':
        print('POST sent')

        email = request.form.get('email')
        pwd = request.form.get('pass')
        string = """select * from users where email='{email}' and pwd='{pwd}' """.format(email=email, pwd=pwd)
        sql = text(string)
        results = db.engine.execute(sql).fetchone()
        if results is None:
            print('No users queried')

            resp = make_response(redirect(url_for('login')))
            resp.set_cookie('querystatement', string)

            return resp
        else:
            resp = make_response(redirect(url_for('home')))
            resp.set_cookie('username', results[2])
            resp.set_cookie('querystatement', string)
            return resp

    else:
        print('GET sent')
        string = request.cookies.get('querystatement') or ""
    return render_template('login.html', querystatement=string)


with app.app_context():
    db.create_all()

    try:
        table_row = Users(email="admin@mail.com", pwd="123456", username="admin")
        db.session.add(table_row)
        db.session.commit()
    except:
        print('admin has been created already')
    



if __name__ == '__main__':
    get_archive_stats(archive_dict=archive_dict)
    app.run(host=host, port=port)
