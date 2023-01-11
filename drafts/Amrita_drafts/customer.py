import pymysql
import pandas as pd
import matplotlib.pyplot as plt
from connector import start_rds_connection
import streamlit as st

#establish database connection
con = start_rds_connection()

#create cursor object
cursor = con.cursor()


Customer_numbr = int
Customer_name = vars
Last_name = vars
First_name = vars
Phone = vars
Address_line_1 = vars
City = vars
State = vars
Country = vars

with st.form("entry form", clear_on_submit = False):
    st.write ("### Enter Customer information")
    customerNumber = st.text_input("Customer_number")
    customerName = st.text_input("Customer_name")
    contactLastName = st.text_input("Last_name")
    contactFirstName = st.text_input("First_name")
    phone = st.text_input("Phone")
    addressLine1 = st.text_input("Address_line_1")
    city = st.text_input("City")
    state = st.text_input("State")
    country = st.text_input("Country")
    submitted = st.form_submit_button()
if submitted:
    #def insert_records():
    try:
        with con.cursor() as cursor:
            sql = f"INSERT INTO customers (`customerNumber`, `customerName`, `contactLastName`, `contactFirstName`, \
                                        `phone`, `addressLine1`, `city`, `state`,`country`) \
                                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);"
            cursor.execute(sql, (customerNumber,customerName,contactLastName,contactFirstName, \
                                phone,addressLine1,city, state, country))

        # Connection is not autocommit by default, so we must commit to save changes
        con.commit()
        print(f'Successfully inserted records')
        
    except Exception as e:
        print(f'Error in insertion to MySQL database: {e}')
    #insert_records()
    st.write ("### done")
##get_records('SELECT * FROM customers WHERE customerNumber = 497;')