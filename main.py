import webapp2
import cgi
import re

# form = """<form method="post">
#     <label> Type in what is 2+2=
#     <input type="text" name="answer" value="%(answer)s">
#     </label>
#     <br>
#     <div style="color: red;">%(error)s</div>
#     <input type="submit">
#     </form>
# """
form = """<form method="post">
        <label> Username
        <input type="text" name="username" value="%(username)s">
        <div style="color:red">%(error_name)s</div>
        </label>
        <br>
        <label> Password
        <input type="password" name="password" value="%(password)s">
        <div style="color:red">%(error_pass)s</div>
        </label>
        <br>
        <label> Verify Password
        <input type="password" name="verify" value="%(verify)s">
        <div style="color:red">%(error_ver)s</div>
        </label>
        <br>
        <label> Email (optional)
        <input type="email" name="email" value="%(email)s">
        <div style="color:red">%(error_mail)s</div>
        </label>
        <br>
        <input type="submit">
</form>
"""

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
PASS_RE = re.compile(r"^.{3,20}$")
MAIL_RE = re.compile(r"^[\S]+@[\S]+\.[\S]+$")

def escape_html(s):
    return cgi.escape(s, quote = True)

def valid_username(username):
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

# class HelloWebapp2(webapp2.RequestHandler):
#     def write_form(self, error="", username='', password='', verify='', email=''):
#         self.response.out.write(form % {'error': escape_html(error),
#                                         'username': escape_html(username),
#                                         'password': escape_html(password),
#                                         'verify': escape_html(verify),
#                                         'email': escape_html(email)})

outer = {}

class HelloWebapp2(webapp2.RequestHandler):
    def write_form(self, error_name="", error_pass="", error_ver="", error_mail="", username='', password='', verify='', email=''):
        self.response.out.write(form % {'error_name': escape_html(error_name),
                                        'error_pass': escape_html(error_pass),
                                        'error_ver': escape_html(error_ver),
                                        'error_mail': escape_html(error_mail),
                                        'username': escape_html(username),
                                        'password': escape_html(password),
                                        'verify': escape_html(verify),
                                        'email': escape_html(email)})

    def get(self):
        # self.response.headers['Content-Type'] = 'text/plain'
        self.write_form()

# class TestHandler(webapp2.RequestHandler):
    def post(self):
        # q = self.request.get('q')
        # self.response.out.write(q)
        username = self.request.get('username')
        password = self.request.get('password')
        verify = self.request.get('verify')
        email = self.request.get('email')

        if valid_username(username) and valid_password(password) and valid_verify(password, verify) and valid_email(email):
            outer['username'] = username
            # self.response.headers['Content-Type'] = 'text/plain'
            self.redirect("/signup?username=" + username)
        else:
            # if not valid_username(username):
            #     self.response.headers['Content-Type'] = 'text/html'
            #     self.write_form("That's not a valid username.","", "", "",  username, password, verify, email)
            # elif not valid_password(password):
            #     self.response.headers['Content-Type'] = 'text/html'
            #     self.write_form("","That's not a valid password.","", "", username, password, verify, email)
            # elif not valid_verify(password, verify):
            #     self.response.headers['Content-Type'] = 'text/html'
            #     self.write_form("", "", "That's not a valid verify.", "", username, password, verify, email)
            # elif not valid_email(email):
            #     self.response.headers['Content-Type'] = 'text/html'
            #     self.write_form("", "", "","That's not a valid email.", username, password, verify, email)
            fill = []
            if not valid_username(username):
                fill.append("That's not a valid username.")
            elif valid_username(username):
                fill.append("")
            if not valid_password(password):
                fill.append("That's not a valid password.")
                password = ''
            elif valid_password(password):
                fill.append("")
            if not valid_verify(password, verify):
                fill.append("That's not a valid verify.")
                password = ''
                verify = ''
            elif valid_verify(password, verify):
                fill.append("")
            if not valid_email(email):
                fill.append("That's not a valid email.")
            elif valid_email(email):
                fill.append("")
            self.response.headers['Content-Type'] = 'text/html'
            self.write_form(fill[0], fill[1], fill[2], fill[3], username, password, verify, email)
        # self.response.headers['Content-Type'] = 'text/plain'
        # self.response.out.write(self.request)

welc_form = """
        <p>
        Welcome, %s!
        </p>
"""

class ThanksHandler(webapp2.RequestHandler):
    def get(self):
        name = outer['username']
        self.response.headers['Content-Type'] = 'text/html'
        self.response.out.write(welc_form % name)


app = webapp2.WSGIApplication([
    ('/', HelloWebapp2),
    ('/signup', ThanksHandler)
    # ('/testform', TestHandler),
], debug=True)
