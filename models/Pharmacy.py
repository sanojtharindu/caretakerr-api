import os
from flask import Flask
from flask_cors import CORS
from flask_mysqldb import MySQL
import MySQLdb
from models.User import User

class Pharmacy(User):
    def __init__(self, name, code, email, phone, address, openHours, available, license=None, password=None, id=None, createdOn=None, updatedOn=None):
        super().__init__(name, email, password, phone, address, id, createdOn, updatedOn)
        self.code = code
        self.license = license
        self.openHours = openHours
        self.available = available

    def setCode(self, code):
        self.code = code

    def getCode(self):
        return self.code
    
    def setLicense(self, license):
        self.license = license

    def getLicense(self):
        return self.license

    def setOpenHours(self, openHours):
        self.openHours = openHours

    def getOpenHours(self):
        return self.openHours

    def setAvailable(self, available):
        self.available = available

    def getAvailable(self):
        return self.available

    @staticmethod
    def getAllPharmacies(mysql):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        
        cursor.execute('SELECT * FROM pharmacy ORDER BY id')
        pharmacies = cursor.fetchall()

        return pharmacies

    @staticmethod
    def getPharmacy(pharmacy_id, mysql):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        
        cursor.execute('SELECT * FROM pharmacy WHERE id = % s',(pharmacy_id,))
        pharmacy = cursor.fetchone()

        return pharmacy

    @staticmethod
    def addPharmacy(pharmacy, mysql):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        cursor.execute('INSERT INTO pharmacy (name, code, email, password, phone, address, license, openHours) VALUES(% s, % s, % s, % s, % s, % s, % s, % s)', 
        (pharmacy.getName(), pharmacy.getCode(), pharmacy.getEmail(), pharmacy.getPassword(), pharmacy.getPhone(), pharmacy.getAddress(), pharmacy.getLicense(), pharmacy.getOpenHours(),))
        mysql.connection.commit()

        return True

    @staticmethod
    def updatePharmacy(pharmacy_id, pharmacy, mysql):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        if pharmacy.getLicense() is not None:
            cursor.execute('UPDATE pharmacy SET name = % s, code = % s, email = % s, phone = % s, address = % s, license = % s, openhours = % s, available = % s WHERE id= % s',
            (pharmacy.getName(), pharmacy.getCode(), pharmacy.getEmail(), pharmacy.getPhone(), pharmacy.getAddress(), pharmacy.getLicense(), pharmacy.getOpenHours(), pharmacy.getAvailable(), pharmacy_id,))
            mysql.connection.commit()
        else:
            cursor.execute('UPDATE pharmacy SET name = % s, code = % s, email = % s, phone = % s, address = % s, openhours = % s, available = % s WHERE id= % s',
            (pharmacy.getName(), pharmacy.getCode(), pharmacy.getEmail(), pharmacy.getPhone(), pharmacy.getAddress(), pharmacy.getOpenHours(), pharmacy.getAvailable(), pharmacy_id,))
            mysql.connection.commit()

        return True

    @staticmethod
    def makeAvailable(pharmacy_id, mysql):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        cursor.execute('UPDATE pharmacy SET available = %s WHERE id = % s', (1, pharmacy_id,))
        mysql.connection.commit()

        return True
        
    @staticmethod
    def makeUnavailable(pharmacy_id, mysql):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        cursor.execute('UPDATE pharmacy SET available = %s WHERE id = % s', (0, pharmacy_id,))
        mysql.connection.commit()

        return True
    
    @staticmethod
    def deletePharmacy(pharmacy_id, mysql):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        cursor.execute('DELETE FROM pharmacy WHERE id = % s', (pharmacy_id,))
        mysql.connection.commit()

        return True