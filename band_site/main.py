from flask import Flask, url_for, redirect, request, render_template, session
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_login import UserMixin, LoginManager, current_user, login_user, logout_user
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
from functools import wraps

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///band.db'
app.config['SECRET_KEY'] = 'gewagh23tgaweFWF3'

db = SQLAlchemy(app)

login = LoginManager(app)

@login.user_loader
def load_user(user_id):
    return AdminBase.query.get(user_id)

class MyModelViev(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login_for_admin'))

class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated

admin = Admin(app, index_view=MyAdminIndexView())

class AdminBase(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String(25))
    password = db.Column(db.String(50))

# this part allows admin to manipulate AdminBase db(add, delete etc.)
# admin.add_view(MyModelViev(AdminBase, db.session))

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
        result = AdminBase.query.filter_by(name=username).first()
        if result:
            password = result.password
            if sha256_crypt.verify(password_candidate, password):
                session['logged_in'] = True
                session['username'] = username
                login_user(result)
                return redirect(url_for('index'))
            else:
                return render_template('login_for_admin.html')
        else:
            return render_template('login_for_admin.html')
    return render_template('login_for_admin.html')

@app.route('/admin/logout')
def logout():
    session.clear()
    logout_user()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
