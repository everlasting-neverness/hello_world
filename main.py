import webapp2

# form = """<form  action="/testform">
#     <label>
#     One
#   <input type="radio" name='q' value="one">
#   </label>
#
#   <label>
#   Two
#   <input type="radio" name="q" value="two">
#   </label>
#
#   <label>
#   Three
#   <input type="radio" name='q' value="three">
#   </label>
#   <br>
#   <input type="submit">
# </form>
# """
form = """<form  action="/testform">
    <select name="q">
        <option value="1">One</option>
        <option value="2">Two</option>
        <option value="3">Three</option>
    </select>
    <br>
    <input type="submit">
    </form>
"""

class HelloWebapp2(webapp2.RequestHandler):
    def get(self):
        # self.response.headers['Content-Type'] = 'text/plain'
        self.response.write(form)

class TestHandler(webapp2.RequestHandler):
    def get(self):
        q = self.request.get('q')
        self.response.out.write(q)
        # self.response.headers['Content-Type'] = 'text/plain'
        # self.response.out.write(self.request)

app = webapp2.WSGIApplication([
    ('/', HelloWebapp2),
    ('/testform', TestHandler),
], debug=True)
