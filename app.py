from turtle import update
from flask import Flask
import pandas as pd
import psycopg2
import json
import array
conn = psycopg2.connect(
    host="localhost",
    database="db1",
    port=5433,
    user="postgres",
    password="root123")

cursor = conn.cursor()
app = Flask(__name__)
@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/List/")
def getList():
    cursor.execute('''SELECT * from employee_Anuja''')
    result = cursor.fetchall()
    print(type(result))
    print(len(result))
    json_string = json.dumps(result)
    resultJson = []
    for res in result:
        resultJson.append({
            "serial_number":res[0],
            "company_name":res[1],
            "employee_name":res[2],
            "description":res[3],
              "status":res[4]
        })
    return json.dumps(resultJson)

@app.route("/match/")
def getmatched():
    cursor.execute('''SELECT * from employee_Anuja''')
    result = cursor.fetchall() 
    df = pd.DataFrame(result, 
                  columns = ['serial_number','company_name','employee_name','description','status'])
    duplicate = df[df.duplicated(['serial_number'])]
    for row in duplicate['serial_number']:
        print('found match')
        cursor.execute('''Update employee_Anuja SET status = %s where serial_number =%s''',("matched",row))
        print(row)
    print(duplicate)
    cursor.execute('''SELECT * from employee_Anuja''')
    result = cursor.fetchall()
   
    conn.commit()
    resultJson = []

    for res in result:
        
        resultJson.append({
            "serial_number":res[0],
            "company_name":res[1],
            "employee_name":res[2],
            "description":res[3],
              "status":res[4]
        })
    
        
    print(resultJson)
    return json.dumps(resultJson)

if __name__=="main":
    app.run(debug=True)