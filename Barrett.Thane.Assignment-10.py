'''
File: Barrett.Thane.Assignment-10.py
Name: Thane Barrett
Date: 05/31/2020
Course: Python Programming ICT-4370

Program Description:  This program extends the functionality of assignment 8 by retrieving data from Yahoo Finance.  
Given a list of ticker symbols and a start date, the program retrieves data from Yahoo Finance using its API.  The
data is then written to csv files, one for each stock.  The CSV files are read and the data is compiled into 
a single JSON file that is then used to generate the graph.

'''
#SECTION 1: The program is devided into three sections.  This first section contains the import statements and class definition.

#Supports JSON and CSV file read/write
import json
import csv

#Supports graph plotting
import matplotlib.pyplot as plt
import matplotlib

#Supports date calculations
from datetime import datetime
from datetime import date

#Supports data read
from pandas_datareader import data as pdr
import pandas as pd

#Supports read from Yahoo Finance
import yfinance as yf
yf.pdr_override()


#Define New stock Class
class Stock():
    # Describe the Stock class layout - 7 attributes
    def __init__(self, symbol):
        # initialize attributes to describe a stock
        self.symbol = symbol
        self.dates = []
        self.openingPrices = []
        self.highs = []
        self.lows = []
        self.closingPrices = []
        self.volumes = []

    def addData(self, date, opening, high, low, close, volume):
        self.dates.append(date)
        self.openingPrices.append(opening)
        self.highs.append(high)
        self.lows.append(low)
        self.closingPrices.append(float("{:.2f}".format(float(close))))
        self.volumes.append(volume)

#==============================================================================================================

#SECTION 2:  This section of the program gets data from Yahoo Finance based on the tracker_list, the start_date and today's date.  A CSV file is created for each stock.
#Each CSV file contains historical data for the stock.  The individual CSV files are then compiled into one JSON file.

# Tickers list
ticker_list=['AIG', 'F', 'FB', 'GOOG', 'IBM', 'M', 'MSFT', 'RDS-A']

today = date.today()

start_date= '2020-05-01'

#Gets data from Yahoo Finance using the start_date defined above and today's date
files=[]
def getData(ticker):
    print (ticker)
    data = pdr.get_data_yahoo(ticker, start=start_date, end=today)
    dataname= ticker + '_' + str(today)
    files.append(dataname)
    SaveData(data, dataname)

# Create a file in current dir.
def SaveData(df, filename):
    df.to_csv(filename + '.csv')

#This loop will iterate over ticker list, will pass one ticker to get data, and save that data as a CSV file.

for tik in ticker_list:
    getData(tik)

for i in range(0,8):
    df1= pd.read_csv(str(files[i]) + '.csv')

fileNames = []
for symbol in ticker_list:
    fileName = symbol + "_" + str(today) + ".csv"
    fileNames.append(fileName)

#Collects data in CSV files and compiles data to one JSON file
jsonFileName = "stock_data_" + str(today) + ".json"
data = {}

for i in range(0, len(fileNames)):
    with open(fileNames[i]) as csvFile:
        csvReader = csv.DictReader(csvFile)
        num = 0
        for rows in csvReader:
            id = rows['Date']
            rows['Symbol'] = ticker_list[i]
            data[fileNames[i] + "_" + str(num)] = rows
            num += 1

with open(jsonFileName, 'w') as jsonFile:
    jsonFile.write(json.dumps(data, indent=4))

#==============================================================================================================

#SECTION 3: This third and final section reads the JSON file and creates a dictionary based on the data found.  
#The dictionary is then used to generate the graph.

#Opens AllStocks.json
filePath = jsonFileName
with open(filePath) as f:
    dataSet = json.load(f)

investmentDictionary = {}

#iterate through json file and add each time a new symbol is encountered, add it to the investmentDictionary
for investment in dataSet:
    investmentStr = str(investment)
    symbol = investmentStr[0:investmentStr.index("_")]
    if symbol not in investmentDictionary:
        newInvestment = Stock(symbol)
        investmentDictionary[symbol] = {'Stock': newInvestment}
    currentStock = investmentDictionary[symbol]['Stock']
    subDict = dataSet[investmentStr]
    currentStock.addData(datetime.strptime(subDict["Date"], '%Y-%m-%d'), subDict["Open"], subDict["High"], subDict["Low"], subDict["Close"], subDict["Volume"])

for investment in investmentDictionary:
    closes = investmentDictionary[investment]['Stock'].closingPrices
    dates = matplotlib.dates.date2num(investmentDictionary[investment]['Stock'].dates)
    name = investmentDictionary[investment]['Stock'].symbol
    plt.plot_date(dates, closes, linestyle='solid', marker='None', label = name)
    #Adds label to x axis
    plt.xlabel("Date")
    #Adds label to y axis
    plt.ylabel("Closing Price")

#Adds a legend to the plot with the title "Stocks"
plt.legend(title='Stocks')
#Saves the polt as a PNG file
plt.savefig("investmentGraph.png")
#Dispalys the plot
plt.show()