import mysql.connector as mysql


class RespondDB:
    # colect all responses for dialogflow project

    def __init__(self, column1, table, column2):

        self.column1 = column1
        self.table = table
        self.column2 = column2

    def get_db_info(self, value):

        # cofiguration to databese
        db = mysql.connect(host="*********",
                           user="***********",
                           passwd="*************",
                           database="**********"
                           )

        cursor = db.cursor()
        # defining the Query
        query = "SELECT {0} FROM {1} WHERE {2} = {3}".format(self.column1,
                                                             self.table,
                                                             self.column2,
                                                             value)
        # getting item from column from the table
        cursor.execute(query)
        # fetching all usernames from the 'cursor' object
        items = cursor.fetchall()
        db.close()
        # showing the data
        for item in items:
            return item
