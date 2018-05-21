from flask import Flask
from flask_mysqldb import MySQL
from sitefunctions import _about, _index, is_logged_in, _article, _articles, _register, _login, _logout, _dashboard, _add_article, _delete_article, _edit_article

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'f0reverm0re'
app.config['MYSQL_DB'] = 'myflaskapp'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

@app.route('/')
def index():
    return _index()

@app.route('/about')
def about():
    return _about()

@app.route('/articles')
def articles():
    global mysql
    return _articles(mysql)

@app.route('/article/<string:id>/')
def article(id):
    global mysql
    return _article(id, mysql)

@app.route('/register', methods=['GET', 'POST'])
def register():
    global mysql
    return _register(mysql)

@app.route('/login', methods=['GET','POST'])
def login():
    global mysql
    return _login(mysql)

@app.route('/logout')
@is_logged_in
def logout():
    return _logout()

@app.route('/dashboard')
@is_logged_in
def dashboard():
    global mysql
    return _dashboard(mysql)

@app.route('/add_article', methods=['GET', 'POST'])
@is_logged_in
def add_article():
    global mysql
    return _add_article(mysql)

@app.route('/edit_article/<string:id>/', methods=['GET', 'POST'])
@is_logged_in
def edit_article(id):
    global mysql
    return _edit_article(id, mysql)

@app.route('/delete_article/<string:id>/', methods=['POST'])
@is_logged_in
def delete_article(id):
    global mysql
    return _delete_article(id, mysql)

if __name__ == '__main__':
    app.secret_key = 'secret123'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
