from flask import Flask, url_for, redirect, request, render_template, session
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
from functools import wraps

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///band.db'
app.config['SECRET_KEY'] = 'gewagh23tgaweFWF3'

db = SQLAlchemy(app)

admin = Admin(app)

class Lyrics(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(300))
    content = db.Column(db.Text)

    def __repr__(self):
        return '<Lyrics %r>' % (self.name)

class Events(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    place = db.Column(db.String(300))
    data = db.Column(db.String(100))
    comment = db.Column(db.Text)

    def __repr__(self):
        return '<Events %r>' % (self.place)

class News(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(100))
    name= db.Column(db.String(150))
    content = db.Column(db.Text)
    pictures = db.Column(db.LargeBinary)

    def __repr__(self):
        return '<News %r>' % (self.name)

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String(25))
    password = db.Column(db.String(50))

admin.add_view(ModelView(Lyrics, db.session))
admin.add_view(ModelView(Events, db.session))
admin.add_view(ModelView(News, db.session))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/news')
def news():
    news = News.query.all()
    return render_template('news.html', news=news)

@app.route('/news/<int:news_id>/')
def news_item(news_id):
    item = News.query.filter_by(id=news_id).first()
    return render_template('news_item.html', item=item)

@app.route('/materials')
def materials():
    return render_template('materials.html')

@app.route('/events')
def events():
    events = Events.query.all()
    return render_template('events.html', events=events)

# @app.route('/photos')
# def photos():
#     return render_template('photos.html')

@app.route('/materials/lyrics')
def lyrics():
    texts = Lyrics.query.all()
    return render_template('lyrics.html', texts=texts)

@app.route('/materials/lyrics/<string:song_name>/')
def song_lyrics(song_name):
    song = Lyrics.query.filter_by(name=song_name).first()
    if song:
        song = lyrics_maker(song)
        print song.content
        return render_template('song_lyrics.html', song=song)
    return '404 - there is now such song'

def lyrics_maker(song):
    text = song.content.split('\n')
    song.content = text
    return song

@app.route('/login_for_admin', methods=['GET', 'POST'])
def login_for_admin():
    if request.method == 'POST':
        username = request.form['username']
        password_candidate = request.form['password']
        result = Admin.query.filter_by(name=username).first()
        if result:
            password = result.password
            if sha256_crypt.verify(password_candidate, password):
                session['logged_in'] = True
                session['username'] = username
                return redirect(url_for('index'))
            else:
                return render_template('login_for_admin.html')
        else:
            return render_template('login_for_admin.html')
    return render_template('login_for_admin.html')

def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        print 'wraps'
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            return redirect(url_for('index'))
    return wrap

@app.route('/admin')
@is_logged_in
def admin():
    return render_template('admin/index.html')

@app.route('/login_for_admin/logout')
@is_logged_in
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
