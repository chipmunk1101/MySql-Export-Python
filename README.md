MySql-Export-Python
===================

If you are a Django-Mysql user you know the pain of using South to migrate. This program exports MySql a database based on the dependency of the tables within the database. You can just dump the database and import back without pain after syncdb(for django)


Requirements
===================

Python 2.7 or above

MySQLdb for python 



Usage
===================
Edit the following:

user = "your username"

passwd = "your password"

db = "your database name" 


Output
===================
The resultant file will be stored in your HOME path with the name backup.sql

Performance
===================
This code runs in O(n^3) but that is asymptotic, so unless you have a very very very large number of tables(not data, tables) you don't have to worry. I m also trying to improve.
