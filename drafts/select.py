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
sql_query = (f"SELECT employeeNumber, lastname, customer number, checkNumber, paymentDate, amount FROM employees LEFT JOIN payments ON employeeNumber = salesRepEmployeeNumber LEFT JOIN payments ON payments.customerNumber = customers.customerNumber WHERE employeeNymber = {selector} ORDERD BY paymentDate;")

        


#ask for employee number
def ask_employee_number():
    selector = questionary.text("Please select your employee number.").ask()
    return selector

def run():
    selector = ask_employee_number()
    try: 
        cursor.execute(sql_query)
        results = cursor.fetchall()

        for record in results:
            employee_number = record['employeeNumber']
            last_name = record['lastName']
            customer_name = record['customerName']
            check_number = record['checkNumber']
            payment_date = record['paymentDate']
            amount = record['amount']
            print(f"Employee Number: {employee_number}, Last Name: {last_name}, Customer Name: {customer_name}, Check Number: {check_number}, Payment Date: {payment_date}, Amount: {amount}")

    except Exception as e:
        print(f"Exception occurred: {e}")

# Run the main application.
if __name__ == "__main__":
    try:
        fire.Fire(run)
    except Exception as e:
        print(f"You have some error.\nError Code: {e}")