import datetime,re,requests

from threading import Timer, Thread
from xml.etree import ElementTree as ET
from xml.dom import minidom
import urllib
import time
import mysql.connector #imports mysql connection

mydb = mysql.connector.connect( 
    host = "localhost",
    user = "root",
    passwd = "AMT_TEAM3",
    database = "ur5_mtconnect"
)
mycursor = mydb.cursor()
#connects mysql to computer with Agent, needing the host, user, password, and database

#adjustable variables
sleeptime = 3 #time the program sleeps before it searches the MTConnect Client for new values | Should not be less than the update time of MTConnect Client

#functions block
def database_write(par1,par2,par3,par4,par5,par6,par7): #parsing the six joint angles
    current_time = time.strftime('%Y-%m-%d %H:%M:%S')
    #print(current_time)
    sql = "INSERT INTO UR5(time,j0, j1, j2, j3, j4, j5, gripperstate) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
    val = (current_time,par1,par2,par3,par4,par5,par6,par7) #inserts the time and values for six joints
    mycursor.execute(sql,val)
    mydb.commit()
    print(mycursor.rowcount, "record inserted")

def MTConnectXMLSearch(): #searches for the XML
    tag = str()
    for i in range(20):
        try: 
            response = requests.get("http://192.168.1.4:5000/current") #connects to adress of computer
        except requests.exceptions.ConnectionError: #Shows if there is connection error
            print("Connection Error retrying in " + str(sleeptime) + " secs")
            print(str(i)+"th time trying reconnection")
            time.sleep(sleeptime)
            continue
        except requests.exceptions.MissingSchema: #if the XML is not found
            print("Missing Schema retrying in " + str(sleeptime) + " secs")
            time.sleep(sleeptime)
            print(str(i)+"th time trying reconnection")
            continue
        else: 
            break
    else: 
        raise Exception('Unreconverable Error') #error
    
#parses xml for variables
    root = ET.fromstring(response.content) 
    tag = root.tag.split('}')[0]+'}' #Split strings 
    samples = root.findall(".//"+tag+"Samples")
    events = root.findall(".//"+tag+"Events")

    j0 = str(samples[1][0].text) #converts the the sample into strings and prints the joint angles
    print(j0)

    j1 = str(samples[3][0].text) #converts the the sample into strings and prints the joint angles
    print(j1)

    j2 = str(samples[5][0].text) #converts the the sample into strings and prints the joint angles
    print(j2)

    j3 = str(samples[0][0].text) #converts the the sample into strings and prints the joint angles
    print(j3)

    j4 = str(samples[2][0].text) #converts the the sample into strings and prints the joint angles
    print(j4)

    j5 = str(samples[4][0].text) #converts the the sample into strings and prints the joint angles
    print(j5)

    gripperstate = str(events[0][4].text) #converts the the sample into strings and prints the Gripper state
    print(gripperstate)

    
    if (j0old != j0 or j1old != j1 or j2old != j2 or j3old != j3 or j4old != j4 or j5old != j5): #if the old joint angles don't equal then write the new database
        database_write(j0, j1, j2, j3, j4, j5, gripperstate)
    j0old = j0
    j1old = j1
    j2old = j2
    j3old = j3
    j4old = j4
    j5old = j5


#Main infinite searching loop
while True:
    MTConnectXMLSearch()
    time.sleep(sleeptime)