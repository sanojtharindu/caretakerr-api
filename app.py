from flask import Flask, jsonify, send_file
from flask_cors import CORS, cross_origin
from flask_mysqldb import MySQL
from models.User import User
from models.Caretaker import Caretaker
from models.Client import Client
from models.Message import Message
from models.Pharmacy import Pharmacy
from models.Task import Task
from models.Report import Report
from models.Order import Order
from models.Prescription import Prescription
from models.Message import Message
from models.History import History
from flask import request
from werkzeug.utils import secure_filename
import os
import json
import time
from datetime import datetime
import boto3
from s3demo import list_files, upload_file, download_file
from config import create_s3_client

port = int(os.environ.get('PORT', 5000))
app = Flask(__name__)
app.secret_key = '08t$ht788tjHT%674BD'
app.config["DEBUG"] = True
app.config['MYSQL_HOST'] = 'remotemysql.com'
app.config['MYSQL_PORT'] = 3306
app.config['MYSQL_USER'] = '3BzIORiQ7G'
app.config['MYSQL_PASSWORD'] = 'kEl35styGL'
app.config['MYSQL_DB'] = '3BzIORiQ7G'

mysql = MySQL(app)

CORS(app)

s3_resource = boto3.resource('s3')
s3_client = create_s3_client()

# File Get, Upload and Download Endpoints
@app.route('/listfile',methods=['GET'])
def get_files():
    return jsonify({"result":True, "content":list_files()})

@app.route('/file/upload',methods=['POST'])
def upload_file_s3():
    f = request.files['file']
    if f.filename:
        print('Uploading file = {}'.format(f.filename))
        # secure_filename function will replace any whitespace provided filename with an underscore
        # saving the file in the local folder
        filename = secure_filename(f.filename)  # This is convenient to validate your filename, otherwise just use file.filename
        
        s3_client.put_object(Body=f, Bucket='caretakerr', Key=filename, ContentType=request.mimetype)

        # f.save(os.path.join('/', secure_filename(f.filename)))
        # upload_file(f'{secure_filename(f.filename)}')
    else:
        print('Skipping file upload op')
 
    return redirect('/')

@app.route('/download/<path:filename>',methods=['GET'])
def download_file_s3(filename):
    print('Downloading file = {}'.format(filename))
    output = download_file(filename)
 
    return send_file(output, as_attachment=True)

@app.route('/', methods=['GET'])
@cross_origin(origin='*')
def index():
    client = {
        'Function': 'Login',
        'Details' : {
            'Endpoint': '/login/client',
            'Method': 'POST',
            'Parameters': '',
            'Body': 'email, password',
            'Return': 'JSON - {"result": Boolean, "msg": String}',
        },
    }

    caretaker = {
        'Function': 'Login',
        'Details' : {
            'Endpoint': '/login/caretaker',
            'Method': 'POST',
            'Parameters': '',
            'Body': 'email, password',
            'Return': 'JSON - {"result": Boolean, "msg": String}',
        },
    }

    task = {
        'Function': 'GET All Task by User',
        'Details': {
            'Endpoint': '/tasks/<int:user_id>',
            'Method': 'GET',
            'Parameters': 'user_id',
            'Body': '',
            'Return': 'JSON - {"tasks": tasks}',
        },

        'Function': 'GET Task by Task ID',
        'Details': {
            'Endpoint': '/task/<int:task_id>',
            'Method': 'GET',
            'Parameters': 'task_id',
            'Body': '',
            'Return': 'JSON - {"task":task}',
        },

        'Function': 'ADD Task',
        'Details': {
            'Endpoint': '/task',
            'Method': 'POST',
            'Parameters': '',
            'Body': 'title, description, startTime, endTime, date, status, user',
            'Return': 'JSON - {"result":Boolean,"msg": String}',
        },

        'Function': 'UPDATE Task',
        'Details': {
            'Endpoint': '/task/<int:task_id>',
            'Method': 'PUT',
            'Parameters': 'task_id',
            'Body': 'title, description, startTime, endTime, date, status, user',
            'Return': 'JSON - {"result":Boolean, "msg":String}',
        },

        'Function': 'UPDATE Task Status',
        'Details': {
            'Endpoint': '/task/status/<int:task_id>',
            'Method': 'PUT',
            'Parameters': 'task_id',
            'Body': 'task_status',
            'Return': 'JSON - {"result":Boolean, "msg":String}',
        },

        'Function': 'DELETE Task',
        'Details': {
            'Endpoint': '/task/<int:task_id>',
            'Method': 'DELETE',
            'Parameters': 'task_id',
            'Body': '',
            'Return': 'JSON - {"result":Boolean,"msg":String}',
        },
    }

    report = {
        'Function': 'GET All Report by User',
        'Details': {
            'Endpoint': '/reports/<int:user_id>',
            'Method': 'GET',
            'Parameters': 'user_id',
            'Body': '',
            'Return': 'JSON - {"reports": reports}',
        },

        'Function': 'GET Report by Report ID',
        'Details': {
            'Endpoint': '/report/<int:task_id>',
            'Method': 'GET',
            'Parameters': 'report_id',
            'Body': '',
            'Return': 'JSON - {"report":report}',
        },

        'Function': 'ADD Report',
        'Details': {
            'Endpoint': '/report',
            'Method': 'POST',
            'Parameters': '',
            'Body': 'title, description, startTime, endTime, date, status, user',
            'Return': 'JSON - {"result":Boolean,"msg": String}',
        },

        'Function': 'UPDATE Report',
        'Details': {
            'Endpoint': '/report/<int:report_id>',
            'Method': 'PUT',
            'Parameters': 'report_id',
            'Body': 'title, description, startTime, endTime, date, status, user',
            'Return': 'JSON - {"result":Boolean, "msg":String}',
        },

        'Function': 'UPDATE Report Show',
        'Details': {
            'Endpoint': '/report/show/<int:report_id>',
            'Method': 'PUT',
            'Parameters': 'report_id',
            'Body': 'reportShow',
            'Return': 'JSON - {"result":Boolean, "msg":String}',
        },

        'Function': 'DELETE Report',
        'Details': {
            'Endpoint': '/report/<int:report_id>',
            'Method': 'DELETE',
            'Parameters': 'report_id',
            'Body': '',
            'Return': 'JSON - {"result":Boolean,"msg":String}',
        },
    }

    prescription = {
        'Function': 'GET All Prescriptions by User',
        'Details': {
            'Endpoint': '/prescriptions/<int:user_id>',
            'Method': 'GET',
            'Parameters': 'user_id',
            'Body': '',
            'Return': 'JSON - {"prescriptions": prescriptions}',
        },

        'Function': 'GET Prescription by Prescription ID',
        'Details': {
            'Endpoint': '/prescription/<int:prescription_id>',
            'Method': 'GET',
            'Parameters': 'prescription_id',
            'Body': '',
            'Return': 'JSON - {"prescription":prescription}',
        },

        'Function': 'ADD Prescription',
        'Details': {
            'Endpoint': '/prescription',
            'Method': 'POST',
            'Parameters': '',
            'Body': 'prescDesc, prescDate, prescFreq, prescFile, prescAuto, prescPending, prescUser',
            'Return': 'JSON - {"result":Boolean,"msg": String}',
        },

        'Function': 'UPDATE Prescription',
        'Details': {
            'Endpoint': '/prescription/<int:prescription_id>',
            'Method': 'PUT',
            'Parameters': 'prescription_id',
            'Body': 'prescDesc, prescDate, prescFreq, prescFile, prescAuto, prescPending, prescUser, prescPrice',
            'Return': 'JSON - {"result":Boolean, "msg":String}',
        },

        'Function': 'UPDATE Prescription Price',
        'Details': {
            'Endpoint': '/prescription/show/<int:prescription_id>',
            'Method': 'PUT',
            'Parameters': 'prescription_id',
            'Body': 'prescPending, prescPrice',
            'Return': 'JSON - {"result":Boolean, "msg":String}',
        },

        'Function': 'DELETE Prescription',
        'Details': {
            'Endpoint': '/prescription/<int:prescription_id>',
            'Method': 'DELETE',
            'Parameters': 'prescription_id',
            'Body': '',
            'Return': 'JSON - {"result":Boolean,"msg":String}',
        },
    }
    orders = {
        'Function': 'GET All Orders by User',
        'Details': {
            'Endpoint': '/orders/<int:user_id>',
            'Method': 'GET',
            'Parameters': 'user_id',
            'Body': '',
            'Return': 'JSON - {"orders": orders}',
        },

        'Function': 'GET Order by Prescription ID',
        'Details': {
            'Endpoint': '/order/<int:order_id>',
            'Method': 'GET',
            'Parameters': 'order_id',
            'Body': '',
            'Return': 'JSON - {"order":order}',
        },

        'Function': 'ADD Order',
        'Details': {
            'Endpoint': '/order',
            'Method': 'POST',
            'Parameters': '',
            'Body': 'prescDesc, prescDate, prescFreq, prescFile, prescAuto, prescPending, prescUser',
            'Return': 'JSON - {"result":Boolean,"msg": String}',
        },

        'Function': 'UPDATE Order',
        'Details': {
            'Endpoint': '/order/<int:order_id>',
            'Method': 'PUT',
            'Parameters': 'order_id',
            'Body': 'prescDesc, prescDate, prescFreq, prescFile, prescAuto, prescPending, prescUser, prescPrice',
            'Return': 'JSON - {"result":Boolean, "msg":String}',
        },

        'Function': 'UPDATE Order Price',
        'Details': {
            'Endpoint': '/order/show/<int:order_id>',
            'Method': 'PUT',
            'Parameters': 'order_id',
            'Body': 'prescPending, prescPrice',
            'Return': 'JSON - {"result":Boolean, "msg":String}',
        },

        'Function': 'DELETE Order',
        'Details': {
            'Endpoint': '/order/<int:order_id>',
            'Method': 'DELETE',
            'Parameters': 'order_id',
            'Body': '',
            'Return': 'JSON - {"result":Boolean,"msg":String}',
        },
    }

    endpoints = {"client":client,"caretaker":caretaker,"task":task,"report":report,"prescription":prescription,"order":orders}

    return jsonify({"endpoints":endpoints})


'''

'''
@app.route('/getCounts',methods=['GET'])
@cross_origin(origin='*')
def getCounts():
    try:
        clients = Client.getAllClients(mysql)
        caretakers = Caretaker.getAllCaretakers(mysql)
        pharmacies = Pharmacy.getAllPharmacies(mysql)
        orders = Order.getAllOrders(mysql)

        return jsonify({"clients":len(clients),"caretakers":len(caretakers),"pharmacies":len(pharmacies),"orders":len(orders)})
    except Exception as e:
        return jsonify({"result":False,"msg":"Failed to Obtain Counts","error":str(e)})

'''
Client Login API Endpoint
'''
@app.route('/login/client', methods=['POST'])
@cross_origin(origin='*')
def loginUser():
    try:
        # Read the Login Credentials
        data = request.json
        result = Client.login(data['email'],data['password'], mysql)
        if (result):
            return jsonify({"result":True, "msg":"Successfully Logged In!","client":result})

        return jsonify({"result":False, "msg":"Failed to Login!"})
    except Exception as e:
        return jsonify({"result":False, "msg":"Failed to Login!","error":str(e)})

'''
Caretaker Login API Endpoint
'''
@app.route('/login/caretaker', methods=['POST'])
@cross_origin(origin='*')
def loginCaretaker():
    try:
        # Read the Login Credentials
        data = request.json
        result = Caretaker.login(data['email'],data['password'], mysql)

        if (result):
            # Update Status - Offline
            return jsonify({"result":True, "msg":"Successfully Logged In!","caretaker":result})

        return jsonify({"result":False, "msg":"Failed to Login!"})
    except Exception as e:
        return jsonify({"result":False, "msg":"Failed to Login!","error":str(e)})

'''
Admin Login API Endpoint
'''
@app.route('/login/admin', methods=['POST'])
@cross_origin(origin='*')
def loginAdmin():
    try:
        # Read the Login Credentials
        data = request.json
        
        result = User.login(data['email'],data['password'], mysql)

        if (result):
            # Update Status - Online
            return jsonify({"result":True, "msg":"Successfully Logged In!","user":result})

        return jsonify({"result":False, "msg":"Failed to Login!"})
    except Exception as e:
        return jsonify({"result":False, "msg":"Failed to Login!","error":str(e)})

'''
======================
======================
PHARMACY API ENDPOINTS
======================
======================
'''
@app.route('/pharmacies',methods=['GET'])
@cross_origin(origin='*')
def getAllPharmacies():
    try:
        return jsonify({"pharmacies":Pharmacy.getAllPharmacies(mysql)})
    except Exception as e:
        print(e)
        return jsonify({"pharmacies":None,"msg":"Failed to Retrieve Pharmacies","error":str(e)})

@app.route('/pharmacy/<int:pharmacy_id>',methods=['GET'])
@cross_origin(origin='*')
def getPharmacy(pharmacy_id):
    try:
        return jsonify({"pharmacies":Pharmacy.getPharmacy(pharmacy_id,mysql)})
    except Exception as e:
        print(e)
        return jsonify({"pharmacies":None,"msg":"Failed to Retrieve Pharmacies","error":str(e)})

@app.route('/pharmacy',methods=['POST'])
@cross_origin(origin='*')
def addPharmacy():
    try:
        if 'licenseFile' not in request.files:
            return jsonify({"result":False, "msg":"File not found!"})
        
        licImage = request.files['licenseFile']
        licImageName = secure_filename(licImage.filename)
        licImage.save(licImageName)

        # Upload Image to S3
        if licImage.filename:
            print('Uploading file = {}'.format(licImageName))
            s3_client.put_object(Body=licImage, Bucket='caretakerr', Key=licImageName, ContentType=request.mimetype)
        else:
            print('Skipping file upload op')

        pharmacy = Pharmacy(request.form['name'], request.form['code'], request.form['email'], request.form['phone'], request.form['address'], request.form['openHours'], request.form['available'], license=licImageName, password=request.form['password'])
        result = Pharmacy.addPharmacy(pharmacy, mysql)

        return jsonify({"result":True,"msg":"Successfully Created Pharmacy!"})
    except Exception as e:
        return jsonify({"result":False,"msg":"Failed to Add New Pharmacy","error":str(e)})

@app.route('/pharmacy/<int:pharmacy_id>',methods=['PUT'])
@cross_origin(origin='*')
def updatePharmacy(pharmacy_id):
    try:
        if 'licenseFile' not in request.files:
            pharmacy = Pharmacy(request.form['name'], request.form['code'], request.form['email'], request.form['phone'], request.form['address'], request.form['license'], request.form['openHours'], request.form['available'])
            result = Pharmacy.updatePharmacy(pharmacy_id, pharmacy, mysql)

            return jsonify({"result":True,"msg":"Successfully Updated Pharmacy!"})
        else:
            licImage = request.files['licenseFile']
            licImageName = secure_filename(licImage.filename)
            licImage.save(licImageName)

            # Upload Image to S3
            if licImage.filename:
                print('Uploading file = {}'.format(licImageName))
                s3_client.put_object(Body=licImage, Bucket='caretakerr', Key=licImageName, ContentType=request.mimetype)
            else:
                print('Skipping file upload op')

            pharmacy = Pharmacy(request.form['name'], request.form['code'], request.form['email'], request.form['phone'], request.form['address'], request.form['license'], request.form['openHours'], request.form['available'], license=licImageName)
            result = Pharmacy.updatePharmacy(pharmacy_id, pharmacy, mysql)

            return jsonify({"result":True,"msg":"Successfully Updated Pharmacy!"})
    except Exception as e:
        return jsonify({"result":False,"msg":"Failed to Update Pharmacy","error":str(e)})


@app.route('/pharmacy/available/<int:pharmacy_id>',methods=['PUT'])
@cross_origin(origin='*')
def makeAvailable(pharmacy_id):
    try:
        result = Pharmacy.makeAvailable(pharmacy_id, mysql)

        return jsonify({"result":True,"msg":"Successfully Made Pharmacy Available"})
    except Exception as e:
        return jsonify({"result":False,"msg":"Failed to Make Pharmacy Available","error":str(e)})
        
@app.route('/pharmacy/unavailable/<int:pharmacy_id>',methods=['PUT'])
@cross_origin(origin='*')
def makeUnavailable(pharmacy_id):
    try:
        result = Pharmacy.makeUnavailable(pharmacy_id, mysql)

        return jsonify({"result":True,"msg":"Successfully Made Pharmacy Unvailable"})
    except Exception as e:
        return jsonify({"result":False,"msg":"Failed to Make Pharmacy Unavailable","error":str(e)})
        
'''
==================
==================
CLIENT API ENDPOINTS
==================
==================
'''
@app.route('/clients', methods=['GET'])
@cross_origin(origin='*')
def getAllUsers():
    try:
        return jsonify({"clients":Client.getAllClients(mysql)})
    except Exception as e:
        print(e)
        return jsonify({"clients":None,"msg":"Failed to Retrieve Clients","error":str(e)})

@app.route('/client/<int:client_id>', methods=['GET'])
@cross_origin(origin='*')
def getUser(client_id):
    try:
        return jsonify({"client":Client.getClient(client_id,mysql)})
    except Exception as e:
        print(e)
        return jsonify({"client":None,"msg":"Failed to Retrieve Client","error":str(e)})

@app.route('/client', methods=['POST'])
@cross_origin(origin='*')
def addUser():
    try:
        client = Client(request.json['name'], request.json['email'], request.json['password'], request.json['phone'], request.json['address'], request.json['identification'], clientName=request.json['clientName'], clientAddress=request.json['clientAddress'], clientBirth=request.json['clientBirth'], clientGender=request.json['clientGender'], clientIdentification=request.json['clientIdentification'], clientConditions=request.json['clientConditions'])
        result = Client.addClient(client,mysql)

        return jsonify({"result":True,"msg":"Successfully Created Client!"})
    except Exception as e:
        print(e)
        return jsonify({"result":False,"msg":"Failed to Create Client","error":str(e)})

@app.route('/client/<int:client_id>', methods=['PUT'])
@cross_origin(origin='*')
def updateClient(client_id):
    try:
        client = Client(request.json['name'], request.json['email'], request.json['password'], request.json['phone'], request.json['address'], id=request.json['id'])

        result = Client.updateClient(client_id,request.json,mysql)

        return jsonify({"result":True,"msg":"Successfully Updated Client!"})
    except Exception as e:
        print(e)
        return jsonify({"result":False,"msg":"Failed to Update Client","error":str(e)})

@app.route('/client/<int:client_id>', methods=['DELETE'])
@cross_origin(origin='*')
def deleteClient(client_id):
    try:
        result = Client.deleteClient(client_id,mysql)

        return jsonify({"result":True,"msg":"Successfully Deleted Client!"})
    except Exception as e:
        print(e)
        return jsonify({"result":False,"msg":"Failed to Delete Client","error":str(e)})

@app.route('/client/payment/<int:client_id>',methods=['GET'])
@cross_origin(origin='*')
def getPaymentInfo(client_id):
    try:
        result = Client.getPaymentInfo(client_id, mysql)

        return jsonify({"paymentInfo":result})
    except Exception as e:
        print(e)
        return jsonify({"paymentInfo":None,"msg":"Failed to Get Payment Information","error":str(e)})

@app.route('/client/payment/<int:client_id>',methods=['PUT'])
@cross_origin(origin='*')
def updatePaymentInfo(client_id):
    try:
        data = request.json
        result = Client.updatePaymentInfo(client_id, data['cardholdername'], data['cardnumber'], data['cvv'], data['expiryDate'], mysql)

        return jsonify({"result":True,"msg":"Successfully Updated Payment Information!"})
    except Exception as e:
        print(e)
        return jsonify({"result":False,"msg":"Failed to Update Payment Information","error":str(e)})

'''
=======================
=======================
CARETAKER API ENDPOINTS
=======================
=======================
'''
@app.route('/caretakers',methods=['GET'])
@cross_origin(origin='*')
def getAllCaretakers():
    try:
        return jsonify({"caretakers":Caretaker.getAllCaretakers(mysql)})
    except Exception as e:
        print(e)
        return jsonify({"caretakers":None,"msg":"Failed to retrieve caretakers","error":str(e)})

@app.route('/caretakers/top',methods=['GET'])
@cross_origin(origin='*')
def getTopCaretakers():
    try:
        return jsonify({"caretakers":Caretaker.getTopCaretakers(mysql)})
    except Exception as e:
        print(e)
        return jsonify({"caretakers":None,"msg":"Failed to Retrieve Caretakers","error":str(e)})

@app.route('/caretakers/unassigned', methods=['GET'])
@cross_origin(origin='*')
def getUnassignedCaretakers():
    try:
        return jsonify({"caretakers":Caretaker.getUnassignedCaretakers(mysql)})
    except Exception as e:
        print(e)
        return jsonify({"caretakers":None, "msg":"Failed to Retrieve Caretakers","error":str(e)})

@app.route('/caretaker/<int:caretaker_id>',methods=['GET'])
@cross_origin(origin='*')
def getCaretaker(caretaker_id):
    try:
        return jsonify({"caretaker":Caretaker.getCaretaker(caretaker_id,mysql)})
    except Exception as e:
        print(e)
        return jsonify({"caretaker":None,"msg":"Failed to retrieve caretaker","error":str(e)})

@app.route('/caretaker',methods=['POST'])
@cross_origin(origin='*')
def addCaretaker():
    try:
        print(request.files)
        # Save Caretaker
        if 'experienceFile' not in request.files:
            return jsonify({"result":False, "msg":"Failed to Create Caretaker"})
        else:
            expImage = request.files['experienceFile']
            expImageName = secure_filename(expImage.filename)
            expImage.save(expImageName)

            # Upload Image to S3
            if expImage.filename:
                print('Uploading file = {}'.format(expImageName))
                s3_client.put_object(Body=expImage, Bucket='caretakerr', Key=expImageName, ContentType=request.mimetype)
            else:
                print('Skipping file upload op')

            data = request.form
            caretaker = Caretaker(data['name'], data['email'], data['password'], data['phone'], data['address'], data['occupation'], data['birthDate'], data['identification'], data['availableHours'], data['availableDays'], experience=expImageName)
            result = Caretaker.addCaretaker(caretaker,mysql)
        
        return jsonify({"result":True,"msg":"Successfully Created Caretaker"})
    except Exception as e:
        return jsonify({"result":False,"msg":"Failed to Create Caretaker","error":str(e)})

@app.route('/caretaker/<int:caretaker_id>',methods=['PUT'])
@cross_origin(origin='*')
def updateCaretaker(caretaker_id):
    try:
        if 'experienceFile' not in request.files:
            data = request.form
            caretaker = Caretaker(data['name'], data['email'], data['password'], data['phone'], data['address'], data['occupation'], data['birthDate'], data['identification'], data['availableHours'], data['availableDays'])
            result = Caretaker.updateCaretaker(caretaker_id,caretaker,mysql)
        else:
            expImage = request.files['experienceFile']
            expImageName = secure_filename(expImage.filename)
            expImage.save(expImageName)

            data = request.form
            caretaker = Caretaker(data['name'], data['email'], data['password'], data['phone'], data['address'], data['occupation'], data['birthDate'], data['identification'], data['availableHours'], data['availableDays'], experience=data['experience'])
            result = Caretaker.updateCaretaker(caretaker_id,caretaker,mysql)

        return jsonify({"result":True,"msg":"Successfully Updated Caretaker"})
    except Exception as e:
        return jsonify({"result":False,"msg":"Failed to Update Caretaker","error":str(e)})

@app.route('/caretaker/active/<int:caretaker_id>',methods=['PUT'])
def activeCaretaker(caretaker_id):
    try:
        result = Caretaker.activeCaretaker(caretaker_id, mysql)
        return jsonify({"result":True,"msg":"Caretaker is now Online"})
    except Exception as e:
        return jsonify({"result":False,"msg":"Failed to Make Caretaker Online","error":str(e)})

@app.route('/caretaker/inactive/<int:caretaker_id>',methods=['PUT'])
def inactiveCaretaker(caretaker_id):
    try:
        result = Caretaker.inactiveCaretaker(caretaker_id, mysql)
        return jsonify({"result":True,"msg":"Caretaker is now Offline"})
    except Exception as e:
        return jsonify({"result":False,"msg":"Failed to Make Caretaker Offline","error":str(e)})

@app.route('/caretaker/<int:caretaker_id>',methods=['DELETE'])
@cross_origin(origin='*')
def deleteCaretaker(caretaker_id):
    try:
        result = Caretaker.deleteCaretaker(caretaker_id,mysql)

        return jsonify({"result":True,"msg":"Successfully Deleted Caretaker"})
    except Exception as e:
        return jsonify({"result":False,"msg":"Failed to Delete Caretaker","error":str(e)})

@app.route('/caretaker/<int:caretaker_id>/<int:client_id>',methods=['PUT'])
@cross_origin(origin='*')
def assignClientCaretaker(caretaker_id, client_id):
    try:
        result = Caretaker.assignClient(caretaker_id,client_id,mysql)
        result = Client.assignCaretaker(client_id,caretaker_id,mysql)

        # Add to History
        history = History(client_id, caretaker_id)
        History.addHistory(history, mysql)

        return jsonify({"result":True,"msg":"Successfully Assigned Client to Caretaker"})
    except Exception as e:
        return jsonify({"result":False,"msg":"Failed to Assign Client to Caretaker","error":str(e)})

@app.route('/caretaker/unassign/<int:caretaker_id>/<int:client_id>',methods=['PUT'])
@cross_origin(origin='*')
def unassignClientCaretaker(caretaker_id, client_id):
    try:
        result = Caretaker.unassignClient(caretaker_id,mysql)
        result = Client.unassignCaretaker(client_id,mysql)

        # Get Last Inserted History
        recentHistory = History.getRecentHistory(client_id, caretaker_id, mysql)

        print(recentHistory)
        
        # History Remove Date
        History.updateHistoryRemoved(recentHistory[0], time.strftime('%Y-%m-%d %H:%M:%S'), mysql)

        return jsonify({"result":True,"msg":"Successfully Unassigned Client from Caretaker"})
    except Exception as e:
        return jsonify({"result":False,"msg":"Failed to Unassign Client from Caretaker","error":str(e)})

'''
==================
==================
TASK API ENDPOINTS
==================
==================
'''
@app.route('/tasks/<int:user_id>',methods=['GET'])
@cross_origin(origin='*')
def getAllTasks(user_id):
    try:
        tasks = Task.getAllTasksUser(user_id,mysql)
        return json.dumps({"tasks":tasks}, default=str)
    except Exception as e:
        return jsonify({"tasks":null,"msg":"Failed to retrieve tasks","error":str(e)})

@app.route('/task/<int:task_id>',methods=['GET'])
@cross_origin(origin='*')
def getTask(task_id):
    try:
        tasks = Task.getTask(task_id,mysql)
        return json.dumps({"task":tasks}, default=str)
    except Exception as e:
        return jsonify({"task":None,"msg":"Failed to retrieve task","error":str(e)})

@app.route('/task',methods=['POST'])
@cross_origin(origin='*')
def addTask():
    new_date=None
    new_data_str=None
    try:
        data = request.json
        # How Does the Task Repeat
        # Repeat = 0 : Do Not Repeat
        # Repeat = 1 : Repeat Daily this Month
        # Repeat = 2 : Every Week for this Month
        if (request.json['repeat'] == 0):
            task = Task(data['title'], data['description'], data['startTime'], data['endTime'], data['date'], 0, user=data['user'])
            result = Task.addTask(task,mysql)

        if (request.json['repeat'] == 1):
            # Repeat Daily for this Month - Get Todays Date. Run it until 30th
            task_date = datetime.strptime(data['date'], '%Y-%m-%d')
            curr_day = task_date.day # Get the Day
            diff_day = 30 - curr_day # Get the Day difference
            curr_mnth = task_date.month # Get the Month
            curr_year = task_date.year # Get the Year
            for i in range(diff_day+1):
                new_day=curr_day+i
                new_date = datetime(curr_year, curr_mnth, new_day)
                # new_date = datetime.strptime(new_date_str, '%Y-%m-%d')
                task = Task(data['title'], data['description'], data['startTime'], data['endTime'], new_date, 0, user=data['user'])
                result = Task.addTask(task,mysql)
        
        if (request.json['repeat'] == 2):
            # Repeat Every Week for this Month - Get Todays Date. Minus 30 and divide by 7. Then insert into that many times plus the date.
            task_date = datetime.strptime(data['date'], '%Y-%m-%d')
            curr_day = task_date.day # Get the Day
            diff_day = 30 - curr_day # Get the Day difference
            curr_mnth = task_date.month # Get the Month
            curr_year = task_date.year # Get the Year
            num_weeks = diff_day//7 #
            for i in range(num_weeks):
                new_day=curr_day+(i*7)
                new_date = datetime(curr_year, curr_mnth, new_day)
                # new_date = datetime.strptime(new_date_str, '%Y-%m-%d')
                task = Task(data['title'], data['description'], data['startTime'], data['endTime'], new_date, 0, user=data['user'])
                result = Task.addTask(task,mysql)

        return jsonify({"result":True,"msg":"Successfully Created Task"})
    except Exception as e:
        return jsonify({"result":False,"msg":"Failed to Create Task","error":str(e)})

@app.route('/task/<int:task_id>',methods=['PUT'])
@cross_origin(origin='*')
def updateTask(task_id):
    try:
        data = request.json
        task = Task(data['title'], data['description'], data['startTime'], data['endTime'], data['date'], data['status'])
        result = Task.updateTask(task_id,task,mysql)

        return jsonify({"result":True,"msg":"Successfully Updated Task"})
    except Exception as e:
        return jsonify({"result":False,"msg":"Failed to Update Task","error":str(e)})

@app.route('/task/status/<int:task_id>',methods=['PUT'])
@cross_origin(origin='*')
def updateTaskStatus(task_id):
    try:
        data = request.json
        result = Task.updateTaskStatus(task_id,data['task_status'],mysql)

        return jsonify({"result":True,"msg":"Successfully Updated Task"})
    except Exception as e:
        return jsonify({"result":False,"msg":"Failed to Update Task","error":str(e)})

@app.route('/task/complete/<int:task_id>',methods=['PUT'])
@cross_origin(origin='*')
def completeTask(task_id):
    try:
        result = Task.completeTask(task_id,mysql)
        return jsonify({"result":True,"msg":"Task Complete Success!"})
    except Exception as e:
        return jsonify({"result":False,"msg":"Task Complete Failed","error":str(e)})

@app.route('/task/incomplete/<int:task_id>',methods=['PUT'])
@cross_origin(origin='*')
def incompleteTask(task_id):
    try:
        result = Task.incompleteTask(task_id,mysql)
        return jsonify({"result":True,"msg":"Task Incomplete Success!"})
    except Exception as e:
        return jsonify({"result":False,"msg":"Task Incomplete Failed","error":str(e)})

@app.route('/task/<int:task_id>',methods=['DELETE'])
@cross_origin(origin='*')
def deleteTask(task_id):
    try:
        result = Task.deleteTask(task_id,mysql)

        return jsonify({"result":True,"msg":"Successfully Deleted Task"})
    except Exception as e:
        return jsonify({"result":False,"msg":"Failed to Delete Task","error":str(e)})

'''
====================
====================
REPORT API ENDPOINTS
====================
====================
'''
@app.route('/reports/<int:user_id>',methods=['GET'])
@cross_origin(origin='*')
def getAllReports(user_id):
    try:
        reports = Report.getAllReportsUser(user_id, mysql)
        return json.dumps({"reports":reports}, default=str)
    except Exception as e:
        return jsonify({"reports":None,"msg":"Failed to retrieve reports","error":str(e)})

@app.route('/report/<int:report_id>',methods=['GET'])
@cross_origin(origin='*')
def getReport(report_id):
    try:
        report = Report.getReport(report_id,mysql)
        return json.dumps({"report":report}, default=str)
    except Exception as e:
        return jsonify({"report":None,"msg":"Failed to retrieve report","error":str(e)})

@app.route('/report',methods=['POST'])
@cross_origin(origin='*')
def addReport():
    try:
        # Save Report
        if 'reportImage' not in request.files:
            return jsonify({"result":False, "msg":"Failed to Create Report"})

        reportImage = request.files['reportImage']
        reportFileName = secure_filename(reportImage.filename)
        reportImage.save(reportFileName)

        # Upload Image to S3
        if reportImage.filename:
            print('Uploading file = {}'.format(reportFileName))
            s3_client.put_object(Body=reportImage, Bucket='caretakerr', Key=reportFileName, ContentType=request.mimetype)
        else:
            print('Skipping file upload op')

        report = Report(request.form['reportDesc'], request.form['reportDate'], reportUser=request.form['reportUser'], reportShow=1, reportFile=reportFileName)
        result = Report.addReport(report,mysql)

        return jsonify({"result":True,"msg":"Successfully Created Report"})
    except Exception as e:
        return jsonify({"result":False,"msg":"Failed to Create Report","error":str(e)})

@app.route('/report/<int:report_id>',methods=['PUT'])
@cross_origin(origin='*')
def updateReport(report_id):
    try:
        # Save Report
        if 'reportImage' not in request.files or request.files['reportImage'].filename == '':
            report = Report(request.json['reportDesc'], request.json['reportDate'])
            result = Report.updateReportNoFile(report_id, report, mysql)
            return jsonify({"result":True,"msg":"Successfully Updated Report"})

        reportImage = request.files['reportImage']
        reportFileName = secure_filename(reportImage.filename)
        reportImage.save(reportFileName)

        # Upload Image to S3
        if reportImage.filename:
            print('Uploading file = {}'.format(reportFileName))
            s3_client.put_object(Body=reportImage, Bucket='caretakerr', Key=reportFileName, ContentType=request.mimetype)
        else:
            print('Skipping file upload op')

        report = Report(request.form['reportDesc'], request.form['reportDate'], reportFile=reportFileName)
        result = Report.updateReport(report_id,report,mysql)

        return jsonify({"result":True,"msg":"Successfully Updated Report"})
    except Exception as e:
        print(e)
        return jsonify({"result":False,"msg":"Failed to Update Report","error":str(e)})

@app.route('/report/show/<int:report_id>',methods=['PUT'])
@cross_origin(origin='*')
def showReport(report_id):
    try:
        result = Report.showReport(report_id,mysql)

        return jsonify({"result":True,"msg":"Successfully Made Report Available!"})
    except Exception as e:
        return jsonify({"result":False, "msg":"Failed to Make Report Available","error":str(e)})

@app.route('/report/hide/<int:report_id>',methods=['PUT'])
@cross_origin(origin='*')
def hideReport(report_id):
    try:
        result = Report.hideReport(report_id,mysql)

        return jsonify({"result":True,"msg":"Successfully Made Report Unavailable!"})
    except Exception as e:
        return jsonify({"result":False,"msg":"Failed to Make Report Unavailable","error":str(e)})

@app.route('/report/<int:report_id>',methods=['DELETE'])
@cross_origin(origin='*')
def deleteReport(report_id):
    result = Report.deleteReport(report_id,mysql)

    return jsonify({"result":True,"msg":"Successfully Deleted Report"})

'''
==========================
==========================
PRESCRIPTION API ENDPOINTS
==========================
==========================
'''
@app.route('/prescriptions',methods=['GET'])
@cross_origin(origin='*')
def getAllPrescriptions():
    try:
        prescriptions = Prescription.getAllPrescriptions(mysql)
        return json.dumps({"prescriptions":prescriptions}, default=str)
    except Exception as e:
        return jsonify({"prescriptions":None,"msg":"Failed to retrieve all prescriptions","error":str(e)})

@app.route('/prescriptions/<int:user_id>',methods=['GET'])
@cross_origin(origin='*')
def getAllPrescriptionsUser(user_id):
    try:
        prescriptions=Prescription.getAllPrescriptionsUser(user_id,mysql)
        return json.dumps({"prescriptions":prescriptions}, default=str)
    except Exception as e:
        return jsonify({"prescriptions":None,"msg":"Failed to retrieve prescriptions","error":str(e)})

@app.route('/prescription/<int:prescription_id>',methods=['GET'])
@cross_origin(origin='*')
def getPrescription(prescription_id):
    try:
        prescription=Prescription.getPrescription(prescription_id, mysql)
        
        return json.dumps({"prescription":prescription}, default=str)
    except Exception as e:
        return jsonify({"prescription":None,"msg":"Failed to retrieve prescription","error":str(e)})

@app.route('/prescription',methods=['POST'])
@cross_origin(origin='*')
def addPrescription():
    try:
        # Save Prescription
        if 'prescImage' not in request.files:
            return jsonify({"result":False, "msg":"Failed to Create Prescription"})

        prescImage = request.files['prescImage']
        prescFileName = secure_filename(prescImage.filename)
        prescImage.save(prescFileName)

        # Upload Image to S3
        if prescImage.filename:
            print('Uploading file = {}'.format(prescFileName))
            s3_client.put_object(Body=prescImage, Bucket='caretakerr', Key=prescFileName, ContentType=request.mimetype)
        else:
            print('Skipping file upload op')

        prescription = Prescription(request.form['prescDesc'], request.form['prescDate'], request.form['prescFreq'], prescUser=request.form['prescUser'], prescFile=prescFileName)
        result = Prescription.addPrescription(prescription,mysql)

        return jsonify({"result":True,"msg":"Successfully Created Prescription"})
    except Exception as e:
        return jsonify({"result":False,"msg":"Failed to Create Prescription","error":str(e)})

@app.route('/prescription/<int:prescription_id>',methods=['PUT'])
@cross_origin(origin='*')
def updatePrescription(prescription_id):
    try:
        # Save Prescription
        if 'prescImage' in request.files:
            prescImage = request.files['prescImage']
            prescFile = secure_filename(prescImage.filename)
            prescImage.save(prescFile)

            # Upload Image to S3
            if prescImage.filename:
                print('Uploading file = {}'.format(prescFile))
                s3_client.put_object(Body=prescImage, Bucket='caretakerr', Key=prescFile, ContentType=request.mimetype)
            else:
                print('Skipping file upload op')

            prescription = Prescription(request.form['prescDesc'], request.form['prescDate'], request.form['prescFreq'], prescFile=prescFile)
            result = Prescription.updatePrescriptionImage(prescription_id,prescription,mysql)

            return jsonify({"result":True,"msg":"Successfully Updated Prescription"})

        prescription = Prescription(request.json['prescDesc'], request.json['prescDate'], request.json['prescFreq'])
        result = Prescription.updatePrescription(prescription_id,prescription,mysql)

        return jsonify({"result":True,"msg":"Successfully Updated Prescription"})
    except Exception as e:
        return({"jsonify":False,"msg":"Failed to update Prescription","error":str(e)})

@app.route('/prescription/pending/<int:prescription_id>',methods=['PUT'])
@cross_origin(origin='*')
def updatePrescriptionPrice(prescription_id):
    try:
        result = Prescription.updatePrescriptionPrice(prescription_id,request.json['prescPrice'],mysql)

        return jsonify({"result":True,"msg":"Successfully Updated Prescription Price"})
    except Exception as e:
        return jsonify({"result":False,"msg":"Failed to Update Prescription Price","error":str(e)})

@app.route('/prescription/auto/on/<int:prescription_id>',methods=['PUT'])
@cross_origin(origin='*')
def updatePrescriptionAutoOn(prescription_id):
    try:
        result = Prescription.updatePrescriptionAutoOn(prescription_id,mysql)
        return jsonify({"result":True,"msg":"Successfully Set Prescription to Auto Order"})
    except Exception as e:
        return jsonify({"result":False,"msg":"Failed to Set Prescription to Auto Order","error":str(e)})

@app.route('/prescription/auto/off/<int:prescription_id>',methods=['PUT'])
@cross_origin(origin='*')
def updatePrescriptionAutoOff(prescription_id):
    try:
        result = Prescription.updatePrescriptionAutoOff(prescription_id,mysql)
        return jsonify({"result":True,"msg":"Successfully Set Prescription to not to Auto Order"})
    except Exception as e:
        return jsonify({"result":False,"msg":"Failed to Set Prescription to not to Auto Order","error":str(e)})

@app.route('/prescription/<int:prescription_id>',methods=['DELETE'])
@cross_origin(origin='*')
def deletePrescription(prescription_id):
    try:
        result = Prescription.deletePrescription(prescription_id,mysql)
        return jsonify({"result":True,"msg":"Successfully Deleted Prescription"})
    except Exception as e:
        return jsonify({"result":False,"msg":"Failed to Delete Prescription","error":str(e)})

'''
===================
===================
ORDER API ENDPOINTS
===================
===================
'''
@app.route('/orders',methods=['GET'])
def getAllOrders():
    try:
        orders = Order.getAllOrders(mysql)
        return json.dumps({"orders":orders}, default=str)
    except Exception as e:
        return jsonify({"results":None,"msg":"Failed to Retrieve Orders","error":str(e)})

@app.route('/orders/monthly',methods=['GET'])
def getAllOrdersMonthly():
    try:
        orders = Order.getAllOrdersMonthly(mysql)
        return json.dumps({"orders":orders}, default=str)
        
    except Exception as e:
        return jsonify({"results":None,"msg":"Failed to Retrieve Orders","errors":str(e)})

@app.route('/orders/top',methods=['GET'])
def getTopOrders():
    try:
        orders = Order.getTopOrders(mysql)
        return json.dumps({"orders":orders}, default=str)
    except Exception as e:
        return jsonify({"results":None,"msg":"Failed to Retrieve Top Orders","error":str(e)})

@app.route('/orders/<int:user_id>',methods=['GET'])
@cross_origin(origin='*')
def getAllOrdersByUser(user_id):
    try:
        orders = Order.getOrdersUser(user_id,mysql)
        return json.dumps({"orders":orders}, default=str)
    except Exception as e:
        return jsonify({"results":None,"msg":"Failed to Retrieve Orders","error":str(e)},default=str)

@app.route('/order/<int:order_id>',methods=['GET'])
@cross_origin(origin='*')
def getOrder(order_id):
    try:
        order = Order.getOrder(order_id,mysql)
        return json.dumps({"order":order}, default=str)
    except Exception as e:
        print(e)
        return jsonify({"order":None,"msg":"Failed to Retrieve Order","error":str(e)}, default=str)

@app.route('/order',methods=['POST'])
@cross_origin(origin='*')
def addOrder():
    try:
        order = Order(request.json['prescription'], request.json['client'], request.json['orderDate'])
        result = Order.addOrder(order,mysql)

        return jsonify({"result":True,"msg":"Successfully Created Order"})
    except Exception as e:
        print(e)
        return jsonify({"result":False,"msg":"Failed to Create Order","error":str(e)})

@app.route('/order/<int:order_id>',methods=['PUT'])
@cross_origin(origin='*')
def updateOrder(order_id):
    try:
        order = Order(request.json['prescription'], request.json['client'], request.json['orderDate'])
        result = Order.updateOrder(order_id,request.json,mysql)

        return jsonify({"result":True,"msg":"Successfully Updated Order"})
    except Exception as e:
        print(e)
        return jsonify({"result":False,"msg":"Failed to Update Order","error":str(e)})

@app.route('/order/pharmacy/<int:order_id>',methods=['PUT'])
@cross_origin(origin='*')
def assignPharmacy(order_id):
    try:
        result = Order.assignPharmacy(order_id,request.json['pharmacy_id'],mysql)

        return jsonify({"result":True,"msg":"Successfully assigned Pharmacy to Order"})
    except Exception as e:
        print(e)
        return jsonify({"result":False,"msg":"Failed to Assign Pharmacy","error":str(e)})

@app.route('/order/pharmacy/unassign/<int:order_id>',methods=['PUT'])
@cross_origin(origin='*')
def unassignPharmacy(order_id):
    try:
        result = Order.unassignPharmacy(order_id,request.json['pharmacy_id'],mysql)

        return jsonify({"result":True,"msg":"Successfully unassigned Pharmacy from Order"})
    except Exception as e:
        print(e)
        return jsonify({"result":False,"msg":"Failed to Unassign Pharmacy","error":str(e)})

@app.route('/order/cancel/<int:order_id>',methods=['PUT'])
@cross_origin(origin='*')
def cancelOrder(order_id):
    try:
        result = Order.cancelOrder(order_id,mysql)

        return jsonify({"result":True,"msg":"Successfully Cancelled Order"})
    except Exception as e:
        print(e)
        return jsonify({"result":False,"msg":"Failed to Cancel Order","error":str(e)})

@app.route('/order/complete/<int:order_id>',methods=['PUT'])
@cross_origin(origin='*')
def completeOrder(order_id):
    try:
        result = Order.completeOrder(order_id,mysql)

        return jsonify({"result":True,"msg":"Successfully Complete Order"})
    except Exception as e:
        print(e)
        return jsonify({"result":False,"msg":"Failed to Complete Order","error":str(e)})

@app.route('/order/<int:order_id>',methods=['DELETE'])
@cross_origin(origin='*')
def deleteOrder(order_id):
    try:
        result = Order.deleteOrder(order_id,request.json,mysql)

        return jsonify({"result":True,"msg":"Successfully Deleted Order"})
    except Exception as e:
        print(e)
        return jsonify({"result":False,"msg":"Failed to Delete Order","error":str(e)})


'''
=====================
=====================
MESSAGE API ENDPOINTS
=====================
=====================
'''
@app.route('/messages',methods=['GET'])
@cross_origin(origin='*')
def getAllMessages():
    return jsonify({"messages":Message.getAllMessages(mysql)})

@app.route('/messages/<int:client_id>/<int:caretaker_id>',methods=['GET'])
@cross_origin(origin='*')
def getMessagesByUser(client_id, caretaker_id):
    return jsonify({"messages":Message.getMessages(client_id, caretaker_id, mysql)})

@app.route('/messages/<int:client_id>/<int:caretaker_id>',methods=['POST'])
@cross_origin(origin='*')
def addMessageByUser(client_id, caretaker_id):
    if 'messages' not in request.json or 'sender' not in request.json or 'date' not in request.json:
        return jsonify({"result":False,"msg":"Missing Fields"})

    message = Message(client_id, caretaker_id, request.json['messages'], request.json['sender'], request.json['date'])
    
    print("Client ID: "+str(client_id)+" | Caretaker ID: "+str(caretaker_id)+" | Messages: "+request.json['messages']+" | Sender: "+str(request.json['sender'])+" | Date: "+request.json['date'])

    result = Message.addMessages(message,  mysql)
    return jsonify({"result":True,"msg":"Successfully Created Message"})

@app.route('/messages/<int:client_id>/<int:caretaker_id>',methods=['PUT'])
@cross_origin(origin='*')
def updateMessageByUser(client_id, caretaker_id):
    if 'messages' not in request.json or 'sender' not in request.json or 'date' not in request.json:
        return jsonify({"result":False, "msg":"Missing Fields"})

    message = Message(client_id, caretaker_id, request.json['messages'], request.json['sender'], request.json['date'])

    result = Message.updateMessagesByUser(message, mysql)
    return jsonify({"result":True,"msg":"Successfully Updated Message"})

@app.route('/messages/<int:client_id>/<int:caretaker_id>', methods=['DELETE'])
@cross_origin(origin='*')
def deleteMessagesByUser(client_id, caretaker_id):
    result = deleteMessageByUser(client_id, caretaker_id, mysql)
    return jsonify({"result":True,"msg":"Successfully Deleted Messages"})


'''
=====================
=====================
HISTORY API ENDPOINTS
=====================
=====================
'''
@app.route('/history',methods=['GET'])
@cross_origin(origin='*')
def getAllHistory():
    return jsonify({"history":History.getAllHistory(mysql)})

@app.route('/history/client/<int:client_id>', methods=['GET'])
@cross_origin(origin='*')
def getAllHistoryClient(client_id):
    return jsonify({"history":History.getAllHistoryClient(client_id,mysql)})

@app.route('/history/caretaker/<int:caretaker_id>', methods=['GET'])
@cross_origin(origin='*')
def getAllHistoryCaretaker(caretaker_id):
    return jsonify({"history":History.getAllHistoryCaretaker(caretaker_id,mysql)})

@app.route('/history/<int:history_id>', methods=['GET'])
@cross_origin(origin='*')
def getHistory(history_id):
    return jsonify({"history":History.getIndividualHistory(history_id,mysql)})

@app.route('/history', methods=['POST'])
@cross_origin(origin='*')
def addHistory():
    history = History(request.json['client_id'], request.json['caretaker_id'], request.json['notes'])
    result = History.addHistory(history, mysql)

    if result is True:
        return jsonify({"result":True, "msg":"Successfully Added History"})
    else:
        return jsonify({"result":False, "msg":"Failed to Add History"})

@app.route('/history/<int:history_id>', methods=['PUT'])
@cross_origin(origin='*')
def updateHistoryNotes(history_id):
    result = History.updateHistoryNotes(history_id, request.json['notes'], mysql)

    if result is True:
        return jsonify({"result":True, "msg":"Successfully Added Notes to History"})
    else:
        return jsonify({"result":False, "msg":"Failed to Add Notes to History"})

if __name__ == '__main__':
    app.DEBUG=True
    app.run()
    # app.run(host="127.0.0.1",port="8080")