import pandas as pd
import requests
from bs4 import BeautifulSoup

import csv



def get_financials(url):
    page_source = requests.get(url)

    soup_html = BeautifulSoup(page_source.text, 'html.parser')
    tabelle_soup = soup_html.find('div', class_="M(0) Whs(n) BdEnd Bdc($seperatorColor) D(itb)")

    # Get Title Row
    überschriften = tabelle_soup.find('div', class_="D(tbr) C($primaryColor)")
    überschriften = überschriften.findAll('span')
    title_row = list()
    for ü in überschriften:
        title_row.append(ü.text)

    tabelle = pd.DataFrame(None, columns=title_row)
    restliche_zeilen = tabelle_soup.findAll('div', class_="D(tbr) fi-row Bgc($hoverBgColor):h")
    for zeile in restliche_zeilen:
        spalten = zeile.findChildren('div', recursive=False)
        zeilenwerte = list()
        for spalte in spalten:
            zeilenwerte.append(spalte.text)
        tabelle.loc [ len(tabelle) ] = zeilenwerte
    tabelle = tabelle.set_index(title_row [ 0 ])
    return tabelle.T


def get_income_statement(symbol):
    url = 'https://finance.yahoo.com/quote/' + symbol + '/financials'
    return get_financials(url)


def get_balance_sheet(symbol):
    url = 'https://finance.yahoo.com/quote/' + symbol + '/balance-sheet'
    return get_financials(url)


def get_cashflow(symbol):
    url = 'https://finance.yahoo.com/quote/' + symbol + '/cash-flow'
    return get_financials(url)

ti = []
with open('S&P500_stock_info.csv', mode='r') as csv_file:
    csv_reader =  csv.reader(csv_file)
    for row in csv_reader:
        ti.append(row[0])
ti.pop(0)

for symbol in ti:
    n1 = str(symbol) + '_income_statement.csv'
    n2 = str(symbol) + '_balance_sheet.csv'
    n3 = str(symbol) + '_cash_flow.csv'
    income_statement = get_income_statement(symbol)
    balance_sheet = get_balance_sheet(symbol)
    cash_flow = get_cashflow(symbol)
    income_statement.to_csv(str(n1), header=True)
    balance_sheet.to_csv(str(n2), header=True)
    cash_flow.to_csv(str(n3), header=True)