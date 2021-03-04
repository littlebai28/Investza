import yfinance as yf
#根据股票代码找一个股票，例子给的是microsoft
msft = yf.Ticker("MSFT")

# get stock info as a dictionary
# 可以根据info里的industry找到可比公司，还有各种金融数据不同的ratio可以用
info = msft.info
# get historical market data by day in a panda dataframe
# 所有历史的股价走势都有
hist = msft.history(period="max")
# 只有两列记录了 dividend（给股东的分红） 和 stock split（有时候把一股分成两股，用来adjust stock price）
actions = msft.actions
#这个看financial 的function好像不work了，我google了一下找到了一个别人写的function，放在financials那个py file里了
fin = msft.financials
bs = msft.balance_sheet
cf = msft.cashflow
e = msft.earnings
#major share holders, 不太有用
mh = msft.major_holders
ih = msft.institutional_holders
#这个是一些analyst的recommendation，挺有用的，但是action里面的reit和main我没太懂是什么意思
r = msft.recommendations

#这个是同时看多个股票合起来写的方法，就是是高频的marketdata
data = yf.download(  # or pdr.get_data_yahoo(...
        # tickers list or string as well
        tickers = "SPY AAPL MSFT",
        # use "period" instead of start/end
        # valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
        # (optional, default is '1mo')
        period = "ytd",
        # fetch data by interval (including intraday if period < 60 days)
        # valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
        # (optional, default is '1d')
        interval = "1m",
        # group by ticker (to access via data['SPY'])
        # (optional, default is 'column')
        group_by = 'ticker',
        # adjust all OHLC automatically
        # (optional, default is False)
        auto_adjust = True,
        # download pre/post regular market hours data
        # (optional, default is False)
        prepost = True,
        # use threads for mass downloading? (True/False/Integer)
        # (optional, default is True)
        threads = True,
    )