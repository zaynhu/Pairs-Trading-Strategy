
# region imports
from AlgorithmImports import *
# endregion
from QuantConnect.Algorithm import QCAlgorithm
from QuantConnect.Data.Market import TradeBar
from QuantConnect.Indicators import RollingWindow
from sklearn import linear_model
import numpy as np
import pandas as pd
from math import floor
from QuantConnect import Resolution  # Add this import statement

class PairsTradingAlgorithm(QCAlgorithm):
    
    def Initialize(self):
        
        self.SetStartDate(2013, 9, 1)
        self.SetEndDate(2018, 9, 1)
        self.SetCash(10000)
        self.numdays = 252  # set the length of the training period
        tickers = ["HPQ", "ORCL"]
        self.symbols = []
        self.threshold = 1.

        for i in tickers:
            self.symbols.append(self.AddEquity(i, Resolution.Daily).Symbol)
            # Daily Securities Format 
            # Add equity, daily resolution
            # Store symbols

        for symbol in self.symbols:
            symbol.hist_window = RollingWindow[TradeBar](self.numdays + 1)
            # Rolling window store historical price data, length = numdays

    def OnData(self, data):
        if not (data.ContainsKey("HPQ") and data.ContainsKey("ORCL")): #Price Data
            return

        for symbol in self.symbols:
            symbol.hist_window.Add(data[symbol])
            # Rolling window

        price_x = pd.Series([float(i.Close) for i in self.symbols[0].hist_window], 
                            index=[i.Time for i in self.symbols[0].hist_window])

        price_y = pd.Series([float(i.Close) for i in self.symbols[1].hist_window], 
                            index=[i.Time for i in self.symbols[1].hist_window])

        if len(price_x) < 252:
            return

        spread = self.regr(np.log(price_x), np.log(price_y)) #regression on the log of the prices
        mean = np.mean(spread)
        std = np.std(spread)
        ratio = floor(self.Portfolio[self.symbols[1]].Price / self.Portfolio[self.symbols[0]].Price) #price ratio

        if spread[-1] > mean + self.threshold * std: 
            if not self.Portfolio[self.symbols[0]].Quantity > 0 and not self.Portfolio[self.symbols[0]].Quantity < 0: 
                #no existing position before executing the next set of actions
                self.Sell(self.symbols[1], 100) 
                self.Buy(self.symbols[0], ratio * 100)
                #same dollar value in each position

        elif spread[-1] < mean - self.threshold * std:
            if not self.Portfolio[self.symbols[0]].Quantity < 0 and not self.Portfolio[self.symbols[0]].Quantity > 0:
                self.Sell(self.symbols[0], 100)
                self.Buy(self.symbols[1], ratio * 100) #desired ratio between S1 and S2

        else:
            self.Liquidate() #no holdings/existing position of the stock

    def regr(self, x, y):
        regr = linear_model.LinearRegression()
        x_constant = np.column_stack([np.ones(len(x)), x])
        regr.fit(x_constant, y)
        beta = regr.coef_[0]
        alpha = regr.intercept_
        spread = y - x * beta - alpha
        return spread
