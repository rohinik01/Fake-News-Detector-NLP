import keras
import numpy as np
import pandas as pd
import yfinance as yf
import streamlit as st
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import load_model

# Title
st.set_page_config(layout="wide")
st.title("📈 Stock Market Price Predictor")
st.markdown("Enter a stock symbol (e.g., `GOOG`, `AAPL`, `TCS.NS`) to view historical data, moving averages, and price predictions.")

# Load model
model_path = 'C:\\Users\\rohin\\Downloads\\Stock Predictions Model.keras'
try:
    model = load_model(model_path)
except:
    st.error(f"❌ Model not found at: {model_path}")
    st.stop()

# Input
stock = st.text_input("Enter Stock Symbol:", "GOOG").upper()
start = '2010-01-01'
end = '2024-12-31'


# Fetch data
try:
    data = yf.download(stock, start=start, end=end)
except:
    st.error("⚠️ Could not fetch stock data. Check symbol.")
    st.stop()

if data.empty:
    st.warning("⚠️ No data found for this stock symbol.")
    st.stop()

st.subheader("📊 Raw Stock Data")
st.write(data.tail())

# Train-test split
data_train = pd.DataFrame(data['Close'][0:int(len(data)*0.80)])
data_test = pd.DataFrame(data['Close'][int(len(data)*0.80):])

# Combine last 100 days + test data
scaler = MinMaxScaler(feature_range=(0,1))
pas_100_days = data_train.tail(100)
data_test_full = pd.concat([pas_100_days, data_test], ignore_index=True)
data_test_scaled = scaler.fit_transform(data_test_full)

# MA50 Plot
st.subheader("📈 MA50 vs Closing Price")
ma_50 = data['Close'].rolling(50).mean()

fig1 = plt.figure(figsize=(10,5))
plt.plot(data['Close'], label='Close Price', color='green')
plt.plot(ma_50, label='MA50', color='red')
plt.xlabel('Date')
plt.ylabel('Price')
plt.title(f"{stock} Closing Price vs 50-Day Moving Average")
plt.legend()
plt.grid(True)
st.pyplot(fig1)

# Prepare input data
x = []
y = []
for i in range(100, data_test_scaled.shape[0]):
    x.append(data_test_scaled[i-100:i])
    y.append(data_test_scaled[i, 0])

x, y = np.array(x), np.array(y)

# Predict
predicted_prices = model.predict(x)

# Reverse scale
scale_factor = 1 / scaler.scale_[0]
predicted_prices = predicted_prices * scale_factor
y_actual = y * scale_factor

# Prediction plot
st.subheader("📉 Actual vs Predicted Prices")
fig2 = plt.figure(figsize=(10,5))
plt.plot(y_actual, label='Actual Price', color='blue')
plt.plot(predicted_prices, label='Predicted Price', color='orange')
plt.xlabel('Time')
plt.ylabel('Stock Price')
plt.title(f"{stock} Price Prediction")
plt.legend()
plt.grid(True)
st.pyplot(fig2)
