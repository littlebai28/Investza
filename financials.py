import pandas as pd
import requests
from bs4 import BeautifulSoup


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


symbol = 'MSFT'
# Functions return dataframe
income_statement = get_income_statement(symbol)
balance_sheet = get_balance_sheet(symbol)
cash_flow = get_cashflow(symbol)