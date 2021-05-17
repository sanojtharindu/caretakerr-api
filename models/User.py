import os
from flask import Flask
from flask_cors import CORS
from flask_mysqldb import MySQL
import MySQLdb

class User:
    def __init__(self, name, email, password, phone, address, id=None, createdOn=None, updatedOn=None):
        self.name = name
        self.email = email
        self.password = password
        self.phone = phone
        self.address = address
        self.id = id
        self.createdOn = createdOn
        self.updatedOn = updatedOn

    def setName(self, name):
        self.name = name

    def getName(self):
        return self.name

    def setEmail(self, email):
        self.email = email

    def getEmail(self):
        return self.email

    def setPassword(self, password):
        self.password = password

    def getPassword(self):
        return self.password

    def setPhone(self, phone):
        self.phone = phone

    def getPhone(self):
        return self.phone

    def setAddress(self, address):
        self.address = address

    def getAddress(self):
        return self.address

    def setId(self, id):
        self.id = id

    def getId(self):
        return self.id

    def getCreatedOn(self):
        return self.createdOn

    def getUpdatedOn(self):
        return self.updatedOn

    @staticmethod
    def getAllUsers(mysql):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        
        cursor.execute('SELECT * FROM user ORDER BY id')
        users = cursor.fetchall()

        return users

    @staticmethod
    def getUser(user_id, mysql):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        
        cursor.execute('SELECT * FROM user WHERE id = % s',(user_id,))
        user = cursor.fetchone()

        return user

    @staticmethod
    def addUser(user, mysql):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        
        cursor.execute('INSERT INTO user (name, email, password, phone, address) VALUES(% s, % s, % s, % s, % s)',(user.getName(), user.getEmail(), user.getPassword(), user.getPhone(), user.getAddress(),))
        mysql.connection.commit()

        return True

    @staticmethod
    def updateUser(user_id, user, mysql):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        
        cursor.execute('UPDATE user SET name = % s, email = % s, password = % s, phone = % s, address = % s WHERE id = % s',(user.getName(), user.getEmail(), user.getPassword(), user.getPhone(), user.getAddress(), user_id,))
        mysql.connection.commit()

        return True

    @staticmethod
    def deleteUser(user_id, mysql):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        cursor.execute('DELETE FROM user WHERE id = % s', (user_id,))
        mysql.connection.commit()

        return True

    @staticmethod
    def login(email, password, mysql):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        cursor.execute('SELECT * FROM user WHERE email = % s AND password = % s', (email, password,))
        user = cursor.fetchone()

        return user