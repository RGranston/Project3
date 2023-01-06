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
sql_query = "SELECT employeeNumber from employees"

        


#ask for employee number
def ask_employee_number():
    cursor.execute(sql_query)
    employee = list(cursor)
    selector = questionary.select("Please select your employee number", employee).ask()
    return selector

def run():
    employee_number = ask_employee_number()
    print(f"{employee_number}")



# Run the main application.
if __name__ == "__main__":
    try:
        fire.Fire(run)
    except Exception as e:
        print(f"You have some error.\nError Code: {e}")