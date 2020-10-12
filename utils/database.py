import sqlite3 as sl

class Database():
    def __init__(self):
        self.database = sl.connect('database.db')
        self.database.execute("""
            CREATE TABLE IF NOT EXISTS MATERIAL (
                nome TEXT,
                rho INTEGER,
                E FLOAT
        );
    """)


 #   def materials_db(self):
 #       dummy_material = {'E': 200e9, 'rho':1e3, 'nome': 'Dummy'}
 #       sql = 'INSERT INTO MATERIAL (nome, rho, E) values(?, ?, ?)'
 #       data = [
 #           (dummy_material['nome'], dummy_material['rho'], dummy_material['E']),
 #       ]#
#
#        with self.database:
#            self.database.executemany(sql, data)

    def showContent(self):
        print('Mostrar conteudo do db')
        with self.database:
            data = self.database.execute("SELECT * FROM MATERIAL")
            for row in data:
                print(row)

    def getContent(self):
        with self.database:
            data = self.database.execute("SELECT * FROM MATERIAL")
            return data

if __name__ == '__main__':
    # Comandos de teste para desenvolver este modulo


    db = Database()