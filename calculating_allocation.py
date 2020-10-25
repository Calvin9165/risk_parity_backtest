import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import norgatedata
from datetime import datetime
from math import sqrt

from load_data import securities_pct

# # resetting the Date column to the index for the time being
securities_pct.set_index(keys='Date', inplace=True)

# volatility lookback period
lookback = 63


def calculate_allocation(df_pct, vol_period, target_vol, rebal_freq):
    # DataFrame which holds the rolling annualized historical volatility based on vol_period days
    security_vol = df_pct.rolling(vol_period).std() * sqrt(252)
    security_vol.dropna(inplace=True)

    # creating a DataFrame which stores the theoretical daily allocation to each asset based on the assets volatility
    # and the portfolio's target volatility
    num_stocks = len(security_vol.columns)
    allocation = target_vol / num_stocks / security_vol

    # only want to keep allocation values for every rebal_freq days, then fill forward until next rebal_freq multiple
    allocation_slice = allocation.iloc[0::rebal_freq]

    final_allocation = pd.DataFrame(data=allocation_slice, index=allocation.index)
    final_allocation.fillna(method='ffill', inplace=True)

    final_allocation['Cash'] = 1 - final_allocation.sum(axis=1)

    return final_allocation


allocation = calculate_allocation(df_pct=securities_pct,
                                  vol_period=lookback,
                                  target_vol=0.15,
                                  rebal_freq=21)

securities_pct = securities_pct.iloc[lookback:]
