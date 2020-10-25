import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import norgatedata
from datetime import datetime
from math import sqrt

from calculating_allocation import allocation, securities_pct

# saving the date column as a seperate series so we can add it back
dates = securities_pct.index

# removing the Date Index and subsequently the date column from securities DataFrame
securities_pct.reset_index(inplace=True)
securities_pct.drop(labels='Date', axis=1, inplace=True)

# setting the pct change value of cash fo 0% for each day
securities_pct['Cash'] = 0

# removing the Date Index and subsequently the date column from the allocation index
allocation.reset_index(inplace=True)
allocation.drop(labels='Date', axis=1, inplace=True)


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

    t_end = t + rebal_freq

    for position in positions:
        positions.loc[t: t_end, position] = portfolio_value['Portfolio'][t-1] * (allocation[position][t] * np.cumprod(1 + securities_pct.loc[t: t_end, position]))

    portfolio_value.loc[t: t_end, 'Portfolio'] = np.nansum(positions.loc[t: t_end], axis=1)


portfolio_value.plot()
plt.show()

