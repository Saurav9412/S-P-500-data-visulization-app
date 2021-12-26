import streamlit as st
import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
import base64
import yfinance as yf

st.title('S&P 500 App')

expander_bar = st.expander("About")
expander_bar.markdown("""
This App retrieves the list of the **S&P 500** (from Wikipedia) and its corresponding **stock closing price (year-to-date)!**
* **Python libraries:** base64, pandas, streamlit, numpy, seaborn, matplotlib
* **Data Source:** [wikipedia](https://www.wikipedia.org) and yfinance. 
* **Credit:** [wikipedia](https://www.wikipedia.org). 
""")
st.sidebar.header('User Input Features')

@st.cache
def load_data():
	url = "https://en.wikipedia.org/wiki/List_of_S&P_500_companies"
	html = pd.read_html(url, header = 0)
	df = html[0]
	return df
df = load_data()
sector = df.groupby('GICS Sector')

# Examining Sector
unique_sector = df['GICS Sector'].unique()
selected_sector = st.sidebar.multiselect('GICS Sector', unique_sector, unique_sector)

#Filtering DataFrame
df_selected_sector = df[ (df['GICS Sector'].isin(selected_sector)) ]

# Diplaying DataFrame
st.header('Displaying Companies in Selected Sector')
st.write(f'Data Dimension: {df_selected_sector.shape[0]} rows and {df_selected_sector.shape[1]} columns.')
st.dataframe(df_selected_sector.astype(str))

# DataFrame Download
def file_download(df):
	csv = df.to_csv(index = False)
	b64 = base64.b64encode(csv.encode()).decode()
	href = f'<a href = "data:file/csv;base64,{b64}" download = "SP500.csv">Download CSV File</a>'
	return href
st.markdown(file_download(df_selected_sector), unsafe_allow_html = True)

# https://pypi.org/project/yfinance/
data = yf.download(#or pdr.get_data_yahoo(...
	#ticker list or string as well
	tickers = list(df_selected_sector[:10].Symbol),

	# use "period" instead of start/end
	# valid period: 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 5y, 10y, ytd, max
	# (optional, default is "1mo")
	period = 'ytd',

	# fetch data by interval (including intraday if period < 60 days)
	# valid intervals : 1mo, 2mo, 5mo, 15mo, 30mo, 60mo, 90mo, 1h, 1d, 5d, 1wk, 1mo, 3mo
	# (optional, default is "1d")
	interval = "1d",

	# group by ticker ( to access via data['SPY'])
	# (optional, default is "column")
	group_by = 'ticker',

	# adjust all OHLC automatically
	# (optional, default is False)
	auto_adjust = True,

	# download pre/post regular market hours data
	# (optional, defualt is False)
	prepost = True,

	# use threads for mass downloading? (True/False/Integer)
	# (optional, default is True)
	threads = True,

	# proxy URL scheme use when downloading?
	# (optional, default is None)
	proxy = None
)


# ploting closeing price of Query Symbol
st.set_option('deprecation.showPyplotGlobalUse', False)
def price_plot(symbol):
	df = pd.DataFrame(data[symbol].Close)
	df['Date'] = df.index
	plt.fill_between(df.Date, df.Close, color = 'skyblue', alpha = 0.3)
	plt.plot(df.Date, df.Close, color = "skyblue", alpha = 0.8)
	plt.xticks(rotation=90)
	plt.title(symbol, fontweight = "bold")
	plt.xlabel('Date', fontweight = "bold")
	plt.ylabel('Closing Price', fontweight = "bold")
	return st.pyplot()

number_of_companies = st.sidebar.slider('Number of Companies', 1, 10)

if st.button('Show Plots'):
	st.header('Stock Closing Price')
	for i in list(df_selected_sector.Symbol)[:number_of_companies]:
		price_plot(i)
