from fastapi import FastAPI,HTTPException,File, UploadFile
from pydantic import BaseModel
import mysql.connector
app = FastAPI ()

@app.get("/users")
def hello():
    return{"message": "Hello, World!"}
@app.get("/name")
def world():
    return{"text" :"MY name is Fareena Zafar"}
@app.get("/greet/{name}")
def name(name:str):
    return{"message":f"Hello, {name}"}
@app.get("/add/{a}/{b}")
def calculate(a:int,b:int):
    return{"result":a+b}
@app.get("/square")
def calculator(c:int):
    return{"result":c*c}
@app.get("/even/a")
def even(n:int):
    if n%2==0:
        return{"result":"even"}
    else:
        return{"result":"odd"}
@app.get("/calculator/{p}/op/{q}")
def calculator(p:int,op:str,q:int):
  if op=="+":
      return{"result":p+q}
  elif op=="-":
      return{"result":p-q}
  elif op=="*":
      return{"result":p*q}
  elif op=="/":
      return{"result":p/q} 
@app.get("/convert/{temp}")
def convert(temp:float):
    return{"temperature":(temp-32)*5/9}
@app.get("/reverse/{string}")
def reverse(string):
    return{"reverse":string[ : :-1]}
#@app.get("/name")
"""def name(sentence:str):
    word=sentence.split()
    count=len(word)
    return{"sentence":sentence,"word_count":count}"""
@app.get("/name1")
def name(sentence: str):
    word = sentence.split()
    count = len(word)
    return {"sentence": sentence, "word_count": count}


class Name(BaseModel):
    intro:str
@app.post("/names")
def intro(name:Name):
        return{"name":{name.intro} }
          
class BMI(BaseModel):
    weight:float
    height:float  
@app.post("/weight")
def check(bmi:BMI):
    result=bmi.weight/(bmi.height*bmi.height)
    if result < 18.5:
       category = "Underweight"
    elif result < 25:
        category = "Normal"
    else:
        category = "Overweight"
    return {"bmi": result, "category": category}
@app.get("/table")
def table(num:int,table:int):
    result=[]
    
    for i in range (table):

        result.append(num*i)
    
    return{"table":result}
@app.get("/age")
def age(dob:int,mob:int,yob:int,pd:int,pm:int,py:int):
     date=dob-pd   
     if date>0:
        date=dob-pd
     elif date<0:
        date=pd-dob
     month=mob-pm
     if month>0:
        month=mob-pm
     elif month<0:
        month=pm-mob
     year=py-yob
     return{"years":year,"months":month,"days":date}

@app.get("/merge")
def merge():
    list1 = [1, 2, 3]
    list2 = [4, 5, 6]
    list3 = [7, 8, 9]
    
    result = list1 + list2 + list3
    
    return {"merged": result}

@app.get("/find")
def find(number: int):
    my_list = [10, 20, 30, 40, 50]
    
    if number in my_list:
        return {"message": f"{number} found!", "status": True}
    else:
        return {"message": f"{number} not found!", "status": False}
    
@app.get("/add")
def add_item(item: str):
    my_list = ["apple", "banana", "mango"]
    
    my_list.append(item)
    
    return {"list": my_list}

@app.get("/delete/{item}")
def delete_item(item: str):
    my_list = ["apple", "banana", "mango", "orange"]
    
    if item in my_list:
        my_list.remove(item)
        return {"message": f"{item} deleted!", "list": my_list}
    else:
        return {"message": f"{item} not found!"}
 # MySQL Connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Fareena@626",
    database="database"
)
cursor = db.cursor()

# Model
class Student(BaseModel):
    name: str
    age: int
    city: str

# CREATE
@app.post("/students")
def create_student(student: Student):
    query = "INSERT INTO students (name, age, city) VALUES (%s, %s, %s)"
    values = (student.name, student.age, student.city)
    cursor.execute(query, values)
    db.commit()
    return {"message": "Student added!", "id": cursor.lastrowid}

# READ — all students
@app.get("/students")
def get_students():
    cursor.execute("SELECT * FROM students")
    result = cursor.fetchall()
    students = []
    for row in result:
        students.append({
            "id": row[0],
            "name": row[1],
            "age": row[2],
            "city": row[3]
        })
    return {"students": students}

# READ 
@app.get("/students/{id}")
def get_student(id: int):
    cursor.execute("SELECT * FROM students WHERE id = %s", (id,))
    row = cursor.fetchone()
    if row:
        return {"id": row[0], "name": row[1], "age": row[2], "city": row[3]}
    return {"message": "Student not found!"}

# UPDATE
@app.put("/students/{id}")
def update_student(id: int, student: Student):
    query = "UPDATE students SET name=%s, age=%s, city=%s WHERE id=%s"
    values = (student.name, student.age, student.city, id)
    cursor.execute(query, values)
    db.commit()
    return {"message": f"Student {id} updated!"}

# DELETE
@app.delete("/students/{id}")
def delete_student(id: int):
    cursor.execute("DELETE FROM students WHERE id = %s", (id,))
    db.commit()
    return {"message": f"Student {id} deleted!"}
#Book Task 
#CREATE 
class Book(BaseModel):
    title:str 
    Author:str
    price:float
@app.post("/book")
def create_book(book:Book):
    query="INSERT INTO book(title,Author,price) VALUES(%s,%s,%s)"
    values=(book.title,book.Author,book.price)
    cursor.execute(query,values)
    db.commit()
    return{"message": "Book added successfully","book":cursor.lastrowid}  
#READ all books!  
@app.get("/book")
def get_book():
    cursor.execute("SELECT * FROM book")
    result = cursor.fetchall()
    books = []
    for row in result:
        books.append({
            "id": row[0],
            "title": row[1],
            "author": row[2],
            "price": row[3]
        })
    return {"books": books}
class Car(BaseModel):
    id:int 
    model:str
    color:str
    price:int
@app.post("/Url",status_code=201)
def car(car:Car):
    query="INSERT INTO car (id,model,color,price) VALUES (%s,%s,%s,%s)"
    values=(car.id,car.model,car.color,car.price)
    cursor.execute(query,values)
    db.commit()
    return{"message":"Car added successfully"}
@app.get("/Url",status_code=200)
def get_car():
    cursor.execute("SELECT * From car")
    result=cursor.fetchall()
    car=[]
    for row in result:
        car.append({
             "id":row[0],
             "model":row[1],
             "color":row[2],
             "price":row[3]
        })
    return{"Car":car}
@app.get("/Url/{id}",status_code=200)
def get_cars(id:int):
    cursor.execute("SELECT * FROM car WHERE id=%s",(id,))
    row=cursor.fetchone()
    if not row:
        raise HTTPException(
            status_code=404,
            detail={"message":f"no {id} found!"}
        )
    return{"id": row[0], "model": row[1], "color": row[2], "price": row[3]}
@app.post("/Url",status_code=201)
def update_car(id:int,car:Car):
    query="UPDATE car SET model=%s,coor-%s,price=%s WHERE id=%s"
    values=(car.model,car.color,car.price,(id,))
    cursor.execute(query,values)
    row=cursor.fetchone()
    if not row:
        raise HTTPException(
            status_code=404,
            detail={"message":f"no {id} found!"}
        )
    return{"Car {id} updated successfully"}

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    return {"filename": file.filename}

import os
os.makedirs("uploads", exist_ok=True)
@app.post("/ul")
async def update(size: UploadFile = File(...)):
    if size.content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(
            status_code=400,
            detail="Type not found"
        )
    contents = await size.read()
    file_path = f"uploads/{size.filename}"
    with open(file_path, "wb") as buffer:
        buffer.write(contents)
    return {
        "filename": size.filename,
        "Type": size.content_type,
        "size": f"{len(contents)/1024:.2f}KB"
    }
    
# --- THIS is "in-memory storage" ---
# Just a normal Python list, sitting in the computer's memory.
# No database, no file, nothing saved to disk.
todos = []


@app.post("/todos")
def add_todo(title: str):
    # Every time someone calls this, we just append to the list
    todo = {"id": len(todos) + 1, "title": title, "completed": False}
    todos.append(todo)
    return todo


@app.get("/todos")
def get_todos():
    # We just return whatever is currently in the list
    return todos

