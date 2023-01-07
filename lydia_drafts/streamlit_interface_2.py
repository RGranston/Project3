#imports
import pymysql
from connector import start_rds_connection
import streamlit as st
import pandas as pd
import sqlalchemy as sql
from config import PASSWORD

#establish database connection
connection = start_rds_connection()
#create cursor object
cursor = connection.cursor()

database_connection_string = f"mysql+pymysql://admin:{PASSWORD}@project-database.cmlzwclsvyh6.us-west-2.rds.amazonaws.com:3306/classicmodels"

engine = sql.create_engine(database_connection_string, echo=True)

identifier = st.text_input("Enter your employee number")

#write sql query
sql_query = f"""
SELECT
    employeeNumber,
    firstName,
    lastName,
    customerName,
    checkNumber,
    paymentDate,
    amount
FROM employees
LEFT JOIN customers ON
    employeeNumber = salesRepEmployeeNumber
LEFT JOIN payments ON
    payments.customerNumber = customers.customerNumber
WHERE employeeNumber = {identifier}
ORDER BY
    paymentDate;
"""
if st.button("Search records"):
    try:
        cursor.execute(sql_query)
        results_df = pd.read_sql_query(sql_query, con=engine)
        st.dataframe(results_df)


    except Exception as e:
        print(f"Exception occurred: {e}")

connection.close()