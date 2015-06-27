
from flask import Flask
from flask import render_template
from flask_bootstrap import Bootstrap
from flask import request, flash
import pre_process
import datetime
 

app = Flask(__name__) 
 
app.secret_key = 'development key'



query_global = ""
result_global = []
result_total_len = 0
result_final = []
both_date_set = False


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
   global result_final
   global from_date
   global to_date
   global both_date_set


   result_final = []
   query_global = request.form['keywords']

   from_date = request.form['from_date']
      
   to_date = request.form['to_date']
   
   result_global = processlogic.process_query(query_global) #lista de tuplas

   result_total_len = int(len(result_global)/20) + 2

   if from_date!="" and to_date!="":  #ambas fechas
      both_date_set = True
      from_date = datetime.datetime.strptime(from_date[2:],"%y-%m-%d").date()
      to_date = datetime.datetime.strptime(to_date[2:],"%y-%m-%d").date()
      count = 0
      for x in result_global:
        if count == 19:
            break
        temp = processlogic.json_obj.select_data(x[0])  # date  = datetime.date(2013, 5, 16)
        if temp[0][0] < to_date and temp[0][0] > from_date:     
            result_final.append(temp[0])
            count += 1
   else:
      both_date_set = False
      result_temp = result_global[:20]
      result_final = []
      for x in result_temp:
         temp = processlogic.json_obj.select_data(x[0])
         result_final.append(temp[0])
 
   #print (result_final)
   return render_template('search.html',keywords = query_global, result = result_final , from_date = from_date, to_date = to_date, len_result = result_total_len,method = 'POST')

#@app.route("/search")
@app.route("/search/<int:page_id>")
def pagine(page_id):

   index = page_id*20
   result_final = []
   if both_date_set == True:
      result_temp = result_global[index-20:]
      count = 0
      for x in result_temp:
         if count == 19:
            break
         temp = processlogic.json_obj.select_data(x[0])  # date  = datetime.date(2013, 5, 16)
         if temp[0][0] < to_date and temp[0][0] > from_date:     
            result_final.append(temp[0])
            count += 1
   else:
      result_temp = result_global[index-20:index]      
      for x in result_temp:
         temp = processlogic.json_obj.select_data(x[0])
         result_final.append(temp[0])

   return render_template('search.html', keywords = query_global, result = result_final, from_date = from_date, to_date = to_date, len_result = result_total_len)	

Bootstrap(app)
if __name__ == "__main__":
	app.run()
