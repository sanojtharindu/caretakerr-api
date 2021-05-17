import os
from flask import Flask
from flask_cors import CORS
from flask_mysqldb import MySQL
import MySQLdb
from models.User import User

class Client(User):
    def __init__(self, name, email, password, phone, address, identification, clientName=None, clientAddress=None, clientBirth=None, clientGender=None, clientIdentification=None, clientConditions=None, caregiver=None, id=None, createdOn=None, updatedOn=None):
        super().__init__(name, email, password, phone, address, id, createdOn, updatedOn)
        self.identification = identification
        self.clientName = clientName
        self.clientAddress = clientAddress
        self.clientBirth = clientBirth
        self.clientGender = clientGender
        self.clientIdentification = clientIdentification
        self.clientConditions = clientConditions
        self.caregiver = caregiver

    def setClientName(self, clientName):
        self.clientName = clientName

    def getClientName(self):
        return self.clientName

    def setClientAddress(self, clientAddress):
        self.clientAddress = clientAddress
    
    def getClientAddress(self):
        return self.clientAddress
    
    def setClientBirth(self, clientBirth):
        self.clientBirth = clientBirth

    def getClientBirth(self):
        return self.clientBirth

    def setClientGender(self, clientGender):
        self.clientGender = clientGender
    
    def getClientGender(self):
        return self.clientGender

    def setClientIdentification(self, clientIdentification):
        self.clientIdentification = clientIdentification

    def getClientIdentification(self):
        return self.clientIdentification

    def setClientConditions(self, clientConditions):
        self.clientConditions = clientConditions

    def getClientConditions(self):
        return self.clientConditions

    def setCaregiver(self, caregiver):
        self.caregiver = caregiver

    def getCaregiver(self):
        return self.caregiver

    def getIdentification(self):
        return self.identification

    @staticmethod
    def getAllClients(mysql):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        
        cursor.execute('SELECT * FROM client ORDER BY id')
        clients = cursor.fetchall()

        return clients

    @staticmethod
    def getClient(client_id, mysql):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        
        cursor.execute('SELECT * FROM client WHERE id = % s',(client_id,))
        client = cursor.fetchone()

        return client

    @staticmethod
    def getPaymentInfo(client_id, mysql):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        cursor.execute('SELECT * FROM paymentInfo WHERE userId = % s', (client_id))
        paymentInfo = cursor.fetchone()

        return paymentInfo

    @staticmethod
    def addClient(client, mysql):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        cursor.execute('INSERT INTO client (caregiver, name, email, password, phone, address, identification, clientName, clientAddress, clientBirth, clientGender, clientIdentification, clientConditions) VALUES(% s, % s, % s, % s, % s, % s, % s, % s, % s, % s, % s, % s, % s)', 
        (client.getCaregiver(), client.getName(), client.getEmail(), client.getPassword(), client.getPhone(), client.getAddress(), client.getIdentification(), client.getClientName(), client.getClientAddress(), client.getClientBirth(), client.getClientGender(), client.getClientIdentification(), client.getClientConditions(),))
        mysql.connection.commit()

        # client_id = cursor.lastrowid

        return True

    @staticmethod
    def updateClient(client_id, client, mysql):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        cursor.execute('UPDATE client SET clientName = % s, clientAddress = % s, clientBirth = % s, clientGender = % s, clientIdentification = % s, clientConditions = % s, caregiver = % s WHERE id = % s',
        (client.getClientName(), client.getClientAddress(), client.getClientBirth(), client.getClientGender(), client.getClientIdentification, client.getClientConditions, client.getCaregiver(), client_id,))
        mysql.connection.commit()

        return True

    @staticmethod
    def assignCaretaker(client_id, caretaker_id, mysql):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        cursor.execute('UPDATE client SET caregiver = % s WHERE id = % s',
        (caretaker_id, client_id,))
        mysql.connection.commit()

        return True
    
    @staticmethod
    def unassignCaretaker(client_id,  mysql):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        cursor.execute('UPDATE client SET caregiver = % s WHERE id = % s',
        (None, client_id,))
        mysql.connection.commit()

        return True

    @staticmethod
    def updatePaymentInfo(client_id, cardholdername, cardnumber, cvv, expiryDate, mysql):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        cursor.execute('UPDATE paymentInfo SET cardHolderName = % s, cardNumber = % s, expiryDate = % s, cvv = % s WHERE userId = % s', (cardholdername, cardNumber, expiryDate, cvv, client_id))
        mysql.connection.commit()

        return True
    
    @staticmethod
    def deleteClient(client_id, mysql):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        cursor.execute('DELETE FROM client WHERE id = % s', (client_id,))
        mysql.connection.commit()

        return True

    @staticmethod
    def login(email, password, mysql):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        cursor.execute('SELECT email,identification,id,name,phone,address,caregiver,clientAddress,clientBirth,clientConditions,clientGender,clientIdentification,clientName,createdOn,updatedOn FROM client WHERE email = % s AND password = % s', (email, password,))
        user = cursor.fetchone()

        return user