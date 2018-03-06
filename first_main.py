import webapp2
import cgi

form = """<form method="post">
    <label> Type in what is 2+2=
    <input type="text" name="answer" value="%(answer)s">
    </label>
    <br>
    <div style="color: red;">%(error)s</div>
    <input type="submit">
    </form>
"""

def escape_html(s):
    return cgi.escape(s, quote = True)

class HelloWebapp2(webapp2.RequestHandler):
    def write_form(self, error="", answer=''):
        self.response.out.write(form % {'error': escape_html(error),
                                        'answer': escape_html(answer)})

    def get(self):
        # self.response.headers['Content-Type'] = 'text/plain'
        self.write_form()

# class TestHandler(webapp2.RequestHandler):
    def post(self):
        # q = self.request.get('q')
        # self.response.out.write(q)

        ans = self.request.get('answer')
        # start = q.find('answer=')
        # ans = q[start+7:start+8]
        if ans == '5':
            self.response.headers['Content-Type'] = 'text/plain'
            self.redirect("/thanks")
        else:
            self.response.headers['Content-Type'] = 'text/html'
            self.write_form("Invalid input!", ans)

        # self.response.headers['Content-Type'] = 'text/plain'
        # self.response.out.write(self.request)
class ThanksHandler(webapp2.RequestHandler):
    def get(self):
        self.response.out.write("Right")

app = webapp2.WSGIApplication([
    ('/', HelloWebapp2),
    ('/thanks', ThanksHandler)
    # ('/testform', TestHandler),
], debug=True)
