import yfinance as yf
from yahoo_fin import stock_info as si
import os
import tkinter as tk
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy

list = []
list2 = []
FlexyPath = os.path.dirname(os.path.abspath(__file__))
window = tk.Tk() 
window.minsize(1000, 250)
def all_children (wid) :
    _list = wid.winfo_children()

    for item in _list :
        if item.winfo_children() :
            _list.extend(item.winfo_children())

    return _list
def retreveStocks(ticker):
    # try:
    # except:
    #     print("nope")
    stock = yf.Ticker(ticker)
    stock_historical = stock.history(start="2020-01-1", interval="1d")

    stock_historical = stock_historical.drop(['Stock Splits', 'Dividends', 'Volume', 'Open', 'Low', 'High'], axis = 1)
    # indexNamesArr = stock_historical.index.values
    # listOfRowIndexLabels = indexNamesArr
    # for i in listOfRowIndexLabels:
    #     i = numpy.datetime_as_string(i, unit='D')
    #     list.append(i)

    # listHistoricalvalues = stock_historical.values.tolist()

    # for i in range(len(listHistoricalvalues)): #Traversing through the main list
    #     for j in range (len(listHistoricalvalues[i])): #Traversing through each sublist
    #         list2.append(listHistoricalvalues[i][j])

    figure2 = plt.Figure(figsize=(5,4), dpi=100)
    ax2 = figure2.add_subplot(111)   
    line2 = FigureCanvasTkAgg(figure2, window)
    line2.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)
    stock_historical.plot(kind='line', legend=True, ax=ax2, color='r', fontsize=10)
    # company_name = stock.info['longName']
    ax2.set_title(ticker.upper())
    line2.delete("all")
    # print(figure2, ax2, line2)

    # print(getCompany('tsla'))





def StockRetrieve():
    l = e1.get()
    retreveStocks(l)
    print(all_children(window))

    print("hello")

def task():
    l = e1.get()
    try:
        label['text'] = si.get_live_price(l)      

    except:
        print("nope")
    window.after(1000, task)  # reschedule event in 2 seconds
    # convert ndarray to list

# def BuyButton:

# print(list)
# stock_historical = stock_historical.values.tolist()


label = tk.Label(window, text="price")
label.place(x=200,y=30)
label.pack()



# retreveStocks("BTC-AUD")


e1 = tk.Entry(window)
e1.place(x=700,y=100)
e1.pack()

b = tk.Button(window, text="Okay", command=StockRetrieve)
b.place(x=700,y=100)
b.pack()

b2 = tk.Button(window, text="Buy", command=StockRetrieve)
b2.place(x=900,y=30)

b3 = tk.Button(window, text="Buy", command=StockRetrieve)
b3.place(x=800,y=30)
# b2.pack()


window.after(1000, task)
window.mainloop()