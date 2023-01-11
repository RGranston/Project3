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

#application header
st.markdown("# Classic Models Inc. Employee Dashboard") 
image = Image.open('69_camaro.jpeg')
st.image(image)

#employee records search header
st.markdown("## Employee Records Search:")

#text input box for the employee to enter their number
user_input = st.sidebar.text_input(f"Enter your employee number")

#query to display information of all employees
employee_lookup_query = f"""
SELECT * FROM employees;
"""

#press the button to search records
if st.button("Search All Employees"):
    try:
        results_df = pd.read_sql_query(employee_lookup_query, con=engine)
        st.dataframe(results_df)


    except Exception as e:
        st.write(f"Error: {e}")

#query to search employee sales records
employee_sales_query = f"""
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

#press the button to search employee sales records
if st.button("Employee Sales"):
    try:
        results_df = pd.read_sql_query(employee_sales_query, con=engine)
        st.dataframe(results_df)


    except Exception as e:
        st.write(f"Error: {e}")



#query to display all of the customers for the specified employee
employee_customer_query = f"""
SELECT * FROM customers WHERE salesRepEmployeeNumber = "{user_input}";
"""

#press the button to execute the query
if st.button("Employee's Customer List"):
    try:
        results_df = pd.read_sql_query(employee_customer_query, con=engine)
        st.dataframe(results_df)


    except Exception as e:
        st.write(f"Error: {e}")

#query to display shipped orders
shipped_orders_query = f"""
SELECT
    e.firstName, 
    e.lastName, 
COUNT(*) AS "Number of shipped orders"
FROM
    customers c
JOIN orders o ON o.customerNumber = c.customerNumber
JOIN employees e ON e.employeeNumber = c.salesRepEmployeeNumber
WHERE
    o.status = "Shipped"
GROUP BY e.firstName, e.lastName
ORDER BY COUNT(*)DESC;
"""

#press the button to show number of shipped orders
if st.button("Number of shipped orders by employee"):
    try:
        results_df = pd.read_sql_query(shipped_orders_query, con=engine)
        st.dataframe(results_df)


    except Exception as e:
        st.write(f"Error: {e}")

#query to display orders not yet shipped
not_shipped_query = f"""
SELECT * FROM orders WHERE status != 'Shipped';
"""

#press the button to execute the query
if st.button("Orders Not Shipped"):
    try:
        results_df = pd.read_sql_query(not_shipped_query, con=engine)
        st.dataframe(results_df)


    except Exception as e:
        st.write(f"Error: {e}")

st.markdown("---")

#inventory status section header
st.markdown("## Inventory Status:")

# Check Inventory Status
# Select Product Line to view
product_type = st.selectbox(
    "Which product line would you like to view?",
    ("Classic Cars", "Motorcycles","Planes","Ships","Trains","Trucks and Buses", "Vintage Cars"))
   
#query to check item status
item_status_query = f"""
SELECT
    p.productName,
    p.productVendor,
    p.quantityInStock,
    p.buyPrice,
    pl.productLine
FROM
    products p
JOIN
    productlines pl
ON
    p.productLine = pl.productLine
WHERE
    p.productLine = "{product_type}"
ORDER BY
    pl.productLine
"""

#press the button to execute the query
if st.button("Inventory Status by Product Line"):
    try:
        results_df = pd.read_sql_query(item_status_query, con=engine)
        st.dataframe(results_df)


    except Exception as e:
        st.write(f"Error: {e}")


#select which vendor to view
vendor = st.selectbox(
    "Which vendor would you like to view?",
    ("Autoart Studio Design", "Autoart Studio Design","Classic Metal Creations","Classic Metal Creations","Gearbox Collectibles","Highway 66 Mini Classics",
     "Min Lin Diecast", "Motor City Art Classics","Red Start Diecast","Second Gear Diecast","Studio M Art Models","Unimax Art Galleries","Welly Diecast Productions"))


#query to check the vendor status
vendor_status_query = f"""
SELECT
    p.productName,
    p.productVendor,
    p.quantityInStock,
    p.buyPrice,
    pl.productLine
FROM
    products p
JOIN
    productlines pl ON p.productLine = pl.productLine
WHERE
    p.productVendor = "{vendor}"
ORDER BY
    p.productVendor
"""

#press the button to execute the query
if st.button("Inventory Status by Vendor"):
    try:
        results_df = pd.read_sql_query(vendor_status_query, con=engine)
        st.dataframe(results_df)


    except Exception as e:
        st.write(f"Error: {e}")

st.markdown("---")

#add customer section header
st. markdown("## Add Customer")
#Customer_number = int
#Customer_name = vars
#Last_name = vars
#First_name = vars
#Phone = vars
#Address_line_1 = vars
#City = vars
#State = vars
#Country = vars


st.markdown(" #### Enter Customer Information")

#text input boxes to enter new customer's information
customerNumber = st.text_input("Customer Number")
customerName = st.text_input("Customer Name")
contactLastName = st.text_input("Last Name")
contactFirstName = st.text_input("First Name")
phone = st.text_input("Phone")
addressLine1 = st.text_input("Address line 1")
city = st.text_input("City")
state = st.text_input("State")
country = st.text_input("Country")

#press the button to enter the customer
if st.button("Enter Customer"):
    
    try:
        sql = f"INSERT INTO customers (`customerNumber`, `customerName`, `contactLastName`, `contactFirstName`, \
                                        `phone`, `addressLine1`, `city`, `state`,`country`) \
                                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);"
        cursor.execute(sql, (customerNumber,customerName,contactLastName,contactFirstName, \
                                phone,addressLine1,city, state, country))

        # Connection is not autocommit by default, so we must commit to save changes
        connection.commit()
        print(f'Successfully inserted records')
        
    except Exception as e:
        print(f'Error in insertion to MySQL database: {e}')
    #insert_records()
    st.write ("Records successfully inserted")

st.markdown("---")

#update customer records section header
st.markdown("## Update Customer Records:")

customer_information = {
    "Customer Name":"customerName",
    "Contact Last Name":"contactLastName",
    "Contact First Name":"contactFirstName",
    "Phone Number":"phone",
    "Address Line 1":"addressLine1",
}

#enter the number of the customer whose information you want to update
customer_number = st.text_input("Enter your customer number")

#select what information to update
information_type = st.selectbox("What information would you like to update?", (customer_information))

#enter the new information to be updated
new_input = st.text_input(f"Enter your new {information_type}")

#change the identifier type to it can be part of the query
info_to_update = customer_information.get(information_type)

#query to update customer information
cusotmer_update_query = f"""
UPDATE
    customers
SET {info_to_update} = "{new_input}"
WHERE customerNumber = {customer_number};
"""

#press the button to execute the query
if st.button("Update Information"):
    try:
        cursor.execute(cusotmer_update_query)
        connection.commit()
        st.write("Update Successful")

    except Exception as e:
        st.write(f"Error: {e}")

#close the connection
connection.close()