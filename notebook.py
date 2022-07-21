import pandas as pd

import matplotlib.pyplot as plt
%matplotlib inline
%config InlineBackend.figure_format = 'svg' 
plt.style.use('fivethirtyeight')
dec6 = pd.read_csv('datasets/coinmarketcap_06122017.csv')

market_cap_raw = dec6[['id', 'market_cap_usd']]
market_cap_raw.count()

cap = market_cap_raw.query('market_cap_usd > 0')
cap.count()

TOP_CAP_TITLE = 'Top 10 market capitalization'
TOP_CAP_YLABEL = '% of total cap'

cap10 = cap[:10].set_index('id')
cap10 = cap10.assign(market_cap_perc = lambda x: (x.market_cap_usd / cap.market_cap_usd.sum())*100)


ax = cap10.market_cap_perc.plot.bar(title=TOP_CAP_TITLE)

ax.set_ylabel(TOP_CAP_YLABEL);

volatility = dec6[['id', 'percent_change_24h', 'percent_change_7d']]
volatility = volatility.set_index('id').dropna()
volatility = volatility.sort_values('percent_change_24h')
volatility.head()

def top10_subplot(volatility_series, title):
    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(10, 6))
    ax = volatility_series[:10].plot.bar(color="darkred", ax=axes[0])
    fig.suptitle(title)
    ax.set_ylabel('% change')
    ax = volatility_series[-10:].plot.bar(color="darkblue", ax=axes[1])
    return fig, ax

DTITLE = "24 hours top losers and winners"
fig, ax = top10_subplot(volatility.percent_change_24h, DTITLE)
volatility7d = volatility.sort_values("percent_change_7d")

WTITLE = "Weekly top losers and winners"
fig, ax = top10_subplot(volatility7d.percent_change_7d, WTITLE);
largecaps = cap.query("market_cap_usd > 1E+10")
largecaps

def capcount(query_string):
    return cap.query(query_string).count().id

LABELS = ["biggish", "micro", "nano"]
biggish = capcount("market_cap_usd > 3E+8")
micro = capcount("market_cap_usd >= 5E+7 & market_cap_usd < 3E+8")
nano =  capcount("market_cap_usd < 5E+7")
values = [biggish, micro, nano]

plt.bar(range(len(values)), values, tick_label=LABELS);
