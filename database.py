from psycopg2 import pool
from config import database

try:
	params = database()
	print('Connecting to the PostgreSQL database...')
	db_pool = pool.SimpleConnectionPool(**params)
	conn = db_pool.getconn()
	cursor = conn.cursor()
	cursor.execute("CREATE TABLE IF NOT EXISTS conversations (sessionID INT PRIMARY KEY,conv TEXT);")
except (Exception) as error:
	print(error)
def close():
		try:
			cursor.close()
			conn.close()
			print("database connection closed")
		except (Exception) as error:
			print(error)
			if conn is not None:
				conn.close()
				print('Database connection closed.')
