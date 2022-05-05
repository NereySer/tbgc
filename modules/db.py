import os
import psycopg2

db_conn = None, db_cur = None

def getCursor():
    global db_conn, db_cur
    
    if db_conn is None:
        db_cur = None
        
        DATABASE_URL = os.getenv['DATABASE_URL']
    
        db_conn = psycopg2.connect(DATABASE_URL) #, sslmode='require')
        db_conn.set_session(autocommit=True)
    
    if db_cur is None:
        cur = conn.cursor()
        
def testDB():
    cur = getCursor()
    
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
        sql = open('tools/init.sql').read()

        cur.execute(sql)

#cur.execute("CREATE TABLE config (key varchar PRIMARY KEY, value varchar);")
#conn.commit()

def closeDB()
    db_cur.close()
    db_conn.close()
