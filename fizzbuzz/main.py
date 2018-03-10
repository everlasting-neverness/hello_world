import webapp2
import jinja2
import os

template_dir = os.path.join(os.path.dirname(__file__), '')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape = True)

class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

class FizzBuzz(Handler):
    def get(self):
        n=self.request.get('n', 0)
        n = n and int(n)
        self.render('fizzbuzz.html', n=n)

# class HelloWebapp2(webapp2.RequestHandler):
#     def write_form(self, ):
#         self.response.out.write(form % )
#
#     def get(self):
#         # self.response.headers['Content-Type'] = 'text/plain'
#         self.write_form()
#
# # class TestHandler(webapp2.RequestHandler):
#     def post(self):
#         # q = self.request.get('q')
#         # self.response.out.write(q)
#         username = self.request.get('username')
#         password = self.request.get('password')
#         verify = self.request.get('verify')
#         email = self.request.get('email')
#
#
# class ThanksHandler(webapp2.RequestHandler):
#     def get(self):
#         name = outer['username']
#         self.response.headers['Content-Type'] = 'text/html'
#         self.response.out.write(welc_form % name)


app = webapp2.WSGIApplication([
    # ('/', HelloWebapp2),
    ('/fizzbuzz', FizzBuzz)
    # ('/testform', TestHandler),
], debug=True)
