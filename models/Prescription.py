import os
from flask import Flask
from flask_cors import CORS
from flask_mysqldb import MySQL
import MySQLdb

class Prescription:
    def __init__(self, prescDesc, prescDate, prescFreq, prescUser=None, prescAuto=1, prescPending=None, prescFile=None, prescPrice=None, id=None, createdOn=None, updatedOn=None):
        self.prescDesc = prescDesc
        self.prescDate = prescDate
        self.prescFreq = prescFreq
        self.prescFile = prescFile
        self.prescAuto = prescAuto
        self.prescPending = prescPending
        self.prescUser = prescUser
        self.prescPrice = prescPrice
        self.id = id
        self.createdOn = createdOn
        self.updatedOn = updatedOn

    def setPrescDesc(self, prescDesc):
        self.prescDesc = prescDesc

    def getPrescDesc(self):
        return self.prescDesc

    def setPrescDate(self, prescDate):
        self.prescDate = prescDate

    def getPrescDate(self):
        return self.prescDate

    def setPrescFreq(self, prescFreq):
        self.prescFreq = prescFreq

    def getPrescFreq(self):
        return self.prescFreq

    def setPrescFile(self, prescFile):
        self.prescFile = prescFile

    def getPrescFile(self):
        return self.prescFile

    def setPrescAuto(self, prescAuto):
        self.prescAuto = prescAuto

    def getPrescAuto(self):
        return self.prescAuto

    def setPrescPending(self, prescPending):
        self.prescPending = prescPending

    def getPrescPending(self):
        return self.prescPending

    def setPrescUser(self, prescUser):
        self.prescUser = prescUser

    def getPrescUser(self):
        return self.prescUser

    def setPrescPrice(self, prescPrice):
        self.prescPrice = prescPrice

    def getPrescPrice(self):
        return self.prescPrice

    def setId(self, id):
        self.id = id

    def getId(self):
        return self.id

    def getCreatedOn(self):
        return self.createdOn

    def getUpdatedOn(self):
        return self.updatedOn

    @staticmethod
    def getAllPrescriptions(mysql):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        
        cursor.execute('SELECT * FROM prescription ORDER BY id')
        prescriptions = cursor.fetchall()

        return prescriptions

    @staticmethod
    def getAllPrescriptionsUser(user_id, mysql):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        
        cursor.execute('SELECT * FROM prescription WHERE prescUser = % s ORDER BY createdOn ASC',(user_id,))
        prescriptions = cursor.fetchall()

        return prescriptions
        
    @staticmethod
    def getPrescription(presc_id, mysql):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        cursor.execute('SELECT * FROM prescription WHERE id = % s', (presc_id,))
        prescription = cursor.fetchone()

        return prescription

    @staticmethod
    def addPrescription(prescription, mysql):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        cursor.execute('INSERT INTO prescription (prescUser, prescDesc, prescDate, prescFreq, prescFile) VALUES(% s, % s, % s, % s, % s)', 
        (prescription.getPrescUser(), prescription.getPrescDesc(), prescription.getPrescDate(), prescription.getPrescFreq(), prescription.getPrescFile(),))
        mysql.connection.commit()

        return True

    @staticmethod
    def updatePrescription(presc_id, prescription, mysql):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        cursor.execute('UPDATE prescription SET prescDesc = % s, prescDate = % s, prescFreq = % s WHERE id = % s',
        (prescription.getPrescDesc(), prescription.getPrescDate(), prescription.getPrescFreq(), presc_id,))
        mysql.connection.commit()

        return True

    @staticmethod
    def updatePrescriptionImage(presc_id, prescription, mysql):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        cursor.execute('UPDATE prescription SET prescDesc = % s, prescDate = % s, prescFreq = % s, prescFile = % s WHERE id = % s',
        (prescription.getPrescDesc(), prescription.getPrescDate(), prescription.getPrescFreq(), prescription.getPrescFile(), presc_id,))
        mysql.connection.commit()

        return True

    @staticmethod
    def updatePrescriptionAutoOn(presc_id, mysql):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('UPDATE prescription SET prescAuto = % s WHERE id = % s',(1,presc_id))
        mysql.connection.commit()

        return True

    @staticmethod
    def updatePrescriptionAutoOff(presc_id, mysql):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('UPDATE prescription SET prescAuto = % s WHERE id = % s',(0,presc_id))
        mysql.connection.commit()

        return True

    @staticmethod
    def updatePrescriptionPrice(presc_id, prescPrice, mysql):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        cursor.execute('UPDATE prescription SET prescPending = % s, prescPrice = % s WHERE id = % s',(1, prescPrice, presc_id,))
        mysql.connection.commit()

        return True

    @staticmethod
    def deletePrescription(presc_id, mysql):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        cursor.execute('DELETE FROM prescription WHERE id = % s', (presc_id,))
        mysql.connection.commit()

        return True