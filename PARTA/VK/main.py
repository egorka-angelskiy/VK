from class_vk import *
from class_db import *


db = PostgreDB()
db.connect_db(DBCONNECT)
#db.select()
#db.cursor.execute("SELECT tablename FROM pg_tables where schemaname='public';")
#print(db.cursor.fetchone())