import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import norgatedata
from datetime import datetime
from math import sqrt

from calculating_allocation import allocation, securities_pct


# the frequency with which we rebalance the portfolio
rebal_freq = 21

# the initial investment
invested = 1000

# the dollar value of the portfolio
portfolio = pd.DataFrame(data=None, columns=['Portfolio'], index=securities_pct.index)
portfolio.loc[0]['Portfolio'] = invested


for t in range(1, len(securities_pct), rebal_freq):


    t_end = t + rebal_freq





    pass

