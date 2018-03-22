import webapp2
import jinja2
import random
import string
import hashlib
import os
import re
import cgi
from google.appengine.ext import db

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
PASS_RE = re.compile(r"^.{3,20}$")
MAIL_RE = re.compile(r"^[\S]+@[\S]+\.[\S]+$")

def escape_html(s):
    return cgi.escape(s, quote = True)

def valid_username(username):
    check_name = db.GqlQuery('select * from UserBase')
    for a in check_name:
        if a.username == username:
            return False
    if USER_RE.match(username):
        return True
    return False

def valid_password(password):
    if PASS_RE.match(password):
        return True
    return False

def valid_verify(password, verify):
    if verify == password:
        return True
    return False

def valid_email(email):
    if email == '':
        return True
    if MAIL_RE.match(email):
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


template_dir = os.path.join(os.path.dirname(__file__), '')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape = True)

class UserBase(db.Model):
    username = db.StringProperty(required=True)
    password = db.StringProperty(required=True)
    email = db.StringProperty()
    created = db.DateTimeProperty(auto_now_add=True)


class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

outer = {}

class HelloWebapp2(Handler):
    def write_form(self, error_name="", error_pass="", error_ver="", error_mail="", username='', password='', verify='', email=''):
        self.render("form.html", error_name=escape_html(error_name), error_pass=escape_html(error_pass), error_ver=escape_html(error_ver),
                                    error_mail=escape_html(error_mail), username=escape_html(username), password=escape_html(password),
                                    verify=escape_html(verify), email=escape_html(email))

    def get(self):
        # self.response.headers['Content-Type'] = 'text/plain'
        self.write_form()

# class TestHandler(webapp2.RequestHandler):
    def post(self):
        username = self.request.get('username')
        password = self.request.get('password')
        verify = self.request.get('verify')
        email = self.request.get('email')

        error_name=""
        error_pass=""
        error_ver=""
        error_mail=""

        if valid_username(username) and valid_password(password) and valid_verify(password, verify) and valid_email(email):
            # outer['username'] = username
            password = make_pw_hash(username, password)



            base = UserBase(username = username, password = password, email = email)
            base.put()
            user = base.key().id()
            # self.response.headers['Content-Type'] = 'text/plain'
            self.response.headers.add_header('Set-Cookie', 'name=%s; Path=/' % str(username))
            self.redirect("/welcome")
        else:
            if not valid_username(username):
                error_name = "That's not a valid username."
            if not valid_password(password) or not password:
                error_pass = "That's not a valid password."
                password = ''
            if not valid_verify(password, verify):
                error_ver = "That's not a valid verify."
                password = ''
                verify = ''
            if not valid_email(email):
                error_mail = "That's not a valid email."
            # self.response.headers['Content-Type'] = 'text/html'
            self.write_form(error_name, error_pass, error_ver,
                                        error_mail, username, password,
                                        verify, email)


class ThanksHandler(Handler):
    def get(self):
        username = self.request.cookies.get('name')
        # person = UserBase.get_by_id(int(user))
        # username = person.username
        # username = outer['username']
        # username = self.request.get('username')
        self.response.headers['Content-Type'] = 'text/html'
        self.render("welc_form.html", username=username)
        # check_name = db.GqlQuery('select * from UserBase')
        # out = []
        # for a in check_name:
        #     if a.username == username:
        #         out.append(a.username)
        # self.response.out.write(out)

app = webapp2.WSGIApplication([
    # ('/blog', Blog),
    # ('/blog/newpost', NewPost),
    # (r'/blog/(\d+)', Side),
    ('/blog/signup', HelloWebapp2),
    ('/welcome', ThanksHandler)
], debug=True)
