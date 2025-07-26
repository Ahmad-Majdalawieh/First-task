import streamlit as st
import sqlite3
import pandas as pd
import requests

st.set_page_config(page_title="Employee Management")
st.title('Employee Management Page')

URL = "http://127.0.0.1:8000"
response = requests.get(URL + "/employee")

st.markdown('Form to add new employees')

name = st.text_input("Enter employee name")
department = st.text_input("Enter department")
salary = st.number_input("Enter salary")
hire_date = st.date_input("Select hire date")

if st.button("Submit Add"):
    add_data = {
        "name": name,
        "department": department,
        "salary": salary,
        "hire_date": str(hire_date),
    }
    response = requests.post(URL + "/employee/add", json=add_data)
    if response.status_code == 200:
        st.success("Employee added successfully!")
    else:
        st.error("Failed to add employee.")

st.subheader("Option to update or delete existing employees")

option = st.selectbox("Will you update or delete employees?", ("Update","Delete" ))

def update_delete(option, employee_id, updated_data=None):
    if option == "Update":
        url = URL + "/employee/" + str(employee_id) + "/update"
        response = requests.put(url, json=updated_data)
    elif option == "Delete":
        url = URL + "/employee/" + str(employee_id) + "/delete"
        response = requests.delete(url)
    else:
        response = None
    return response

employee_id = st.text_input("Enter Employee ID")

if st.button("Submit"):
    if option == "Update":
        updated_data = {
            "name": st.text_input("Name"),
            "department": st.text_input("Department"),
            "salary": st.number_input("Salary", min_value=0.0),
            "hire_date": str(st.date_input("Hire Date")),
        }
        response = update_delete(option, employee_id, updated_data)
    else:
        response = update_delete(option, employee_id)

    if response and response.status_code == 200:
        st.success(option + " successful!")
    else:
        st.error(option + " failed.")
