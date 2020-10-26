import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import norgatedata
from datetime import datetime, timedelta
from math import sqrt
import pandas_market_calendars as mcal

from calculating_allocation import allocation, securities_pct

# creating the trading day calendar that we'll use for rebalancing
nyse = mcal.get_calendar(name='NYSE')
schedule = nyse.schedule(start_date=securities_pct.index[0],end_date=securities_pct.index[-1])
schedule = schedule.index

print(schedule[:30])
print(schedule[0])
print(schedule[0] + timedelta(21))

# the frequency with which we rebalance the portfolio
rebal_freq = 21

# the initial investment
invested = 1000

# the dollar value of the portfolio
portfolio_value = pd.DataFrame(data=None, columns=['Portfolio'], index=securities_pct.index)
portfolio_value.iloc[0]['Portfolio'] = invested

# the $ value allocated in each position
positions = pd.DataFrame(data=None, columns=securities_pct.columns, index=securities_pct.index)


for t in range(1, len(securities_pct), rebal_freq):

    rb_day = securities_pct.index[t]
    rb_value = securities_pct.index[t - 1]

    try:
        rb_end = securities_pct.index[t + rebal_freq]
    except IndexError:
        rb_end = securities_pct.index[-1]

    for position in positions:
        positions.loc[rb_day: rb_end, position] = portfolio_value['Portfolio'][rb_value] * (allocation[position][rb_day] * np.cumprod(1 + securities_pct.loc[rb_day: rb_end, position]))

    portfolio_value.loc[rb_day: rb_end, 'Portfolio'] = np.nansum(positions.loc[rb_day: rb_end], axis=1)


portfolio_value.plot()
plt.show()

