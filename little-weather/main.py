import requests
from flask import url_for, Flask, render_template, request, redirect


app = Flask(__name__)

@app.route('/', methods=['GET','POST'])
def index():
    weather = {}
    # print 'wag'
    if request.method == 'POST':
        # print 'here'
        url = 'https://developer.github.com/v3/'
        r = requests.get(url).json()
        print r
        return redirect(url_for('index'))
    return render_template('index.html', weather=weather)














if __name__ == '__main__':
    app.debug = True
    app.run('0.0.0.0', port=5000)
