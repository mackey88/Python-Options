
# Used code from philk111 to help with using BeautifulSoup
# Link below:
# https://github.com/philk111/Nasdaq-options-scraper-with-Python/blob/master/options_scrape.py

import json
import requests
from bs4 import BeautifulSoup as soup
import pandas as pd
import time


# Create empyt data frame to hold all the data


columns = ['date', 'Symbol', 'Price', 'Strike', 'last', 'gain', 'bid', 'bidSize', 'ask', 'askSize', 'volume', 'interest', 'state', 'StrikePercent']

df = pd.DataFrame(columns=columns)


# Create a list of symbols we want to get data on
# List is mostly based of the 2016 most traded options by volume from CBOE in their
# '2016 Market Statistics' report


symbols = ["AAPL","BAC","FB","NFLX","TWTR","AMZN","MSFT","TSLA","BABA","C","GE","FCX","PG","MU","INTC","JPM","XOM","WFC","T","CHK","X","CSCO","GILD","F","PFE","DIS","CVX","GOLD","AAL","VZ","NVDA","SBUX","GM","AMD","DAL","WMT","BMY","CAT","GPRO","AA","ET","JCP","RIG","IBM","NKE","GOOGL","GS","PBR","HD","WYNN","KMI","QCOM","CRM","MCD","COP","V","DB","BIDU","KO","ORCL","GOOG","SRPT","FIT","CLF","WLL","CELG","JNJ","BA","MS","HAL","VALE","MRK","LVS","CMG","BAX","MRO","TEVA","SUN","JD","MDLZ","ATVI","SLB","NEM","UPS","AGN","ABBV","MGM", "RAD","TGT","GG","PYPL","M","EBAY","BX","BP", "SQ", "SHOP"]


# Loop through each Symbol and add date to dataframe


for s in range(0, len(symbols)):
    
    print("Starting " + symbols[s])
    print(s)
    url = 'https://www.nasdaq.com/symbol/' + symbols[s] + '/option-chain?callput=call'
    response = requests.get(url)

    page_soup = soup(response.content, "html.parser")


    quote = page_soup.find("div", {"id": "qwidget_lastsale"})

    quote = quote.text.strip('$')

    containers = page_soup.findAll("div", {"class": "OptionsChain-chart borderAll thin"})

    for container in containers:
        table_container = container.findAll("tr")

    table_container = container.findAll("tr")

    rows = []
    for row in table_container:

        rows.append(row.findAll("td"))


    for i in range(1, len(rows)):

        date = rows[i][0].text
        symbol = rows[i][1].text
        price = float(quote)
        strike = float(rows[i][2].text)
        
        if rows[i][3].text == '':
            last = .01
        else:
            last = float(rows[i][3].text)
        
        if rows[i][5].text == '':
            bid = .01
        else:
            bid = float(rows[i][5].text)
        bidSize = int(rows[i][6].text)

        if rows[i][7].text == '':
            ask = .01
        else:
            ask = float(rows[i][7].text)

        askSize = int(rows[i][8].text)
        volume = int(rows[i][9].text)

        if rows[i][10].text == '':
            interest = 0
        else:
            interest = int(rows[i][10].text)

        if price < strike:
            state = "OTM"
            gain = bid / price * 100
        elif price == strike:
            state = "ATM"
            gain = bid / price *100
        else:
            state = "ITM"
            gain =  (bid - (price - strike)) / price * 100
            
        StrikePercent = price / strike * 100

        df.at[len(df)] = [date, symbol, price, strike, last, gain, bid, bidSize, ask, askSize, volume, interest, state, StrikePercent]
        
    time.sleep(2)  # Using 2 second sleep as to not make constant requests against the website
    
    print("Finished " + symbols[s])
    


# Write dataframe to file using the time as part of file name


fileName = 'Options-' + time.ctime().replace('  ', ' ').replace(' ', '-') + '.csv'
df.to_csv(fileName)

