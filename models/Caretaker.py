import os
from flask import Flask
from flask_cors import CORS
from flask_mysqldb import MySQL
import MySQLdb
from models.User import User

class Caretaker(User):
    def __init__(self, name, email, password, phone, address, occupation, birthDate, identification, availableHours, availableDays, experience=None, status=1, user=None, id=None, createdOn=None, updatedOn=None):
        super().__init__(name, email, password, phone, address, id, createdOn, updatedOn)
        self.occupation = occupation
        self.birthDate = birthDate
        self.identification = identification
        self.availableHours = availableHours
        self.availableDays = availableDays
        self.experience = experience
        self.status = status
        self.user = user
        self.experience = experience

    def setOccupation(self, occupation):
        self.occupation = occupation

    def getOccupation(self):
        return self.occupation

    def setBirthDate(self, birthDate):
        self.birthDate = birthDate

    def getBirthDate(self):
        return self.birthDate

    def setIdentification(self, identification):
        self.identification = identification

    def getIdentification(self):
        return self.identification

    def setAvailableHours(self, availableHours):
        self.availableHours = availableHours

    def getAvailableHours(self):
        return self.availableHours

    def setAvailableDays(self, availableDays):
        self.availableDays = availableDays

    def getAvailableDays(self):
        return self.availableDays

    def setExperience(self, experience):
        self.experience = experience

    def getExperience(self):
        return self.experience

    def setStatus(self, status):
        self.status = status

    def getStatus(self):
        return self.status

    def setUser(self, user):
        self.user = user

    def getUser(self):
        return self.user

    def setExperience(self, experience):
        self.experience = experience

    def getExperience(self):
        return self.experience

    @staticmethod
    def getAllCaretakers(mysql):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        
        cursor.execute('SELECT * FROM caretaker ORDER BY id')
        caretakers = cursor.fetchall()

        return caretakers

    @staticmethod
    def getTopCaretakers(mysql):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        cursor.execute('SELECT * FROM caretaker ORDER BY createdOn DESC LIMIT 5')
        caretakers = cursor.fetchall()

        return caretakers

    @staticmethod
    def getUnassignedCaretakers(mysql):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        cursor.execute('SELECT * FROM caretaker WHERE user IS NULL ORDER BY createdOn DESC')
        caretakers = cursor.fetchall()

        return caretakers

    @staticmethod
    def getCaretaker(caretaker_id, mysql):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        
        cursor.execute('SELECT * FROM caretaker WHERE id = % s',(caretaker_id,))
        caretaker = cursor.fetchone()

        return caretaker

    @staticmethod
    def addCaretaker(caretaker, mysql):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        cursor.execute('INSERT INTO caretaker (name, email, password, phone, address, occupation, birthDate, identification, availableHours, availableDays, experience, status, user) VALUES(% s, % s, % s, % s, % s, % s, % s, % s, % s, % s, % s, % s, % s)', 
        (caretaker.getName(), caretaker.getEmail(), caretaker.getPassword(), caretaker.getPhone(), caretaker.getAddress(), caretaker.getOccupation(), caretaker.getBirthDate(), caretaker.getIdentification(), caretaker.getAvailableHours(), caretaker.getAvailableDays(), caretaker.getExperience(), caretaker.getStatus(), caretaker.getUser(),))
        mysql.connection.commit()
        
        return True

    @staticmethod
    def updateCaretaker(caretaker_id, caretaker, mysql):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        if (caretaker.getExperience() == None):
            cursor.execute('UPDATE caretaker SET name = % s, email = % s, password = % s, phone = % s, address = % s, occupation = % s, birthDate = % s, identification = % s, availableHours = % s, availableDays = % s WHERE id = % s',
            (caretaker.getName(), caretaker.getEmail(), caretaker.getPassword(), caretaker.getPhone(), caretaker.getAddress(), caretaker.getOccupation(), caretaker.getBirthDate(), caretaker.getIdentification(), caretaker.getAvailableHours(), caretaker.getAvailableDays(), caretaker_id,))
            mysql.connection.commit()
        else:
            cursor.execute('UPDATE caretaker SET name = % s, email = % s, password = % s, phone = % s, address = % s, occupation = % s, birthDate = % s, identification = % s, availableHours = % s, availableDays = % s, experience = % s WHERE id = % s',
            (caretaker.getName(), caretaker.getEmail(), caretaker.getPassword(), caretaker.getPhone(), caretaker.getAddress(), caretaker.getOccupation(), caretaker.getBirthDate(), caretaker.getIdentification(), caretaker.getAvailableHours(), caretaker.getAvailableDays(), caretaker.getExperience(), caretaker_id,))
            mysql.connection.commit()

        return True

    @staticmethod
    def assignClient(caretaker_id, client_id, mysql):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('UPDATE caretaker SET user = % s WHERE id = % s', (client_id, caretaker_id,))
        mysql.connection.commit()

        return True
    
    @staticmethod
    def unassignClient(caretaker_id, mysql):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('UPDATE caretaker SET user = % s WHERE id = % s', (None, caretaker_id,))
        mysql.connection.commit()

        return True
    
    @staticmethod
    def activeCaretaker(caretaker_id, mysql):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        cursor.execute('UPDATE caretaker SET status = % s WHERE id = % s', (1, caretaker_id,))
        mysql.connection.commit()

        return True

    @staticmethod
    def inactiveCaretaker(caretaker_id, mysql):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        cursor.execute('UPDATE caretaker SET status = % s WHERE id = % s', (0, caretaker_id))
        mysql.connection.commit()

        return True
    
    @staticmethod
    def deleteCaretaker(caretaker_id, mysql):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        cursor.execute('DELETE FROM caretaker WHERE id = % s', (caretaker_id,))
        mysql.connection.commit()

        return True

    @staticmethod
    def login(email, password, mysql):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        cursor.execute('SELECT address,availableDays,availableHours,birthDate,createdOn,email,id,identification,name,occupation,phone,status,updatedOn,user FROM caretaker WHERE email = % s AND password = % s', (email, password,))
        user = cursor.fetchone()

        return user