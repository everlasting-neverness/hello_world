from flask import Flask, request, url_for, render_template, redirect, send_file
from flask_sqlalchemy import SQLAlchemy
from io import BytesIO

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tryflask.db'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:f0reverm0re@localhost/tryflask'
db = SQLAlchemy(app)


# class Example(db.Model):
# 	__tablename__ = 'example'
# 	id = db.Column('id', db.Integer, primary_key=True)
# 	data = db.Column('data', db.Unicode)
#
# 	def __init__(self, id, data):
# 		self.id = id
# 		self.data = data

class File(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(300))
	data = db.Column(db.LargeBinary)

@app.route('/')
def index():
	# result = db.session.execute('select * from example where id = 3;').fetchone()
	# print dir(db.session)
	# db.session.delete(result)
	# db.session.close()
	# result = Example.query.filter_by(id=3).first()
	# db.session.delete(result)
	# db.session.commit()
	# output = db.session.execute('select * from example;').fetchall()
	# return str(len(output))
	filedata = File.query.all()
	print filedata[0].name
	return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
	file = request.files['inputFile']
	newfile = File(name=file.filename, data=file.read())
	db.session.add(newfile)
	db.session.commit()
	return 'Saved' + file.filename + ' to the database!'

@app.route('/download')
def download():
	filedata = File.query.filter_by(name='03-the_last_rock_and_roll_star.mp3')
	return send_file(BytesIO(filedata[0].data), attachment_filename='03-the_last_rock_and_roll_star.mp3', as_attachment=True)

if __name__ == '__main__':
	app.debug = True
	app.run(host='0.0.0.0', port=5000)
