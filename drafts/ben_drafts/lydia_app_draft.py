#imports
import pymysql
from connector import start_rds_connection

#establish database connection
con = start_rds_connection()

#create cursor object
cursor = con.cursor()

#write sql query
sql_query = "SELECT * FROM employees"

#execute query
try:
    cursor.execute(sql_query)
    results = cursor.fetchall()

    for record in results:
        employee_number = record['employeeNumber']
        first_name = record['firstName']
        last_name = record['lastName']
        print(f"Employee Number: {employee_number}, First Name: {first_name}, Last Name: {last_name}")

#print exception message if failed
except Exception as e:
    print(f"Exception occurred: {e}")

#close connection
con.close()