import webapp2
import jinja2
import os
import re
from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), '')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape = True)

class Art(db.Model):
    subject = db.StringProperty(required=True)
    content = db.TextProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)


class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

# class FizzBuzz(Handler):
#     def get(self):
#         n=self.request.get('n', 0)
#         n = n and int(n)
#         self.render('fizzbuzz.html', n=n)

class Blog(Handler):
    def render_front(self, subject='', content='', error=''):
        arts = db.GqlQuery('select * from Art order by created desc')
        self.render('base.html', subject=subject, content=content, error=error, arts=arts)

    def get(self):
        self.render_front()

    # def post(self):


class NewPost(Handler):
    def render_new(self, subject='', content='', error_subject='', error_content=''):
        # self.render('new_post.html', subject=subject, content=content, error-subject=error-subject, error-content=error-content)
        self.render('new_post.html' % {'subject': subject,
                                        'content': content,
                                        'error_subject': error_subject,
                                        'error_content': error_content})

    def get(self):
        self.render_new()

    def post(self):
        subject = self.request.get('subject')
        content = self.request.get('content')
        if content and subject:
            a = Art(subject = subject, content = content)
            a.put()
            permalink = Art.key(a).id()

            # self.redirect('/' + str(permalink))
            self.redirect('/add.html/' + str(permalink), permalink)



class Side(Handler):
    def get(self, permalink):
        pas = Art.get_by_id(permalink)
        self.render('/add.html/', permalink, pas=pas)

        # elif not content:
        #     self.write('new_post.html' % {'subject': subject,
        #                                     'content': content,
        #                                     'error-subject': error-subject,
        #                                     'error-content': error-content})


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
    ('/blog', Blog),
    ('/newpost', NewPost),
    (r'/add.html/(\d+)', Side)

], debug=True)
