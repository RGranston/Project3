import pymysql

USERNAME = "<username>"
PASSWORD = "<password>"
ENDPOINT = "<endpoint>"
PORT = 3306
REGION = "us-west-2d"
DBNAME = "<dbname>"
SSL_CA = "./SSL/global-bundle.pem"
CURSORCLASS = pymysql.cursors.DictCursor