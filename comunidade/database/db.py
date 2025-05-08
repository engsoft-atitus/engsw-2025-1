import sqlite3
class Db:

    def __init__(self, db_name):
        self.db_name = db_name
        # Conectando o database
        self.connection = sqlite3.connect(db_name, check_same_thread=False)
        self.__setup_tables()

    def __setup_tables(self):
        cursor = self.connection.cursor()
        # Criando a tabela caso ela não exista
        cursor.execute('''
            CREATE TABLE  IF NOT EXISTS bola_community(
        	    id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome_tag TEXT UNIQUE,
                nome TEXT,
                sobre TEXT
           )''')


        return 0