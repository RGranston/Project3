#imports
from connector import start_rds_connection
import streamlit as st
import pandas as pd
import sqlalchemy as sql
from config import PASSWORD, USERNAME, ENDPOINT, DBNAME, PORT
from PIL import Image
#establish database connection
connection = start_rds_connection()
#create cursor object
cursor = connection.cursor()
#create database connection string
database_connection_string = f"mysql+pymysql://{USERNAME}:{PASSWORD}@{ENDPOINT}:{PORT}/{DBNAME}"
#create engine
engine = sql.create_engine(database_connection_string, echo=True)

#ways the employee can identify themself
identifiers = {
    "Email":"email",
    "Employee Number":"employeeNumber",
    "Last Name":"lastName",
    "First Name":"firstName",
    "Extension":"extension"
}
st.markdown("# Classic Models Employee Dashboard:")
image = Image.open('69_camaro.jpeg')
st.image(image)
st.markdown("### Employee Records Search:")

#the employee selects their identifier type
identifier_type = st.sidebar.selectbox(
    "By what information would you like to search for records?",
    (identifiers))

#change the identifier type to it can be part of the query
identifier = identifiers.get(identifier_type)

#text box where the employee enters their information
user_input = st.sidebar.text_input(f"Enter your {identifier_type}")

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
WHERE {identifier} = "{user_input}"
ORDER BY
    paymentDate;
"""

#press the button to search records
if st.button("Search records"):
    try:
        results_df = pd.read_sql_query(sql_query, con=engine)
        st.dataframe(results_df)


    except Exception as e:
        st.write(f"Error: {e}")

connection.close()


st.markdown("### Inventory Status:")
# Check Inventory Status

# Select Product Line to view
product_type = st.sidebar.selectbox(
    "Which Product?",
    ("Classic Cars", "Motorcycles","Planes","Ships","Trains","Trucks and Buses", "Vintage Cars"))
   

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
WHERE p.productLine = "{product_type}"
order by pl.productLine


'''

if st.button("Inventory Status by Product Line:"):
    try:
        results_df = pd.read_sql_query(item_status_query, con=engine)
        st.dataframe(results_df)


    except Exception as e:
        st.write(f"Error: {e}")


vendor = st.sidebar.selectbox(
    "Which Vendor? ?",
    ("Autoart Studio Design", "Autoart Studio Design","Classic Metal Creations","Classic Metal Creations","Gearbox Collectibles","Highway 66 Mini Classics",
     "Min Lin Diecast", "Motor City Art Classics","Red Start Diecast","Second Gear Diecast","Studio M Art Models","Unimax Art Galleries","Welly Diecast Productions"))


vendor_status_query = f'''
select
p.productName,
p.productVendor,
p.quantityInStock,
p.buyPrice,
pl.productLine

from products p
join productlines pl
on p.productLine = pl.productLine
WHERE p.productVendor = "{vendor}"
order by p.productVendor


'''

if st.button("Inventory Status by Vendor:"):
    try:
        results_df = pd.read_sql_query(vendor_status_query, con=engine)
        st.dataframe(results_df)


    except Exception as e:
        st.write(f"Error: {e}")