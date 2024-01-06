from application import app
from flask_mysqldb import MySQL

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'qaz$02pm'
app.config['MYSQL_DB'] = 'timemanagementsys'

mysql = MySQL(app)
