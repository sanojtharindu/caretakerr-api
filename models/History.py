import os
from flask import Flask
from flask_cors import CORS
from flask_mysqldb import MySQL
import MySQLdb

class History:
    def __init__(self, client_id, caretaker_id, assigned_date=None, removed_date=None, notes=None, id=None):
        self.client_id = client_id
        self.caretaker_id = caretaker_id
        self.assigned_date = assigned_date
        self.removed_date = removed_date
        self.id = id
        self.notes = notes

    def setClientId(self, client_id):
        self.client_id = client_id

    def getClientId(self):
        return self.client_id

    def setCaretakerId(self, caretaker_id):
        self.caretaker_id = caretaker_id

    def getCaretakerId(self):
        return self.caretaker_id

    def setAssignedDate(self, assigned_date):
        self.assigned_date = assigned_date

    def getAssignedDate(self):
        return self.assigned_date

    def setRemovedDate(self, removed_date):
        self.removed_date = removed_date

    def getRemovedDate(self):
        return self.removed_date

    def setId(self, id):
        self.id = id

    def getId(self):
        return self.id
    
    def setNotes(self, notes):
        self.notes = notes

    def getNotes(self):
        return self.notes

    @staticmethod
    def getAllHistory(mysql):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        cursor.execute('SELECT * FROM history ORDER BY id DESC')
        history = cursor.fetchall()

        return history

    @staticmethod
    def getAllHistoryClient(client_id, mysql):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        cursor.execute('SELECT * FROM history WHERE client_id = % s ORDER BY id DESC', (client_id,))
        history = cursor.fetchall()

        return history

    @staticmethod
    def getAllHistoryCaretaker(caretaker_id, mysql):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        cursor.execute('SELECT * FROM history WHERE caretaker_id = % s ORDER BY id DESC', (caretaker_id,))
        history = cursor.fetchall()

        return history

    @staticmethod
    def getIndividualHistory(id, mysql):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        cursor.execute('SELECT * FROM history WHERE id = % s', (id,))
        history = cursor.fetchone()

        return history

    @staticmethod
    def getRecentHistory(client_id, caretaker_id, mysql):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        cursor.execute('SELECT * FROM history WHERE client_id = % s AND caretaker_id = % s ORDER BY id DESC LIMIT 1')

        return cursor.fetchone()

    @staticmethod
    def addHistory(history, mysql):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        cursor.execute('INSERT INTO history (client_id, caretaker_id, notes) VALUES(% s, % s, % s)', (history.getClientId(), history.getCaretakerId(), history.getNotes(), ))
        mysql.connection.commit()

        return True

    @staticmethod
    def updateHistoryRemoved(history_id, removed_date, mysql):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        cursor.execute('UPDATE history SET removed_date = % s WHERE id = % s', 
        (removed_date, history_id,))
        mysql.connection.commit()

        return True
    
    @staticmethod
    def updateHistoryNotes(history_id, notes, mysql):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        cursor.execute('UPDATE history SET notes = % s WHERE id = % s', 
        (notes, history_id,))
        mysql.connection.commit()

        return True

    @staticmethod
    def deleteHistory(history_id, mysql):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        cursor.execute('DELETE FROM history WHERE id = % s', (history_id,))
        mysql.connection.commit()

        return True