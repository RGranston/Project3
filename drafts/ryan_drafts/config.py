import pymysql

USERNAME = 'admin'
PASSWORD = 'fintechfinalproject'
ENDPOINT = "project-database.cmlzwclsvyh6.us-west-2.rds.amazonaws.com"
PORT = 3306
REGION = "us-west-2d"
DBNAME = 'classicmodels'
SSL_CA = "./SSL/global-bundle.pem"
CURSORCLASS = pymysql.cursors.DictCursor