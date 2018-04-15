import webapp2
import jinja2
import re
import os
import cgi
import logging
import hmac
import hashlib
import random
import json
import string
from google.appengine.ext import db
from google.appengine.api import memcache


USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
PASS_RE = re.compile(r"^.{3,20}$")
MAIL_RE = re.compile(r"^[\S]+@[\S]+\.[\S]+$")


secret = 'KL5b3'

def make_sec_val(val):
    return '%s|%s' % (val, hmac.new(secret, val).hexdigest())

def check_sec_val(sec_val):
    val = sec_val.split('|')[0]
    if sec_val == make_sec_val(val):
        return val

template_dir = os.path.join(os.path.dirname(__file__), '')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape = True)

def escape_html(s):
    return cgi.escape(s, quote = True)

def valid_username(username):
    if username and USER_RE.match(username):
        return True
    return False

def user_exist(username):
    # maybe try select * from Users where username=username
    check_user = db.GqlQuery('select * from Users')
    for unit in check_user:
        if unit.username == username:
            return True
    return False

def valid_password(password):
    if password and PASS_RE.match(password):
        return True
    return False

def valid_verify(verify, password):
    if verify and verify == password:
        return True
    return False

def valid_email(email):
    if not email or MAIL_RE.match(email):
        return True
    return False

def make_salt():
    return ''.join(random.choice(string.letters) for x in xrange(5))

def make_pw_hash(name, pw, salt = None):
    if not salt:
        salt = make_salt()
    h = hashlib.sha256(name + pw + salt).hexdigest()
    return "%s,%s" % (h, salt)

def valid_pw(name, pw, h):
    salt = h.split(',')[1]
    if make_pw_hash(name, pw, salt) == h:
        return True
    return False

def login_pw_verify(name, pw):
    database = db.GqlQuery('select * from Users')
    for entry in database:
        if entry.username == name:
            if valid_pw(name, pw, entry.password):
                return True
    return False

class Users(db.Model):
    username = db.StringProperty(required=True)
    password = db.StringProperty(required=True)
    email = db.StringProperty()
    created = db.DateTimeProperty(auto_now_add=True)

class Posts(db.Model):
    post_name = db.StringProperty(required=True)
    content = db.TextProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)

def top_posts(update = False):
    key = 'top'
    posts = memcache.get(key)
    if posts is None or update:
        posts = db.GqlQuery('select * from Posts order by created desc')
        posts = list(posts)
        memcache.set(key, posts)
        logging.info('hit the db')
    return posts

def get_from_cache(page):
    #try to use name of the page instead id as permalink
    posts = memcache.get('top')
    # secs = memcache.get('secs')
    if not posts:
        posts = top_posts(True)
    elif posts:
        posts = list(posts)
    pas = None
    for a in posts:
        if a.post_name == page:
            pas = a
            break
    return pas




class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

class MainPage(Handler):
    # def render_front_page(self):
    #     self.render("base.html")
    def render_front_page(self, page = None):
        page = get_from_cache("main")
        self.render("wikipage.html", page = page)


    def get(self):
        self.render_front_page()

class Signup(Handler):
    def render_sup(self, **params):
        # yet leave this without errors
        self.render("registration.html", **params)

    def get(self):
        self.render_sup()

    def post(self):
        #placed escape_html here
        username = self.request.get("username")
        password = self.request.get("password")
        verify = self.request.get("verify")
        email = self.request.get("email")

        error_username=""
        error_password=""
        error_verify=""
        error_email=""

        if valid_username(username) and valid_password(password) and valid_verify(verify, password) and valid_email(email) and not user_exist(username):
            password = make_pw_hash(username, password)
            base = Users(username = username, password = password, email = email)
            base.put()
            user = base.key().id()
            self.response.headers.add_header('Set-Cookie', 'user_id=%s; Path=/' % make_sec_val(str(user)))
            self.redirect('/')
        else:
            params = dict(username=escape_html(username), email=escape_html(email))
            if not valid_username(username):
                params['error_username'] = "That's not a valid username."
                params['password'] = ''
            if user_exist(username):
            	params['error_username'] = "That user already exists."
            	params['password'] = ''
            if not valid_password(password) or not password:
                params['error_password'] = "That's not a valid password."
                params['password'] = ''
            if not valid_verify(verify, password):
                params['error_verify'] = "That's not a valid verify."
                params['password'] = ''
                params['verify'] = ''
            if not valid_email(email):
                params['error_mail'] = "That's not a valid email."
            # logging.info(params)
            self.render_sup(**params)

class Login(Handler):
    def render_login(self, **params):
        # req = db.GqlQuery('select * from Users where username=:1', "qwerty" ).get()
        # logging.info(dir(req.get()))
        self.render('login.html', **params)

    def get(self):
        self.render_login()

    def post(self):
        username = self.request.get('username')
        password = self.request.get("password")

        if valid_username(username) and valid_password(password) and login_pw_verify(username, password):
            user = Users.all().filter('username = ', username).get()
            self.response.headers.add_header('Set-Cookie', 'user_id=%s; Path=/' % make_sec_val(str(user.key().id())))
            self.redirect('/')
        else:
            params = dict(username = "", password = "", error = "Invalid login")
            self.render_login(**params)


class EditPage(Handler):
    def render_edit_page(self, page = None):

        self.render("edit.html", page=page)

    def get(self):
        url_page = page_from_url(self.request.url)
        if url_page == '':
            url_page = "main"
            # need to gigure out how to meke the main page editable
        page = get_from_cache(url_page)
        # logging.info(page.post_name)
        user_id = self.request.cookies.get('user_id')
        if not user_id or not check_sec_val(user_id):
            if page and page.post_name != "main":
                self.redirect("/" + page.post_name)
            elif page and page.post_name == "main":
                self.redirect("/")
            else:
                self.error(404)
                return
        if page:
            self.render_edit_page(page)
        else:
            self.render_edit_page()


    def post(self):
        # need a hint for main page
        post_name = page_from_url(self.request.url)
        if post_name == '':
            post_name = "main"
        content = self.request.get("user_post")
        if content:
            # logging.info(content)
            post = Posts(post_name = post_name, content = content)
            post.put()
            a = post.key().id()
            test = Posts.get_by_id(a)
            permalink = post.post_name
            if permalink == "main":
                permalink = ""
            posts = top_posts(True)
            # permalink = posts[0].post_name
            # logging.info(posts[0].content)
            self.redirect("/" + permalink)
        # in case
        # else:
        #     self.redirect("/")


def page_from_url(url):
    return "".join(url.split('/')[-1])

class WikiPage(Handler):
    def render_wiki_page(self, page = None):
        self.response.headers['Content-Type'] = "text/html"
        self.render('wikipage.html', page=page)

    def get(self):
        url_page = page_from_url(self.request.url)
        # logging.info(self.request.url)
        # if not url_page:
            # need to gigure out how to meke the main page editable
        page = get_from_cache(url_page)
        if page:
            self.render_wiki_page(page)
        else:
            user_id = self.request.cookies.get('user_id')
            if not user_id or not check_sec_val(user_id):
                if page:
                    self.redirect("/" + url_page)
                else:
                    self.error(404)
                    return
            # logging.info(url_page)
            # logging.info('right')
            self.redirect('/_edit/' + url_page)


class Logout(Handler):
    def get(self):
        # del_page_time_cache()
        # self.response.delete_cookie('user_id')
        self.response.headers.add_header('Set-Cookie', 'user_id=; Path=/')
        self.redirect("/")


PAGE_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")

app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/signup', Signup),
    ('/login', Login),
    ('/logout', Logout),
    # ('/_edit/' + PAGE_RE, EditPage),
    # ('/' + PAGE_RE, WikiPage)
    ('/_edit/', EditPage),
    (r'^/_edit/[a-zA-Z0-9_-]{3,20}$', EditPage),
    (r'^/[a-zA-Z0-9_-]{3,20}$', WikiPage)
    # this regular expression is ? because of / inside it
], debug=True)
