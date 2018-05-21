from flask import Flask, render_template, session, flash, url_for, redirect, logging, request
from flask_mysqldb import MySQL
from passlib.hash import sha256_crypt
from siteforms import RegisterForm, ArticleForm
from functools import wraps

def _index():
    return render_template('home.html')

def _about():
    return render_template('about.html')

def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, please login', 'danger')
            return redirect(url_for('login'))
    return wrap

def _register(mysql):
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        email = form.email.data
        username = form.username.data
        password = sha256_crypt.encrypt(str(form.password.data))
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users(name, email, username, password) VALUES (%s,%s,%s,%s);", (name, email, username, password))
        mysql.connection.commit()
        cur.close()
        flash('You are now registered and can log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

def _login(mysql):
    if request.method == 'POST':
        username = request.form['username']
        password_candidate = request.form['password']
        cur = mysql.connection.cursor()
        result = cur.execute('SELECT * FROM users WHERE username = (%s)', [username])
        if result > 0:
            data = cur.fetchone()
            password = data['password']
            if sha256_crypt.verify(password_candidate, password):
                session['logged_in'] = True
                session['username'] = username
                flash('You are now logged in', 'success')
                return redirect(url_for('dashboard'))
            else:
                error = 'Invalid login'
                return render_template('login.html', error=error)
            cur.close()
        else:
            error = 'Username not found'
            return render_template('login.html', error=error)
    return render_template('login.html')

def _logout():
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('login'))

def _articles(mysql):
    cur = mysql.connection.cursor()
    result = cur.execute('SELECT * FROM articles ORDER BY create_date;')
    articles = cur.fetchall()
    if result > 0:
        return render_template('articles.html', articles=articles)
    else:
        msg = 'No articles found'
        return render_template('articles.html', msg=msg)
    cur.close()

def _article(id, mysql):
    cur = mysql.connection.cursor()
    result = cur.execute('SELECT * FROM articles WHERE id = (%s);', (id, ))
    article = cur.fetchone()
    return render_template('article.html', article=article)
    cur.close()

def _dashboard(mysql):
    cur = mysql.connection.cursor()
    result = cur.execute('SELECT * FROM articles ORDER BY create_date;')
    articles = cur.fetchall()
    if result > 0:
        return render_template('dashboard.html', articles=articles)
    else:
        msg = 'No articles found'
        return render_template('dashboard.html', msg=msg)
    cur.close()

def _add_article(mysql):
    form = ArticleForm(request.form)
    if request.method == 'POST' and form.validate():
        title = form.title.data
        body = form.body.data
        cur = mysql.connection.cursor()
        result = cur.execute('INSERT INTO articles(title, body, author) VALUES (%s, %s, %s);', (title, body, session['username']))
        mysql.connection.commit()
        cur.close()
        flash('Article created', 'success')
        return redirect(url_for('dashboard'))
    return render_template('add_article.html', form=form)

def _edit_article(id, mysql):
    cur = mysql.connection.cursor()
    result = cur.execute('SELECT * FROM articles WHERE id = (%s);', (id, ))
    article = cur.fetchone()
    form = ArticleForm(request.form)
    form.title.data = article['title']
    form.body.data = article['body']
    if request.method == 'POST' and form.validate():
        title = request.form['title']
        body = request.form['body']
        cur = mysql.connection.cursor()
        result = cur.execute('UPDATE articles SET title=(%s), body=(%s) WHERE id = (%s);', (title, body, id))
        mysql.connection.commit()
        cur.close()
        flash('Article edited', 'success')
        return redirect(url_for('dashboard'))
    cur.close()
    return render_template('edit_article.html', form=form)

def _delete_article(id, mysql):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM articles WHERE id = (%s);', (id, ))
    mysql.connection.commit()
    cur.close()
    flash('Article deleted', 'success')
    return redirect(url_for('dashboard'))
