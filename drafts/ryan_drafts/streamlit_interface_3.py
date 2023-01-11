#imports
from connector import start_rds_connection
import streamlit as st
import pandas as pd
import sqlalchemy as sql
from config import PASSWORD, USERNAME, ENDPOINT, DBNAME, PORT

#establish database connection
connection = start_rds_connection()
#create cursor object
cursor = connection.cursor()
#create database connection string
database_connection_string = f"mysql+pymysql://{USERNAME}:{PASSWORD}@{ENDPOINT}:{PORT}/{DBNAME}"
#create engine
engine = sql.create_engine(database_connection_string, echo=True)

#search emplyee records
st.markdown("# Employee Records Search")

#text box where the employee enters their information
user_input = st.sidebar.text_input(f"Enter your employee number")

#employee lookup
employee_lookup_query = f'''
SELECT * FROM employees;
'''

#press the button to search records
if st.button("Employee Lookup"):
    try:
        results_df = pd.read_sql_query(employee_lookup_query, con=engine)
        st.dataframe(results_df)


    except Exception as e:
        st.write(f"Error: {e}")

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
WHERE employeeNumber = "{user_input}"
ORDER BY
    paymentDate;
"""

#press the button to search records
if st.button("Employee Sales"):
    try:
        results_df = pd.read_sql_query(sql_query, con=engine)
        st.dataframe(results_df)


    except Exception as e:
        st.write(f"Error: {e}")

connection.close()

#employee customer list
employee_customer_query = f'''
SELECT * FROM customers WHERE salesRepEmployeeNumber = "{user_input}";
'''

if st.button("Employee's Customer List"):
    try:
        results_df = pd.read_sql_query(employee_customer_query, con=engine)
        st.dataframe(results_df)


    except Exception as e:
        st.write(f"Error: {e}")

# Check number of shipped orders

shipped_orders_query = f'''

select 
e.firstName, 
e.lastName, 
count(*) as 'Number of shipped orders'
from customers c
join orders o on o.customerNumber = c.customerNumber
join employees e on e.employeeNumber = c.salesRepEmployeeNumber
where o.status = 'Shipped'
group by e.firstName, e.lastName
order by count(*)desc
'''

#press the button to show number of shipped orders
if st.button("Number of shipped orders by employee"):
    try:
        results_df = pd.read_sql_query(shipped_orders_query, con=engine)
        st.dataframe(results_df)


    except Exception as e:
        st.write(f"Error: {e}")



# Check Inventory Status
st.markdown("# Inventory Records Search")

item_status_query = f'''
select
p.productName,
p.productVendor,
p.quantityInStock,
p.buyPrice,
pl.productLine

from products p
join productlines pl
on p.productLine = pl.productLine


order by pl.productLine

'''

if st.button("Inventory Status"):
    try:
        results_df = pd.read_sql_query(item_status_query, con=engine)
        st.dataframe(results_df)


    except Exception as e:
        st.write(f"Error: {e}")

#orders that havent shipped
not_shipped_query = f'''
SELECT * FROM orders WHERE status != 'Shipped';
'''

if st.button("Orders Not Shipped"):
    try:
        results_df = pd.read_sql_query(not_shipped_query, con=engine)
        st.dataframe(results_df)


    except Exception as e:
        st.write(f"Error: {e}")