import mysql.connector as mysql

class Db:
     def __init__(self, column1, table, column2, value):

        self.column1 = column1
        self.column2 = column2
        self.table = table
        self.value = value

        db = mysql.connect(
            host="***",
            user="***",
            passwd="***",
            database="***"
        )
        cursor = db.cursor()
        query = 'SELECT {} from {} WHERE {} = {}'.format(column1, table, column2, value)
        cursor.execute(query)
        records = cursor.fetchall()
        db.close()
        for self.record in records:
            return self.record

db_obj = Db('typProjektu', 'TypyProjektow', 'dzialanie_id', '2.1')


print(db_obj)
