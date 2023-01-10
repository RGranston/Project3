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