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
st.markdown("# Classic Models Inc.") 
st.markdown("## Employee Dashboard:")
image = Image.open('69_camaro.jpeg')


st.image(image)

st.markdown("### Employee Records Search:")

#the employee selects their identifier type
#identifier_type = st.sidebar.selectbox(
    #"By what information would you like to search for records?",
    #(identifiers))

#change the identifier type to it can be part of the query
#identifier = identifiers.get(identifier_type)

#text box where the employee enters their information
#user_input = st.sidebar.text_input(f"Enter your {identifier_type}")
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
st.markdown("### Inventory Status:")
# Check Inventory Status

# Select Product Line to view
product_type = st.selectbox(
    "Which product line would you like to view?",
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


vendor = st.selectbox(
    "Which vendor would you like to view?",
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

st. markdown("## Add Customer")
Customer_number = int
Customer_name = vars
Last_name = vars
First_name = vars
Phone = vars
Address_line_1 = vars
City = vars
State = vars
Country = vars


st.write (" #### Enter Customer information")
customerNumber = st.text_input("Customer Number")
customerName = st.text_input("Customer Name")
contactLastName = st.text_input("Last Name")
contactFirstName = st.text_input("First Name")
phone = st.text_input("Phone")
addressLine1 = st.text_input("Address line 1")
city = st.text_input("City")
state = st.text_input("State")
country = st.text_input("Country")

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




st.markdown("### Update Customer Records:")

customer_information = {
    "Customer Name":"customerName",
    "Contact Last Name":"contactLastName",
    "Contact First Name":"contactFirstName",
    "Phone Number":"phone",
    "Address Line 1":"addressLine1",
}

#ways the employee can identify themself
customer_number = st.text_input("Enter your customer number")

information_type = st.selectbox("What information would you like to update?", (customer_information))

new_input = st.text_input(f"Enter your new {information_type}")

#change the identifier type to it can be part of the query
info_to_update = customer_information.get(information_type)

#write sql query
sql_query = f"""
UPDATE
    customers
SET {info_to_update} = "{new_input}"
WHERE customerNumber = {customer_number};
"""

#press the button to search records
if st.button("Update Information"):
    try:
        #pd.read_sql_query(sql_query, con=engine)
        #st.write("Update Successful")
        cursor.execute(sql_query)
        connection.commit()
        st.write("Update Successful")

    except Exception as e:
        st.write(f"Error: {e}")

connection.close()