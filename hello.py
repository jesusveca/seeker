
from flask import Flask
from flask import render_template
from flask_bootstrap import Bootstrap
from flask import request, flash

 

app = Flask(__name__) 
 
app.secret_key = 'development key'

result_global = []



@app.route("/")
def hello():
   return render_template('index.html')

@app.route("/controller")
def controller():
   return render_template('index.html',list = ['julio','juan'])

def ejemplo(lista):
	return lista.split()




@app.route("/search", methods = ['POST'])
def search():
#con las Keywords obtendremos una estructura que contiene los resultados de busqueda
   global result_global
   result_global = request.form['keywords']
   return render_template('search.html',keywords = result_global.split(),method = 'POST')

#@app.route("/search")
@app.route("/search/<page_id>")
def pagine(page_id):

   return render_template('search.html', keywords = ejemplo(result_global))





Bootstrap(app)
if __name__ == "__main__":
	app.run()
