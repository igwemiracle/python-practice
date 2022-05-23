from flask import Flask, render_template, request, g
import sqlite3

app = Flask(__name__)
  
def connect_db():
	sql = sqlite3.connect('/Users/apple/Documents/MYPROJECT/project.db')
	sql.row_factory = sqlite3.Row  #This enables the results to be displayed as python dictionaries.
	return sql

def get_db():
	if not hasattr(g, 'sqlite3'):
		g.sqlite_db = connect_db()
	return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
	if hasattr(g, 'sqlite_db'):
		g.sqlite_db.close()

  
@app.route('/main')
def main():
	return render_template('main.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'GET':
		return render_template('login.html')
	else:
		name = request.form['name']
		location = request.form['location']

		db = get_db()
		db.execute('insert into forms (name, location) values(?, ?)', [name, location])
		db.commit()

		return '<h1> Hi {}. You are from {}. You have submitted your form successively! </h1>'.format(name, location)
	

'''
@app.route("/process", methods=['POST'])
def process():
	name = request.form['name']
	location = request.form['location']

	return '<h1> Hi {}. You are from {}. You have submitted the form successfully! </h1>'.format(name, location)
'''
@app.route('/link')
def link():
	return render_template('link.html')

@app.route('/query')
def query():
	name = request.args.get('name')
	location = request.args.get('location')
	return '<h1> Hi {}. You are from {}. You are on the Query page</h1>'.format(name, location)

@app.route('/viewresult')
def viewresult():
	db = get_db()
	cur = db.execute('select id, name, location from forms')
	result = cur.fetchall()
	return '<h1>The ID is {}. The Name is {}. The Location is {}.</h1>'.format(result[7]['id'], result[7]['name'], result[7]['location'])


if __name__ == "__main__":
  app.run(debug = True, host = "0.0.0.0", port = 3000)