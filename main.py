import webapp2

class HelloWebapp2(webapp2.RequestHandler):
    def get(self):
        self.response.write('''<!DOCTYPE html>
        <html>
          <head>
            <meta charset="utf-8" content="text/html">
            <title>Just a page</title>
            <style>
            div {
              color: red;
              background-color: black;
              display: inline-block;
            }

            .but:hover {
              color: blue;
              background-color: yellow;
              cursor: pointer;
            }
            p:hover {
                height: 10px;
            }
            </style>
          </head>
          <body>
            <div>
              <p>
                Some text
              </p>
              <input type='submit' class="but" name="go!" value="Vtudeeeee!">
            </div>
          </body>
        </html>''')

app = webapp2.WSGIApplication([
    ('/', HelloWebapp2),
], debug=True)
