import sqlite3
import fastapi
from pydantic import BaseModel
import pandas as pd
import json

db_path = "employee.db"
conn = sqlite3.connect(db_path, check_same_thread=False)
cursor = conn.cursor()

def create_table():
    table = """create table IF NOT EXISTS employee (employee_id integer primary key autoincrement,name text not null,department text not null,salary real not null,hire_date text not null)"""
    cursor.execute(table)

class Employee(BaseModel):
    name: str
    department: str
    salary: float
    hire_date: str

app = fastapi.FastAPI()

@app.get("/employee")
async def employee_all_data():
    statement = """select * from employee"""
    cursor_obj = cursor.execute(statement)
    read_str = json.dumps(cursor_obj.fetchall())
    return {"ROWS": read_str}

@app.get("/employee/{employee_id}")
def single_employee_data(employee_id: int):
    statement = """select * from employee where employee_id = ?"""
    cursor_obj = cursor.execute(statement, (employee_id,))
    row = cursor_obj.fetchone()
    columns = [column[0] for column in cursor.description]
    if row is None:
        return {"error": f"No employee found with ID {employee_id}"}
    else:
        row_dict = dict(zip(columns, row))
        return {"ROW": row_dict}

@app.post("/employee/add")
def employee_add_data(employee: Employee):
    statement = """insert into employee (name, department, salary, hire_date) values (?, ?, ?,?)"""
    cursor.execute(statement, (employee.name, employee.department, employee.salary, employee.hire_date))
    conn.commit()
    return {"Message": "employee added successfully", "employee": employee}

@app.put("/employee/{employee_id}/update")
def employee_update_data(employee_id: int, employee: Employee):
    statement = """ UPDATE employee SET name = ?, department = ?, salary = ?, hire_date = ? WHERE employee_id = ?"""
    cursor.execute(statement, (employee.name,employee.department, employee.salary, employee.hire_date, employee_id ))
    conn.commit()
    return {"message": "Data updated", "employee": employee}

@app.delete("/employee/{employee_id}/delete")
def employee_delete_data(employee_id: int):
    statement = """delete from employee where employee_id = ?"""
    cursor.execute(statement, (employee_id,))
    conn.commit()
    return {"message": "Employee data deleted"}


