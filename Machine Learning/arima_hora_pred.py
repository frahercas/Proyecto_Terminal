import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.stattools import adfuller
from pmdarima import auto_arima
import statsmodels.tsa.arima.model as arima
from sklearn.metrics import mean_squared_error
from math import sqrt

df = pd.read_excel('Datos_Preparatorios.xlsx', index_col='Fecha', parse_dates=True)
print('Shape of data', df.shape)
print(df.head())

# Plot the original data for Temperatura
df['Temperatura'].plot(figsize=(12, 5))

# ADF Test
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

# Auto ARIMA
stepwise_fit = auto_arima(df['Temperatura'], trace=True, suppress_warnings=True)

# Train-Test Split
train = df.iloc[:-30]
test = df.iloc[-30:]

# ARIMA Model Training
arima_model_temp = arima.ARIMA(train['Temperatura'], order=(4, 0, 4))
arima_model_temp = arima_model_temp.fit()
arima_model_temp.summary()

# Prediction
start = len(train)
end = len(train) + len(test) - 1
pred_temp = arima_model_temp.predict(start=start, end=end, typ='levels').rename('ARIMA Predictions')

# Plotting
test['Temperatura'].plot(legend=True)
pred_temp.plot(legend=True)
plt.show()

# Model Evaluation
rmse_temp = sqrt(mean_squared_error(pred_temp, test['Temperatura']))
print("RMSE for Temperatura= ", rmse_temp)

# ARIMA Model for Future Predictions
model2_temp = arima.ARIMA(df['Temperatura'], order=(4, 0, 4))
model2_temp = model2_temp.fit()

# Future Date Range
index_future_dates = pd.date_range(start='2024-01-01', periods=24, freq='H')  # Adjust the frequency to hourly

# Future Predictions
future_pred_temp = model2_temp.predict(start=len(df), end=len(df) + 23, typ='levels').rename('ARIMA Predictions')

# Plot Future Predictions
future_pred_temp.plot(figsize=(12, 5), legend=True)
plt.show()

# Save Future Predictions to Excel
future_pred_temp.to_excel('predicciones_temp_horas.xlsx', index=True)
#####################################################33
# Humedad
# Train ARIMA Model
arima_model_hum = arima.ARIMA(train['Humedad'], order=(4, 0, 4))
arima_model_hum = arima_model_hum.fit()

# Predict Humedad for the test set
pred_hum = arima_model_hum.predict(start=start, end=end, typ='levels').rename('ARIMA Predictions')
test['Humedad'].plot(legend=True)

# Calculate RMSE
rmse_hum = sqrt(mean_squared_error(pred_hum, test['Humedad']))
#print("RMSE= ", rmse_hum)

# Predict Humedad for the future
model2_hum = arima.ARIMA(df['Humedad'], order=(4, 0, 4))
model2_hum = model2_hum.fit()
pred_hum_fut = model2_hum.predict(start=len(df), end=len(df) + 23, typ='levels').rename('ARIMA Predictions')
pred_hum_fut.index = index_future_dates
pred_hum_fut.plot(figsize=(12, 5), legend=True)
pred_hum_fut.to_excel('predicciones_humedad_horas.xlsx')
#####################################################33
# Presion_Atmosferica
# Train ARIMA Model
arima_model_pres = arima.ARIMA(train['Presion_Atmosferica'], order=(4, 0, 4))
arima_model_pres = arima_model_pres.fit()

# Predict Presion_Atmosferica for the test set
pred_pres = arima_model_pres.predict(start=start, end=end, typ='levels').rename('ARIMA Predictions')
test['Presion_Atmosferica'].plot(legend=True)

# Calculate RMSE
rmse_pres = sqrt(mean_squared_error(pred_pres, test['Presion_Atmosferica']))
#print("RMSE= ", rmse_hum)

# Predict Presion_Atmosferica for the future
model2_pres = arima.ARIMA(df['Presion_Atmosferica'], order=(4, 0, 4))
model2_pres = model2_pres.fit()
pred_pres_fut = model2_pres.predict(start=len(df), end=len(df) + 23, typ='levels').rename('ARIMA Predictions')
pred_pres_fut.index = index_future_dates
pred_pres_fut.plot(figsize=(12, 5), legend=True)
pred_pres_fut.to_excel('predicciones_presion_horas.xlsx')
#####################################################33
# Lluvia_Diaria
# Train ARIMA Model
arima_model_llu = arima.ARIMA(train['Lluvia_Diaria'], order=(4, 0, 4))
arima_model_llu = arima_model_llu.fit()

# Predict Lluvia_Diaria for the test set
pred_llu = arima_model_llu.predict(start=start, end=end, typ='levels').rename('ARIMA Predictions')
test['Lluvia_Diaria'].plot(legend=True)

# Calculate RMSE
rmse_llu = sqrt(mean_squared_error(pred_llu, test['Lluvia_Diaria']))
#print("RMSE= ", rmse_hum)

# Predict Lluvia_Diaria for the future
model2_llu = arima.ARIMA(df['Lluvia_Diaria'], order=(4, 0, 4))
model2_llu = model2_llu.fit()
pred_llu_fut = model2_llu.predict(start=len(df), end=len(df) + 23, typ='levels').rename('ARIMA Predictions')
pred_llu_fut.index = index_future_dates
pred_llu_fut.plot(figsize=(12, 5), legend=True)
pred_llu_fut.to_excel('predicciones_Lluvia_horas.xlsx')

