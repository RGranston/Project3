# make necessary imports
import pymysql.cursors
from config import *

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