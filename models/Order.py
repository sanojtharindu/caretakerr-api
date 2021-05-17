import os
from flask import Flask
from flask_cors import CORS
from flask_mysqldb import MySQL
import MySQLdb
from datetime import datetime

class Order:
    def __init__(self, prescription, client, orderDate, pharmacy=None, orderStatus=None, orderStatusDate=None, id=None, createdOn=None, updatedOn=None):
        self.orderDate = orderDate
        self.orderStatus = orderStatus
        self.prescription = prescription
        self.client = client
        self.pharmacy = pharmacy
        self.orderStatusDate = orderStatusDate
        self.id = id
        self.createdOn = createdOn
        self.updatedOn = updatedOn

    def setOrderDate(self, orderDate):
        self.orderDate = orderDate

    def getOrderDate(self):
        return self.orderDate

    def setOrderStatus(self, orderStatus):
        self.orderStatus = orderStatus

    def getOrderStatus(self):
        return self.orderStatus

    def setPrescription(self, prescription):
        self.prescription = prescription

    def getPrescription(self):
        return self.prescription

    def setClient(self, client):
        self.client = client

    def getClient(self):
        return self.client

    def setPharmacy(self, pharmacy):
        self.pharmacy = pharmacy

    def getPharmacy(self):
        return self.pharmacy

    def setOrderStatusDate(self, orderStatusDate):
        self.orderStatusDate = orderStatusDate

    def getOrderStatusDate(self):
        return self.orderStatusDate

    def setId(self, id):
        self.id = id

    def getId(self):
        return self.id

    def getCreatedOn(self):
        return self.createdOn

    def getUpdatedOn(self):
        return self.updatedOn

    @staticmethod
    def getAllOrders(mysql):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        
        cursor.execute('SELECT * FROM prescOrder ORDER BY id')
        orders = cursor.fetchall()

        return orders

    @staticmethod
    def getAllOrdersMonthly(mysql):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        cursor.execute('SELECT COUNT(*) AS COUNT FROM prescOrder WHERE MONTH(orderDate) = 1 AND YEAR(orderDate) = 2021')
        jan = cursor.fetchone()
        cursor.execute('SELECT COUNT(*) AS COUNT FROM prescOrder WHERE MONTH(orderDate) = 2 AND YEAR(orderDate) = 2021')
        feb = cursor.fetchone()
        cursor.execute('SELECT COUNT(*) AS COUNT FROM prescOrder WHERE MONTH(orderDate) = 3 AND YEAR(orderDate) = 2021')
        mar = cursor.fetchone()
        cursor.execute('SELECT COUNT(*) AS COUNT FROM prescOrder WHERE MONTH(orderDate) = 4 AND YEAR(orderDate) = 2021')
        apr = cursor.fetchone()
        cursor.execute('SELECT COUNT(*) AS COUNT FROM prescOrder WHERE MONTH(orderDate) = 5 AND YEAR(orderDate) = 2021')
        may = cursor.fetchone()
        cursor.execute('SELECT COUNT(*) AS COUNT FROM prescOrder WHERE MONTH(orderDate) = 6 AND YEAR(orderDate) = 2021')
        jun = cursor.fetchone()
        cursor.execute('SELECT COUNT(*) AS COUNT FROM prescOrder WHERE MONTH(orderDate) = 7 AND YEAR(orderDate) = 2021')
        jul = cursor.fetchone()
        cursor.execute('SELECT COUNT(*) AS COUNT FROM prescOrder WHERE MONTH(orderDate) = 8 AND YEAR(orderDate) = 2021')
        aug = cursor.fetchone()
        cursor.execute('SELECT COUNT(*) AS COUNT FROM prescOrder WHERE MONTH(orderDate) = 9 AND YEAR(orderDate) = 2021')
        sept = cursor.fetchone()
        cursor.execute('SELECT COUNT(*) AS COUNT FROM prescOrder WHERE MONTH(orderDate) = 10 AND YEAR(orderDate) = 2021')
        octo = cursor.fetchone()
        cursor.execute('SELECT COUNT(*) AS COUNT FROM prescOrder WHERE MONTH(orderDate) = 11 AND YEAR(orderDate) = 2021')
        nov = cursor.fetchone()
        cursor.execute('SELECT COUNT(*) AS COUNT FROM prescOrder WHERE MONTH(orderDate) = 12 AND YEAR(orderDate) = 2021')
        dec = cursor.fetchone()

        return {"jan":jan,"feb":feb,"mar":mar,"apr":apr,"may":may,"jun":jun,"jul":jul,"aug":aug,"sept":sept,"octo":octo,"nov":nov,"dec":dec}

    @staticmethod
    def getTopOrders(mysql):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        cursor.execute('SELECT * FROM prescOrder WHERE orderStatus = 0 ORDER BY createdOn DESC LIMIT 10')
        orders = cursor.fetchall()

        return orders

    @staticmethod
    def getOrdersUser(user_id, mysql):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        
        cursor.execute('SELECT * FROM prescOrder WHERE client = % s ORDER BY createdOn desc', (user_id,))
        orders = cursor.fetchall()

        return orders

    @staticmethod
    def getOrder(order_id, mysql):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        
        cursor.execute('SELECT * FROM prescOrder WHERE id = % s', (order_id,))
        order = cursor.fetchone()

        return order

    @staticmethod
    def addOrder(order, mysql):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        
        cursor.execute('INSERT INTO prescOrder(prescription, client, orderDate) VALUES(% s, % s, % s)', (order.getPrescription(), order.getClient(), order.getOrderDate(),))
        mysql.connection.commit()

        return True
    
    @staticmethod
    def updateOrder(order_id, order, mysql):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        
        cursor.execute('UPDATE prescOrder SET orderDate = % s, prescription = % s, client = % s WHERE id = % s', 
        (order.getOrderDate(), order.getPrescription(), order.getClient(), order_id,))
        mysql.connection.commit()

        return True

    @staticmethod
    def cancelOrder(order_id, mysql):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        
        cursor.execute('UPDATE prescOrder SET orderStatus = % s, orderStatusDate = % s WHERE id = % s', 
        (2, datetime.today().strftime('%Y-%m-%d'), order_id,))
        mysql.connection.commit()

        return True

    @staticmethod
    def completeOrder(order_id, mysql):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        
        cursor.execute('UPDATE prescOrder SET orderStatus = % s, orderStatusDate = % s WHERE id = % s', 
        (1, datetime.today().strftime('%Y-%m-%d'), order_id,))
        mysql.connection.commit()

        return True

    @staticmethod
    def assignPharmacy(order_id, pharmacy_id, mysql):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        cursor.execute('UPDATE prescOrder SET pharmacy = % s WHERE id = % s', (pharmacy_id, order_id,))
        mysql.connection.commit()

        return True
    
    @staticmethod
    def unassignPharmacy(order_id, pharmacy_id, mysql):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        cursor.execute('UPDATE prescOrder SET pharmacy = % s WHERE id = % s', (None, order_id,))
        mysql.connection.commit()

        return True

    @staticmethod
    def deleteOrder(order_id, mysql):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        cursor.execute('DELETE FROM prescOrder WHERE id = % s', (order_id,))
        mysql.connection.commit()

        return True