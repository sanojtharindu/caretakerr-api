import os
from flask import Flask
from flask_cors import CORS
from flask_mysqldb import MySQL
import MySQLdb

class Report:
    def __init__(self, reportDesc, reportDate, reportUser=None, reportShow=None, reportFile=None, createdOn=None, id=None, updatedOn=None):
        self.reportDesc = reportDesc
        self.reportDate = reportDate
        self.reportFile = reportFile
        self.reportShow = reportShow
        self.reportUser = reportUser
        self.createdOn = createdOn
        self.id= id
        self.updatedOn = updatedOn

    def setReportDesc(self, reportDesc):
        self.reportDesc = reportDesc

    def getReportDesc(self):
        return self.reportDesc

    def setReportDate(self, reportDate):
        self.reportDate = reportDate

    def getReportDate(self):
        return self.reportDate

    def setReportFile(self, reportFile):
        self.reportFile = reportFile

    def getReportFile(self):
        return self.reportFile

    def setReportShow(self, reportShow):
        self.reportShow = reportShow

    def getReportShow(self):
        return self.reportShow

    def setId(self, id):
        self.id = id

    def getId(self):
        return self.id

    def setReportUser(self, user):
        self.reportUser = user

    def getReportUser(self):
        return self.reportUser

    def getCreatedOn(self):
        return self.createdOn

    def getUpdatedOn(self):
        return self.updatedOn

    @staticmethod
    def getAllReports(mysql):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        
        cursor.execute('SELECT * FROM report ORDER BY reportDate DESC')
        reports = cursor.fetchall()

        return reports

    @staticmethod
    def getAllReportsUser(user_id, mysql):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        
        cursor.execute('SELECT * FROM report WHERE reportUser = % s ORDER BY reportDate DESC',(user_id,))
        reports = cursor.fetchall()

        return reports

    @staticmethod
    def getReport(report_id, mysql):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        cursor.execute('SELECT * FROM report WHERE id = % s', (report_id,))
        report = cursor.fetchone()

        return report

    @staticmethod
    def addReport(report, mysql):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        cursor.execute('INSERT INTO report (reportUser, reportDesc, reportDate, reportFile) VALUES (% s, % s, % s, % s)', (report.getReportUser(), report.getReportDesc(), report.getReportDate(), report.getReportFile(),))
        mysql.connection.commit()

        return True

    @staticmethod
    def updateReport(report_id, report, mysql):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        cursor.execute('UPDATE report SET reportDesc = % s, reportDate = % s, reportFile = % s WHERE id = % s', (report.getReportDesc(), report.getReportDate(), report.getReportFile(), report_id,))
        mysql.connection.commit()

        return True

    @staticmethod
    def updateReportNoFile(report_id, report, mysql):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('UPDATE report SET reportDesc = % s, reportDate = % s WHERE id = % s', (report.getReportDesc(), report.getReportDate(), report_id,))
        mysql.connection.commit()

        return True

    @staticmethod
    def showReport(report_id, mysql):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        cursor.execute('UPDATE report SET reportShow = % s WHERE id = % s', (1, report_id,))
        mysql.connection.commit()

        return True

    @staticmethod
    def hideReport(report_id, mysql):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        cursor.execute('UPDATE report SET reportShow = % s WHERE id = % s', (0, report_id,))
        mysql.connection.commit()

        return True
        
    @staticmethod
    def deleteReport(report_id, mysql):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        cursor.execute('DELETE FROM report WHERE id = % s', (report_id,))
        mysql.connection.commit()

        return True
    