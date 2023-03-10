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

#ways the employee can identify themself
identifiers = {
    "Email":"email",
    "Employee Number":"employeeNumber",
    "Last Name":"lastName",
    "First Name":"firstName",
    "Extension":"extension"
}

st.markdown("# Employee Records Search")

#the employee selects their identifier type
identifier_type = st.selectbox(
    "By what information would you like to search for records?",
    (identifiers))

#change the identifier type to it can be part of the query
identifier = identifiers.get(identifier_type)

#text box where the employee enters their information
user_input = st.text_input(f"Enter your {identifier_type}")

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