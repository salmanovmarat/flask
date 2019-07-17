from app import app
from flask import render_template, redirect, url_for, request
import requests
import xmltodict
from datetime import date


@app.route('/', methods=['GET'])
def index():
    if request.method == "GET":
        today = date.today()
        day = today.strftime("%d.%m.%Y")
        url = f"https://www.cbar.az/currencies/{day}.xml"
        currency = requests.get(url)
        mydict = xmltodict.parse(currency.text)
        incomeList = mydict['ValCurs']['ValType'][1]['Valute']
        mylist = []
        for i in incomeList:
            dictionary = {
                'key': i['@Code'],
                'kurs': i['Name'],
                'value': i['Value'],
                'ferq': '~'
            }
            mylist.append(dictionary)

    return render_template('index.html', mylist=mylist)


@app.route('/currency', methods=['POST'])
def currency():
    if request.method == "POST":
        time = request.form.get("time1")
        url = f"https://www.cbar.az/currencies/{time}.xml"
        currency = requests.get(url)
        mydict = xmltodict.parse(currency.text)
        incomeList = mydict['ValCurs']['ValType'][1]['Valute']

        time1 = request.form.get("time2")
        url1 = f"https://www.cbar.az/currencies/{time1}.xml"
        currency1 = requests.get(url1)
        mydict1 = xmltodict.parse(currency1.text)
        incomeList1 = mydict1['ValCurs']['ValType'][1]['Valute']

        mylist = []
        for i in incomeList:
            dictionary = {
                'key': i['@Code'],
                'kurs': i['Name'],
                'value': i['Value']


            }
            mylist.append(dictionary)

        mylist1 = []
        for i in incomeList1:
            dictionary1 = {
                'key': i['@Code'],
                'kurs': i['Name'],
                'value': i['Value']
            }
            mylist1.append(dictionary1)

        for i in range(len(incomeList)):
            if mylist[i]['value'] < mylist1[i]['value']:
                ferq = 'dushub'
            elif mylist[i]['value'] > mylist1[i]['value']:
                ferq = 'qalxib'
            else:
                ferq = 'deyishmeyib'
            swap = mylist[i]
            swap['ferq'] = ferq
            mylist1[i] = ferq

    return render_template('index.html', mylist=mylist)
