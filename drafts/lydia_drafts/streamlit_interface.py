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
        results = cursor.fetchall()

        for record in results:
            employee_number = record['employeeNumber']
            last_name = record['lastName']
            first_name = record['firstName']
            customer_name = record['customerName']
            check_number = record['checkNumber']
            payment_date = record['paymentDate']
            amount = record['amount']
            st.write(f"Employee Number: {employee_number}")
            st.write(f"Employee Name: {first_name} {last_name}")
            st.write(f"Customer Name: {customer_name}")
            st.write(f"Check Number: {check_number}")
            st.write(f"Payment Date: {payment_date}")
            st.write(f"Payment Amount: ${amount}")
            st.markdown("---")


    except Exception as e:
        print(f"Exception occurred: {e}")

con.close()