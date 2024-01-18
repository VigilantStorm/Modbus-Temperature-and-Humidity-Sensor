"""
#Program: SQL Database created and manipulated(Inserting data within database table)
#Program: This program is meant to run on SERVER NOT CLIENT!! Client should send data to server so server can serve those request.
#Program author: Lloyd Bolodeoku Security Engineer
Program last modified: 11/29/2023

#Security: Each user has their own associated salt and is 
"""
import sqlite3
import datetime
import requests
import time
import socket
from pymodbus.client import ModbusSerialClient
import logging
import logging.handlers as Handlers

def connection(): 

    # ----------------------------------------------------------------------- #
    # This will simply send everything logged to console
    # ----------------------------------------------------------------------- #
    logging.basicConfig()
    log = logging.getLogger()
    log.setLevel(logging.DEBUG)
    # ----------------------------------------------------------------------- #

    # ----------------------------------------------------------------------- #

    s = socket.socket()
    print("Socket successfully connected")

    port = 50001

    s.bind(('', port))
    print("Socket binded to ", port)

    s.listen(5)
    print("socket is listening")

    while True:
        c, address = s.accept()
        print("Got connection from", address)

        client = ModbusSerialClient(method = 'rtu', port = '/dev/ttySC0', baudrate = 4800, parity = 'N', bytesize = 8, stopbits = 1, timeout = 50)
        client.connect() #Connect to modbus client

        result = client.read_holding_registers(0,10,1)

        humidity_sensor_value = result.registers[0]
        temperature_sensor_value = result.registers[1]

        insert_data_sensor(temperature_sensor_value, humidity_sensor_value)
        return c

def create_table(): #Creates database table for sensor data.

    cursor_obj.execute("CREATE TABLE IF NOT EXISTS LOGIN (Username VARCHAR(255), Password VARCHAR(255))")
    cursor_obj.execute("CREATE TABLE IF NOT EXISTS SENSOR (Timestamp_sensor DATETIME, Username VARCHAR(255), Temperature_sensor INT, Humidity_sensor INT)")
    cursor_obj.execute("CREATE TABLE IF NOT EXISTS API (Timestamp_api DATETIME, Username VARCHAR(255), Temperature_api INT, Humidity_api INT)")

"""
#Refinement next version update: Hash password in database.  
"""
def insert_data_login(username, password): #Insert username + password into database table LOGIN.  #Client sends credentials to server.
    cursor_obj.execute("INSERT INTO LOGIN VALUES (?,?)",(username, password))
    connection_obj.commit()
    authorized = auth_check(username, password)
    return authorized

def insert_data_sensor(timestamp_sensor, username, temperature_sensor, humidity_sensor): #Insert sensor data into database table SENSOR.
    cursor_obj.execute("INSERT INTO SENSOR VALUES (?,?,?,?)",(timestamp_sensor, username, temperature_sensor, humidity_sensor))
    connection_obj.commit()

def insert_data_api(timestamp_api, username, temperature_api, humidity_api): #Insert api data into database table API.
        cursor_obj.execute("INSERT INTO API VALUES (?,?,?,?)",(timestamp_api, username, temperature_api, humidity_api))
        connection_obj.commit()


#cursor_obj.close()

def get_time(): #Gets the systems current date and time.
    current_time = datetime.datetime.now()
    #print("Current time: ", current_time)
    return current_time

def get_api(): #Gets the current weather and time from specified location.

    url = "https://api.tomorrow.io/v4/weather/realtime?location=baltimore&apikey=place api key here"
    header = "accept: application/json"

    response = requests.get(url, header)
    json_data = response.json() if response and response.status_code == 200 else None
    api_time = json_data['data']['time']
    api_temperature = json_data['data']['values']['temperature']
    api_humidity = json_data['data']['values']['humidity']
    return api_time, api_temperature, api_humidity

"""
#Refinement next version update:  Password data is encrypted once it resides in database.  When validating user + password, the passwords hash is compared with password hash of inputted password from login.
"""
def auth_check(username, password): #Gets data from user input from login dashboard and validates if the user is authorized.  If authorized the user has access to program.

    if cursor_obj.execute("SELECT Username, Password FROM LOGIN WHERE Username == (?) and Password == (?)", (username, password)) == 1:
        authorized = True #The user is authenticated and authorized!
    else:
        authorized = False #The user is not authenticated and authorized!
    return authorized #Tells the program that the user is authenticated and authorized!

def response_to_client(username,c): #Pulls the current temperature and humidity value from the SENSOR and API database with a username correlation for data protection security.

    sensor_temperature_payload = "SELECT MAX(Temperature) FROM SENSOR WHERE Username == (?)", (username)
    sensor_humidity_payload = "SELECT MAX(humdity) FROM SENSOR WHERE Username == (?)", (username)
    api_temperature_payload = "SELECT MAX(Temperature) FROM API WHERE Username == (?)", (username)
    api_humidity_payload = "SELECT MAX(humdity) FROM API WHERE Username == (?)", (username)

    c.send(sensor_temperature_payload.encode()) #Transfers payload to client 
    c.send(sensor_humidity_payload.encode()) #Transfers payload to client
    c.send(api_temperature_payload.encode()) #Transfers payload to client 
    c.send(api_humidity_payload.encode()) #Transfers payload to client

    return sensor_temperature_payload, sensor_humidity_payload, api_temperature_payload, api_humidity_payload
                                                                      



#Main program functions
username = "dev"
connection_obj = sqlite3.connect("test6.db")
cursor_obj = connection_obj.cursor()
create_table()

c=connection()
response_to_client(username, c)

c.close()
#c.send(var.encode())
#     c.send(test.encode())
#     c.close()
#     break



#api_timestamp, api_temperature, api_humidity =get_api()
"""
connection_obj = sqlite3.connect("test6.db")
cursor_obj = connection_obj.cursor()

timestamp = get_time()
temperature_sensor, humidity_sensor = get_sensor()
create_table()
insert_data(username, password, timestamp, temperature_sensor, humidity_sensor, api_timestamp, temperature_api, humidity_api)
"""

