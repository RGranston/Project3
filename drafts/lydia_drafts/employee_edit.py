#imports
import pymysql
from connector import start_rds_connection
import questionary
import fire

#establish database connection
con = start_rds_connection()

#create cursor object
cursor = con.cursor()


#write sql query
sql_query = "SELECT employeeNumber FROM employees"

#ask for employee number
def ask_employee_number():
    cursor.execute(sql_query)
    results = cursor.fetchall()
    employee_numbers = []
    for record in results:
        employee_numbers.append(record['employeeNumber'])
    #employee = list(cursor)
    #selector = questionary.select("Please select your employee number", employee_numbers).ask()
    #return selector
    return employee_numbers

def run():
    employee_numbers = ask_employee_number()
    selector = questionary.select("Please select your employee number", employee_numbers).ask()
    return selector



# Run the main application.
if __name__ == "__main__":
    try:
        fire.Fire(run)
    except Exception as e:
        print(f"You have some error.\nError Code: {e}")