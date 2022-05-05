import os
import psycopg2

db_conn = None
db_cur = None

def initCursor():
    global db_conn, db_cur
    
    if db_conn is None:
        db_cur = None
        
        DATABASE_URL = os.getenv('DATABASE_URL')
    
        db_conn = psycopg2.connect(DATABASE_URL) #, sslmode='require')
        db_conn.set_session(autocommit=True)
    
    if db_cur is None:
        db_cur = db_conn.cursor()
        
def testDB():
    initCursor()
    
    print("Информация о сервере PostgreSQL")
    print(conn.get_dsn_parameters(), "\n")
    # Выполнение SQL-запроса
    db_cur.execute("SELECT version();")
    # Получить результат
    record = db_cur.fetchone()
    print("Вы подключены к - ", record, "\n")

    db_cur.execute("SELECT COUNT(table_name) FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = 'public';")
    tables_count = db_cur.fetchone()[0]

    print("Tables count: "+str(tables_count))

    if tables_count == 0:
        sql = open('tools/init.sql').read()

        db_cur.execute(sql)

#cur.execute("CREATE TABLE config (key varchar PRIMARY KEY, value varchar);")
#conn.commit()

def closeDB():
    if db_cur is not None: 
        db_cur.close()
        
    if db_conn is not None:
        db_conn.close()
