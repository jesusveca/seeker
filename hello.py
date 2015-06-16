
from flask import Flask
from flask import render_template
from flask_bootstrap import Bootstrap


app= Flask(__name__)


@app.route("/")
def hello():
   return render_template('bootstrapexample.html')

@app.route("/controller")
def controller():
   return render_template('index.html',list = ['julio','juan'])




Bootstrap(app)
if __name__ == "__main__":
	app.run()
