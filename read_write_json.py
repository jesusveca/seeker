import psycopg2
import json

class JsonManagePsql:
    def __init__(self):
        #self.initialize_psql()
        pass  
    def initialize_psql(self):
        #try:
            #self.conn = psycopg2.connect(database="NewsSearcher", user="postgres", password="", host="127.0.0.1", port="5432")
        #except:
            #print("I am unable to connect to the database")
        pass
    def read_json_file(self, file_name):
        with open(file_name) as json_file:
            json_data = json.load(json_file)
            return json_data
    def insert_data(self,categoria,titulo,fecha,url): 
        cursor = self.conn.cursor()
        query =  "INSERT INTO Noticias (categoria, titulo, fecha, url) VALUES (%s, %s, %s, %s);"
        data = (str(categoria),str(titulo),str(fecha),str(url))
        try:
            cursor.execute(query, data)
        except psycopg2.DataError:
            print(data)
            self.conn.commit()
            return False
        self.conn.commit()
        return True
