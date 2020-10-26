import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import norgatedata
from datetime import datetime, timedelta
from math import sqrt
import pandas_market_calendars as mcal

from calculating_allocation import allocation, securities_pct
from perf_funcs import cagr, drawdowns, volatility, backtest_perf_plot, create_index

# creating the trading day calendar that we'll use for rebalancing
nyse = mcal.get_calendar(name='NYSE')
schedule = nyse.schedule(start_date=securities_pct.index[0], end_date=securities_pct.index[-1])
schedule = schedule.index

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
        positions.loc[rb_day: rb_end, position] = portfolio_value['Portfolio'][rb_value] * (
                    allocation[position][rb_day] * np.cumprod(1 + securities_pct.loc[rb_day: rb_end, position]))

    portfolio_value.loc[rb_day: rb_end, 'Portfolio'] = np.nansum(positions.loc[rb_day: rb_end], axis=1)

if __name__ == '__main__':
    
    # creating the index to compare our strategy to
    index = create_index(start=portfolio_value.index[0],
                         end=portfolio_value.index[-1],
                         index_ticker='SPY')

    # same initial investment as our backtested strategy
    index = index * invested

    # CAGR
    strat_cagr = cagr(portfolio_value['Portfolio'])
    strat_cagr = '{:.2%}'.format(strat_cagr)

    # drawdowns
    drawdowns = drawdowns(portfolio_value['Portfolio'])
    max_dd = min(drawdowns.fillna(0))
    max_dd = '{:.2%}'.format(max_dd)

    # volatility
    vol = volatility(portfolio_value['Portfolio'])
    vol = '{:.2%}'.format(vol)

    strat_start = portfolio_value.index[0].strftime('%Y-%m-%d')
    strat_end = portfolio_value.index[-1].strftime('%Y-%m-%d')

    # plotting the performance of our backtest with an index
    perf_chart = backtest_perf_plot(equity_curve=portfolio_value,
                                    rolling_dd=drawdowns,
                                    comparison=True,
                                    index=index)
    plt.show()

    print('The CAGR for Risk Parity from {} to {} was {} with an annualized volatility of {}'.format(strat_start,
                                                                                                     strat_end,
                                                                                                     strat_cagr,
                                                                                                     vol))

    print('The Max Drawdown for Risk Parity between {} and {} was {}'.format(strat_start,
                                                                             strat_end,
                                                                             max_dd))
