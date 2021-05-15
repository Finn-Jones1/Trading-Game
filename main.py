import yfinance as yf

aapl= yf.Ticker("aapl")
aapl_historical = aapl.history(start="2020-06-02", end="2020-06-07", interval="1m")
print(aapl_historical)
for ticker in tickers_list:
    ticker_object = yf.Ticker(ticker)

    #convert info() output from dictionary to dataframe
    temp = pd.DataFrame.from_dict(ticker_object.info, orient="index")
    temp.reset_index(inplace=True)
    temp.columns = ["Attribute", "Recent"]
    
    # add (ticker, dataframe) to main dictionary
    tickers_data[ticker] = temp

print(tickers_data)