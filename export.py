import MySQLdb
import os, sys
import datetime
from collections import OrderedDict

user = 'root'
passwd = ''
db = 'pollmaster'


con = MySQLdb.connect(host='localhost', user=user, passwd=passwd, db=db)
cur = con.cursor()

cur.execute("SHOW TABLES")
data = ""


graph = {}                
tables = []

for table in cur.fetchall():
    graph[table[0]] = []


cur.execute("SELECT table_name, referenced_table_name\
                AS list_of_fks FROM INFORMATION_SCHEMA.key_column_usage\
                    WHERE referenced_table_schema = '"+ db + "'\
                        AND referenced_table_name \
                            IS NOT NULL ORDER BY table_name, column_name;")

for table in cur.fetchall():
    if table[1] not in graph[table[0]]:
        graph[table[0]].append(table[1])

graph = OrderedDict(sorted(graph.viewitems(), key=lambda x: len(x[1])))

for item in graph:
    print str(item) + ":" + str(graph[item])

while len(graph) > 0:
    for item in graph:
        if len(graph[item]) == 0:
            tables.append(item)
            dependent_tables = [key for key, value in graph.iteritems() if item \
                                in value]
            if dependent_tables:
                for table in dependent_tables:
                    graph[table].remove(item)
            del graph[item]

    graph = OrderedDict(sorted(graph.viewitems(), key=lambda x: len(x[1])))
   
for table in tables:
    cur.execute("SHOW CREATE TABLE `" + str(table) + "`;")
    table_details = str(cur.fetchone()[1]).replace("CREATE TABLE",\
                                                   "CREATE TABLE IF NOT EXISTS")
    data += "\n" + table_details + ";\n\n"

    cur.execute("SELECT * FROM `" + str(table) + "`;")
    for row in cur.fetchall():
        data += "INSERT IGNORE INTO`" + str(table) + "` VALUES("
        first = True
        for field in row:
            if not first:
                data += ', '
            data += '"' + str(field).replace("\"", "'") + '"'
            first = False


        data += ");\n"
    data += "\n\n"
    
#print data
now = datetime.datetime.now()
filename = str(os.getenv("HOME")) + "/backup.sql"

print "\nFile:" + filename

FILE = open(filename,"w")
FILE.writelines(data)
FILE.close()
