import os
from flask import Flask
from flask_cors import CORS
from flask_mysqldb import MySQL
import MySQLdb

class Task:
    def __init__(self, title, description, startTime, endTime, date, status, user=None, id=None, createdOn=None, updatedOn=None):
        self.title = title
        self.description = description
        self.startTime = startTime
        self.endTime = endTime
        self.date = date
        self.status = status
        self.user = user
        self.id = id
        self.createdOn = createdOn
        self.updatedOn = updatedOn

    def setTitle(self, title):
        self.title = title

    def getTitle(self):
        return self.title

    def setDescription(self, description):
        self.description = description

    def getDescription(self):
        return self.description

    def setStartTime(self, startTime):
        self.startTime = startTime

    def getStartTime(self):
        return self.startTime

    def setEndTime(self, endTime):
        self.endTime = endTime

    def getEndTime(self):
        return self.endTime
    
    def setDate(self, date):
        self.date = date

    def getDate(self):
        return self.date

    def setStatus(self, status):
        self.status = status

    def getStatus(self):
        return self.status

    def setUser(self, user):
        self.user = user

    def getUser(self):
        return self.user

    def setId(self, id):
        self.id = id

    def getId(self):
        return self.id

    def getCreatedOn(self):
        return self.createdOn
    
    def getUpdatedOn(self):
        return self.updatedOn

    @staticmethod
    def getAllTasks(mysql):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        cursor.execute('SELECT * FROM task ORDER BY startTime ASC')
        tasks = cursor.fetchall()

        return tasks

    @staticmethod
    def getAllTasksUser(user_id, mysql):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        cursor.execute('SELECT * FROM task WHERE user = % s ORDER BY createdon ASC', (user_id,))
        tasks = cursor.fetchall()

        return tasks

    @staticmethod
    def getTask(task_id, mysql):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        cursor.execute('SELECT * FROM task WHERE id = % s', (task_id,))
        task = cursor.fetchone()

        return task

    @staticmethod
    def addTask(task, mysql):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        cursor.execute('INSERT INTO task (user, title, description, startTime, endTime, date, status) VALUES(% s, % s, % s, % s, % s, % s, % s)', (task.getUser(), task.getTitle(), task.getDescription(), task.getStartTime(), task.getEndTime(), task.getDate(), task.getStatus(),))
        mysql.connection.commit()

        return True

    @staticmethod
    def updateTask(task_id, task, mysql):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        cursor.execute('UPDATE task SET title = % s, description = % s, startTime = % s, endTime = % s, date = % s, status = % s WHERE id = % s', 
        (task.getTitle(), task.getDescription(), task.getStartTime(), task.getEndTime(), task.getDate(), task.getStatus(), task_id,))
        mysql.connection.commit()

        return True
    
    @staticmethod
    def updateTaskStatus(task_id, task_status, mysql):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        cursor.execute('UPDATE task SET status = % s WHERE id = % s', 
        (task_status, task_id,))
        mysql.connection.commit()

        return True

    @staticmethod
    def completeTask(task_id, mysql):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        cursor.execute('UPDATE task SET status = % s WHERE id = % s', 
        (1, task_id,))
        mysql.connection.commit()

        return True

    @staticmethod
    def incompleteTask(task_id, mysql):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        cursor.execute('UPDATE task SET status = % s WHERE id = % s', 
        (2, task_id,))
        mysql.connection.commit()

        return True

    @staticmethod
    def deleteTask(task_id, mysql):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        cursor.execute('DELETE FROM task WHERE id = % s', (task_id,))
        mysql.connection.commit()

        return True