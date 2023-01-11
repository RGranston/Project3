# make necessary imports
import pymysql.cursors
## config import *

# Configuration parameters (ideally to be placed in separate config.py file)
PORT = 3306
DBNAME = 'classicmodels'
USERNAME = 'admin'
ENDPOINT = "project-database.cmlzwclsvyh6.us-west-2.rds.amazonaws.com"
PASSWORD = 'fintechfinalproject'
CURSORCLASS = pymysql.cursors.DictCursor
SSL_CA = "SSL/global-bundle.pem"
# define function to establish RDS connection
def start_rds_connection():
    try:
        connection = pymysql.connect(host=ENDPOINT,
                                    port=PORT,
                                    user=USERNAME,
                                    passwd=PASSWORD,
                                    db=DBNAME,
                                    cursorclass=CURSORCLASS,
                                    ssl_ca=SSL_CA)
        print('[+] RDS Connection Successful')

    except Exception as e:
        print(f'[+] RDS Connection Failed: {e}')
        connection = None

    return connection