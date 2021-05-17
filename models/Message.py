import os
from flask import Flask
from flask_cors import CORS
from flask_mysqldb import MySQL
import MySQLdb
from models.User import User

class Message():
    def __init__(self, client, caretaker, messages, sender, date, id=None, createdOn=None, updatedOn=None):
        self.client = client
        self.caretaker = caretaker
        self.messages = messages
        self.sender = sender
        self.date = date
        self.id = id
        self.createdOn = createdOn
        self.updatedOn = updatedOn

    def setClient(self, client):
        self.client = client

    def getClient(self):
        return self.client

    def setCaretaker(self, caretaker):
        self.caretaker = caretaker

    def getCaretaker(self):
        return self.caretaker

    def setMessage(self, messages):
        self.messages = messages

    def getMessage(self):
        return self.messages

    def setSender(self, sender):
        self.sender = sender

    def getSender(self):
        return self.sender

    def setDate(self, date):
        self.date = date

    def getDate(self):
        return self.date

    def setId(self, id):
        self.id = id

    def getId(self):
        return self.id

    def setCreatedOn(self, createdOn):
        self.createdOn = createdOn

    def getCreatedOn(self):
        return self.createdOn

    def setUpdatedOn(self, updatedOn):
        self.updatedOn = updatedOn

    def getUpdatedOn(self):
        return self.updatedOn

    @staticmethod
    def getAllMessages(mysql):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM message")
        messages= cursor.fetchall()

        return messages
    
    @staticmethod
    def getMessages(clientId, caretakerId, mysql):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        cursor.execute("SELECT * FROM message WHERE clientId = % s AND caretakerId = % s", (clientId, caretakerId, ))
        messages = cursor.fetchall()

        return messages

    @staticmethod
    def addMessages(message, mysql):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        cursor.execute("INSERT INTO message (clientId, caretakerId, messages, sender, date) VALUES(% s, % s, % s, % s, % s)", (message.getClient(), message.getCaretaker(), message.getMessage(), message.getSender(), message.getDate(), ))
        mysql.connection.commit()

        return True

    @staticmethod
    def updateMessages(message, mysql):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        cursor.execute("UPDATE message SET messages = % s, sender = % s, date = % s WHERE id = % s", (message.getMessage(), message.getSender(), message.getDate(), id, ))
        mysql.connection.commit()

        return True

    @staticmethod
    def updateMessagesByUser(message, mysql):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        cursor.execute("UPDATE message SET messages = % s, sender = % s, date = % s WHERE clientId = % s AND caretakerId = % s", (message.getMessage(), message.getSender(), message.getDate(), message.getClient(), message.getCaretaker(), ))
        mysql.connection.commit()

        return True

    @staticmethod
    def deleteMessage(id, mysql):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        cursor.execute("DELETE FROM message WHERE id = % s", (id,))
        mysql.connection.commit()

        return True

    @staticmethod
    def deleteMessageByUser(clientId, caretakerId, mysql):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        cursor.execute("DELETE FROM message WHERE clientId = % s AND caretakerId = % s", (clientId, caretakerId, ))
        mysql.connection.commit()

        return True

