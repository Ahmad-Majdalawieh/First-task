import streamlit as st
import pandas as pd
from matplotlib import pyplot as plt
import sqlite3

st.set_page_config(page_title="Home Page")

st.title("Dashboard Page")

db_path = 'employee.db'

conn =  sqlite3.connect(db_path, check_same_thread=False)

df = pd.read_sql_query("SELECT * FROM employee", conn)
st.subheader("Employee's Details")
st.dataframe(df)


st.subheader("Analytics")


st.markdown("Average salary for all employees")
avg_salary = df["salary"].mean()
st.metric("Average Salary", avg_salary)

st.markdown("Number of employees in each department") #bar chart
employee_count_by_dept = df["department"].value_counts()
st.bar_chart(employee_count_by_dept)

st.subheader("Salary distribution")#histogram
fig, ax = plt.subplots()
ax.hist(df['salary'], bins=10, color='skyblue', edgecolor='black')
st.pyplot(fig)


conn.close()