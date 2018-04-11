import webapp2
import jinja2
import os
import cgi

def escape_html(s):
    return cgi.escape(s, quote = True)

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

class MainHandler(Handler):
    def get(self):
        self.render("instruction.html")

    def post(self):
        # print "Please, enter the line in small letters or the morse code using spaces between letters (symbols)."
        # print "If there is s mistake in your line, you'll see '@' sign in the output"
        # line = raw_input()
        eng_alphabeth = {'a':".-", 'b':"-...", 'c':"-.-.", 'd':"-..", 'e':".", 'f':"..-.", 'g':"--.",'h':"....",
                    'i':"..", 'j':".---", 'k':"-.-", 'l':".-..", 'm':"--", 'n':"-.", 'o':"---",
                     'p':".--.", 'q':"--.-", 'r':".-.", 's':"...", 't':"-", 'u':"..-",
                     'v':"...-", 'w':".--", 'x':"-..-", 'y':"-.--", 'z':"--..", '1':".----",
                     '2':"..---", '3':"...--", '4':"....-", '5':".....",
                     '6':"-....", '7':"--...", '8':"---..", '9':"----.", '0':"-----"}

        morse_alphab = {".-":'a', "-...":'b', "-.-.":'c', "-..":'d', ".":'e', "..-.":'f', "--.":'g', "....":'h',
                    "..":'i', ".---":'j', "-.-":'k', ".-..":'l', "--":'m', "-.":'n', "---":'o',
                     ".--.":'p', "--.-":'q', ".-.":'r', "...":'s', "-":'t', "..-":'u',
                     "...-":'v', ".--":'w', "-..-":'x', "-.--":'y', "--..":'z', ".----":'1',
                     "..---":'2', "...--":'3', "....-":'4', ".....":'5',
                     "-....":'6', "--...":'7', "---..":'8', "----.":'9', "-----":'0', "||": ' '}

        output = ''
        # if self.request.get("refresh"):
        #     self.render("index.html", user_input='', output='')
        line = escape_html(self.request.get("user_input"))
        if line == '':
            self.render("instruction.html")
        else:
            if line[0] == '.' or line[0] == '-':
                form = line.split()
                for l in form:
                    if l in morse_alphab:
                        output += morse_alphab[l]
                    if l not in morse_alphab:
                        output += '?'
            else:
                for letter in line:
                    if letter in eng_alphabeth:
                        output += eng_alphabeth[letter] + ' '
                    if letter not in eng_alphabeth:
                        if letter == " ":
                            output += " || "
                        else:
                            output += '?' + ' '
            self.render("instruction.html", user_input=line, output=output)

class About(MainHandler):
    def get(self):
        self.render('about.html')

class Dictionary(MainHandler):
    def get(self):
        self.render('dictionary.html')


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/about', About),
    ('/dictionary', Dictionary)
], debug=True)
