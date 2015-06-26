
from flask import Flask
from flask import render_template
from flask_bootstrap import Bootstrap
from flask import request, flash
import pre_process
 

app = Flask(__name__) 
 
app.secret_key = 'development key'



query_global = ""
result_global = []
result_total_len = 0

processlogic = pre_process.PreProcessManager()
processlogic.read_all_data_from_files()


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
   global query_global
   global result_global
   global result_total_len

   query_global = request.form['keywords']

   result_global = processlogic.process_query(query_global) #lista de tuplas

   result_total_len = int(len(result_global)/20) + 2

   result_temp = result_global[:20]

   return render_template('search.html',keywords = query_global, result = result_temp , len_result = result_total_len,method = 'POST')

#@app.route("/search")
@app.route("/search/<int:page_id>")
def pagine(page_id):

   index = page_id*20
   result_temp = result_global[index-20:index]

   return render_template('search.html', keywords = query_global, result = result_temp, len_result = result_total_len)	





Bootstrap(app)
if __name__ == "__main__":
	app.run()
