import psycopg2
import csv


conn = psycopg2.connect(
    dbname="backtester",
    user="postgres",
    password="mazen123",
    host="localhost",
    port="5432"
)
cur = conn.cursor()

with open('aapl_stock_data.csv', 'r') as f:
    next(f)  
    cur.copy_from(f, 'prices', sep=',', columns=('date', 'close'))


conn.commit()
cur.close()
conn.close()

print("Data loaded successfully!")
