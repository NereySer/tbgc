import os
import psycopg2

DATABASE_URL = os.environ['DATABASE_URL']

conn = psycopg2.connect(DATABASE_URL) #, sslmode='require')
conn.set_session(autocommit=True)

cur = conn.cursor()

print("Информация о сервере PostgreSQL")
print(conn.get_dsn_parameters(), "\n")
# Выполнение SQL-запроса
cur.execute("SELECT version();")
# Получить результат
record = cur.fetchone()
print("Вы подключены к - ", record, "\n")




cur.execute("SELECT COUNT(table_name) FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = 'public';")
tables_count = cur.fetchone()[0]

print("Tables count: "+str(tables_count))

if tables_count == 0:
    sql = open('init.sql').read()

    cur.execute(sql)




#cur.execute("CREATE TABLE config (key varchar PRIMARY KEY, value varchar);")
#conn.commit()

cur.close()
conn.close()



