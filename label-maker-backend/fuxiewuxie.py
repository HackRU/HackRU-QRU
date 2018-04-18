import requests
#import json
import sys
from os import path
from win32com.client import Dispatch
import xml.etree.ElementTree as ET
from flask import Flask

app = Flask(__name__)

@app.route('/<email>')
def print_label(email):
    #email = input('Input email address')
    #email = 'yang.benjamin1998@gmail.com'
    #password = 'defacto'

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

    #fake_user = {
    #	'email': email,
    #	'password': password,
    #}
    #auth = requests.post(url + '/create', json=fake_user)
    #token = auth.json()['body']

    #read = requests.post(url + '/read', json=(query_d))
    #print(read.text)

    query_d = {
        'email' : email,
        'query' : {'email': email}
    }

    qrimage = requests.post(url + '/qr', json=(query_d))
    #print(qrimage.json()['body'][22:])


    tree = ET.parse(mylabel)
    root = tree.getroot()
    first_name = root[5][0][14][0][0]
    last_name = root[6][0][14][0][0]
    qr_text = root[7][0][9]


    first_name.text = email
    last_name.text = email
    qr_text.text = qrimage.json()['body'][22:]

    tree.write(mylabel)
    #print(root)

    print(mylabel)


    labelCom = Dispatch('Dymo.DymoAddIn')
    labelText = Dispatch('Dymo.DymoLabels')
    isOpen = labelCom.Open(mylabel)
    selectPrinter = 'LabelWriter 450 Turbo'
    labelCom.SelectPrinter(selectPrinter)


    labelCom.StartPrintJob()
    labelCom.Print(1,False)
    labelCom.EndPrintJob()
    return 'hello world'