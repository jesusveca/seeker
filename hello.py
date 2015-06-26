
from flask import Flask
from flask import render_template
from flask_bootstrap import Bootstrap
from flask import request, flash
from flask.ext.sqlalchemy import SQLAlchemy
 

app = Flask(__name__) 
 
app.secret_key = 'development key'

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/new'

db = SQLAlchemy(app)

@app.route("/")
def hello():
   return render_template('index.html')

@app.route("/controller")
def controller():
   return render_template('index.html',list = ['julio','juan'])

@app.route('/search', methods = ['POST'])
def search():

#con las Keywords obtendremos una estructura que contiene los resultados de busqueda

   keywords = request.form['keywords']

   
   result = []

   result = keywords


   return render_template('search.html',keywords = keywords.split()	,method = 'POST')


Bootstrap(app)
if __name__ == "__main__":
	app.run()
