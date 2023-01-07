#imports
import pymysql
from connector import start_rds_connection
import streamlit as st

#establish database connection
con = start_rds_connection()

#create cursor object
cursor = con.cursor()

identifier = st.text_input("Enter your employee number")

#write sql query
sql_query = f"""
SELECT
    employeeNumber,
    firstName,
    lastName,
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
        results = cursor.fetchall()

        for record in results:
            st.write(record)

    except Exception as e:
        print(f"Exception occurred: {e}")

con.close()