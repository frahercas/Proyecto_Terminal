import pandas as pd
from statsmodels.tsa.stattools import adfuller
from pmdarima import auto_arima
from sklearn.metrics import mean_squared_error
from math import sqrt
import statsmodels.tsa.arima.model as arima

# Read Data
df = pd.read_excel('Datos_Preparatorios.xlsx', index_col='Fecha', parse_dates=True)
df = df.dropna()

# Check Data and Plot
print('Shape of data', df.shape)
print(df.head())
df['Temperatura'].plot(figsize=(12, 5))

# Augmented Dickey-Fuller Test
def ad_test(dataset):
    dftest = adfuller(dataset, autolag='AIC')
    print("1. ADF : ", dftest[0])
    print("2. P-Value : ", dftest[1])
    print("3. Num Of Lags : ", dftest[2])
    print("4. Num Of Observations Used For ADF Regression:", dftest[3])
    print("5. Critical Values :")
    for key, val in dftest[4].items():
        print("\t", key, ": ", val)

ad_test(df['Temperatura'])

# Auto ARIMA Model
stepwise_fit = auto_arima(df['Temperatura'], trace=True, suppress_warnings=True)

# Train-Test Split
train = df.iloc[:-30]
test = df.iloc[-30:]
print(train.shape, test.shape)

# ARIMA Model Training and Prediction
arima_model = arima.ARIMA(train['Temperatura'], order=(3, 0, 3))
arima_model = arima_model.fit()

start = len(train)
end = len(train) + len(test) - 1
pred = arima_model.predict(start=start, end=end, typ='levels').rename('ARIMA Predictions')

# Model Evaluation
rmse = sqrt(mean_squared_error(pred, test['Temperatura']))
print("RMSE = ", rmse)

# Forecasting Future Dates
model2 = arima.ARIMA(df['Temperatura'], order=(3, 0, 3))
model2 = model2.fit()

index_future_dates = pd.date_range(start='2023-04-30', periods=31)
pred = model2.predict(start=len(df), end=len(df) + 30, typ='levels').rename('ARIMA Predictions')
pred.index = index_future_dates

# Plotting and Saving Predictions to Excel
pred.plot(figsize=(12, 5), legend=True)
pred.to_excel('predicciones_temp.xlsx')


