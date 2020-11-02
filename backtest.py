import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import norgatedata
from datetime import datetime, timedelta
from math import sqrt
import pandas_market_calendars as mcal

from calculating_allocation import allocation, securities_pct
from perf_funcs import cagr, drawdowns, volatility, backtest_perf_plot, create_index

# the frequency with which we rebalance the portfolio
rebal_freq = 21

# the initial investment
invested = 1000

# the common date index between returns, securities_pct
dates = securities_pct.index

# the securities present in the backtest
securities = securities_pct.columns

# the dollar value of the portfolio
portfolio_value = pd.DataFrame(data=None, columns=['Portfolio'], index=dates)
portfolio_value.iloc[0]['Portfolio'] = invested

# the $ value allocated in each position
positions = pd.DataFrame(data=None, columns=securities, index=dates)

# pnl_stocks will hold the net PnL Data for each stock over the entire backtest
pnl_positions = pd.DataFrame(data=0, columns=securities, index=dates)

# print(allocation.index)

for t in range(0, len(securities_pct), rebal_freq):

    if t == 0:
        rb_day = dates[t]
    else:
        rb_day = dates[t + 1]

    # the day that we rebalance the portfolio, use this value in portfolio_value to calculate allocation
    rb_value = dates[t]

    try:
        rb_end = dates[t + rebal_freq]
    except IndexError:
        rb_end = dates[-1]

    for position in positions:
        positions.loc[rb_day: rb_end, position] = portfolio_value['Portfolio'][rb_value] * (
                allocation[position][rb_day] * np.cumprod(1 + securities_pct.loc[rb_day: rb_end, position]))

        pnl_positions.loc[rb_day:rb_end, position] = (positions.loc[rb_day:rb_end, position] -
                                                      portfolio_value['Portfolio'][rb_value] * allocation[position][
                                                          rb_day]
                                                      ) + pnl_positions.loc[rb_value, position]

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
                                    position_pnl=pnl_positions,
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
