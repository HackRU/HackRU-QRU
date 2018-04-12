import requests
import json
from pymongo import MongoClient

import sys
from os import path
from datetime import datetime, timedelta
from win32com.client import Dispatch
from tkinter import Tk
import tkinter.messagebox as mbox


#email = input('Input email address')
email = 'testing@hackru.org'
password = 'defacto'

curdir = None
if getattr(sys, 'frozen', False):
	# frozen
	curdir = path.dirname(sys.executable)
else:
	# unfrozen
	curdir = path.dirname(path.abspath(__file__))


mylabel = path.join(curdir,'betterLabel.label')

print(mylabel)

url = 'https://m7cwj1fy7c.execute-api.us-west-2.amazonaws.com/mlhtest'

fake_user = {
	'email': email,
	'password': password,
}
auth = requests.post(url + '/create', json=fake_user)
token = auth.json()['body']

query_d = {
            'email': email,
            #'token': token,
            'query': {'email': email}
    }

read = requests.post(url + '/read', json=(query_d))
print(read.text)


import xml.etree.ElementTree as ET
tree = ET.parse(mylabel)
root = tree.getroot()
#print(root[5][0][14][0][0].text)
first_name = root[5][0][14][0][0]
qr_text = root[6][0][9]
last_name = root[7][0][14][0][0]


first_name.text = 'Billy Bob'
last_name.text = 'hehehe xd'
qr_text.text = 'wtf'

tree.write(mylabel)
#print(root)

#client = MongoClient(url) #DB_URI
#print(client)
#db = client['camelot-test']
#db.authenticate(email, password)  #DB_USER = , DB_PASS =
#test = db['test']
#u = test.find_one({'email': email})
#print(u)
#test.delete_one({'email': email})

labelCom = Dispatch('Dymo.DymoAddIn')
labelText = Dispatch('Dymo.DymoLabels')
isOpen = labelCom.Open(mylabel)
selectPrinter = 'DYMO LabelWriter 450'
labelCom.SelectPrinter(selectPrinter)


labelCom.StartPrintJob()
labelCom.Print(1,False)
labelCom.EndPrintJob()