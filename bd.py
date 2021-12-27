import mysql.connector

class database:
    def __init__(self):
        self.connection = mysql.connector.connect(host="localhost", user="root", passwd="", database="maia")

        self.cursor = self.connection.cursor()

    def query(self, query, executar=False):
        """
        executa uma query e retorna seu resultado
        """
        self.cursor.execute(query)
        
        if executar:
            self.connection.commit()
        
        return list(list(self.cursor))