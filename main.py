import webapp2

form = """<form method="post">
    <label> Enter
    <input type="textarea" name="answer" value="%(answer)s" style="border:3px solid green;color:blue;weidth:300px;height:100px;">
    </label>
    <br>
    <div style="color: red;"></div>
    <input type="submit">
    </form>
"""

class HelloWebapp2(webapp2.RequestHandler):
    def write_form(self, answer=''):
        self.response.out.write(form % {'answer': answer})

    def get(self):
        self.write_form()

    def post(self):
        # q = self.request.get('q')
        # self.response.out.write(q)

        ans = self.request.get('answer')
        self.response.headers['Content-Type'] = 'text/html'
        self.write_form(self.rot13(ans))

    def rot13(self, s):
        output = ''
        for a in s:
            if ord(a) in range(65, 91):
                if (ord(a)+13) >= 91:
                    n = (ord(a)+13) - 91
                    output += (chr(65+n))
                else:
                    output += chr(ord(a)+13)
            elif ord(a) in range(97, 123):
                if (ord(a)+13) >= 123:
                    n = (ord(a)+13) - 123
                    output += (chr(97+n))
                else:
                    output += chr(ord(a)+13)
            else:
                output += a
        return output

app = webapp2.WSGIApplication([
    ('/', HelloWebapp2),
    # ('/thanks', ThanksHandler)
    # ('/testform', TestHandler),
], debug=True)
