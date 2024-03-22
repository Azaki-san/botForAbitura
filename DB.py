import sqlite3

class WorkingWithDB:

    def __init__(self):
        self.cursor, self.connection = self.connect_to_database()

    def connect_to_database(self):
        connection = sqlite3.connect("database.db", check_same_thread=False)
        cursor = connection.cursor()
        return cursor, connection

    def checkRegister(self, id):
        self.cursor.execute("SELECT * FROM data WHERE ID = ?", (id,))
        res = self.cursor.fetchone()
        return res

    def checkNameSurname(self, name, surname):
        self.cursor.execute("SELECT * FROM data WHERE Name = ? AND Surname = ?", (name.lower(), surname.lower(),))
        return self.cursor.fetchone()

    def register(self, id, name, surname, alias):
        try:
            self.cursor.execute("INSERT INTO data (ID, Name, Surname, Alias) VALUES (?, ?, ?, ?)", (id, name.lower(),
                                                                                                    surname.lower(),
                                                                                                    alias,))
            self.connection.commit()
            return 1
        except Exception:
            return 0

    def addSelectionNames(self, NAMES):
        try:
            for i in NAMES:
                self.cursor.execute("INSERT INTO NAMES (Name, Surname) VALUES (?, ?)", (i[0], i[1],))
                self.connection.commit()
            return 1
        except Exception:
            return 0

    def getLink(self):
        self.cursor.execute("SELECT link FROM link WHERE id = 0")
        return self.cursor.fetchone()


    def erase(self, id):
        self.cursor.execute("DELETE FROM data WHERE ID = ?", (id,))
        self.connection.commit()


    def getStatistics(self):
        self.cursor.execute("SELECT * FROM data")
        return self.cursor.fetchall()

    def getRegisteredIds(self):
        self.cursor.execute("SELECT ID FROM data")
        return self.cursor.fetchall()

    def getAllNamesOnSelection(self):
        self.cursor.execute("SELECT Name, Surname FROM NAMES")
        return self.cursor.fetchall()


dbClone = WorkingWithDB()
