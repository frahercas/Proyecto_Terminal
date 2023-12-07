import pandas as pd
import matplotlib.pyplot as plt
df=pd.read_excel('Datos_Preparatorios.xlsx',index_col='Fecha'   ,parse_dates=True)
#df=df.dropna()
print('Shape of data',df.shape)
print(df.head())
df['Temperatura'].plot(figsize=(12,5)) #primer plot solo los datos
from statsmodels.tsa.stattools import adfuller
def ad_test(dataset):
     dftest = adfuller(dataset, autolag = 'AIC')
     print("1. ADF : ",dftest[0])
     print("2. P-Value : ", dftest[1])
     print("3. Num Of Lags : ", dftest[2])
     print("4. Num Of Observations Used For ADF Regression:",      dftest[3])
     print("5. Critical Values :")
     for key, val in dftest[4].items():
         print("\t",key, ": ", val)
ad_test(df['Temperatura'])
from pmdarima import auto_arima
stepwise_fit = auto_arima(df['Temperatura'], trace=True,
suppress_warnings=True)
#print(df.shape)
train=df.iloc[:-30]
test=df.iloc[-30:]
#print(train.shape,test.shape)
# Cambiar esta línea
import statsmodels.tsa.arima.model as arima
arima_model=arima.ARIMA(train['Temperatura'],order=(3,0,3))
arima_model=arima_model.fit()
arima_model.summary()
start=len(train)
end=len(train)+len(test)-1
pred=arima_model.predict(start=start,end=end,typ='levels').rename('ARIMA Predictions')
#.plot(legend=True)
test['Temperatura'].plot(legend=True) #plot con los datos predichos
from sklearn.metrics import mean_squared_error
from math import sqrt
test['Temperatura'].mean()
rmse=sqrt(mean_squared_error(pred,test['Temperatura']))
#print("RMSE= ",rmse)
model2=arima.ARIMA(df['Temperatura'],order=(3,0,3))
model2=model2.fit()
#print(df.tail())
index_future_dates=pd.date_range(start='2023-04-30',periods=31)
#print(index_future_dates)
pred=model2.predict(start=len(df),end=len(df)+30,typ='levels').rename('ARIMA Predictions')
#print(comp_pred)
pred.index=index_future_dates
#print(pred)
pred.plot(figsize=(12,5),legend=True)
pred.to_excel('predicciones_temp.xlsx')
#####################################################33
# Entrenar el modelo con la columna Humedad
arima_model_hum=arima.ARIMA(train['Humedad'],order=(3,0,3))
arima_model_hum=arima_model_hum.fit()

# Predecir la humedad para el conjunto de prueba
pred_hum=arima_model_hum.predict(start=start,end=end,typ='levels').rename('ARIMA Predictions')
test['Humedad'].plot(legend=True) #plot con los datos predichos

# Calcular el error cuadrático medio
rmse_hum=sqrt(mean_squared_error(pred_hum,test['Humedad']))
#print("RMSE= ",rmse_hum)

# Predecir la humedad para el futuro
model2_hum=arima.ARIMA(df['Humedad'],order=(3,0,3))
model2_hum=model2_hum.fit()
pred_hum_fut=model2_hum.predict(start=len(df),end=len(df)+30,typ='levels').rename('ARIMA Predictions')
pred_hum_fut.index=index_future_dates
pred_hum_fut.plot(figsize=(12,5),legend=True)
pred_hum_fut.to_excel('predicciones_hum.xlsx')
#####################################################33
# Entrenar el modelo con la columna Presion_ATmosferica
arima_model_pres=arima.ARIMA(train['Presion_Atmosferica'],order=(3,0,3))
arima_model_pres=arima_model_pres.fit()

# Predecir la humedad para el conjunto de prueba
pred_pres=arima_model_pres.predict(start=start,end=end,typ='levels').rename('ARIMA Predictions')
test['Presion_Atmosferica'].plot(legend=True) #plot con los datos predichos

# Calcular el error cuadrático medio
rmse_pres=sqrt(mean_squared_error(pred_pres,test['Presion_Atmosferica']))
#print("RMSE= ",rmse_hum)

# Predecir la presion atmosferica para el futuro
model2_pres=arima.ARIMA(df['Presion_Atmosferica'],order=(3,0,3))
model2_pres=model2_pres.fit()
pred_pres_fut=model2_pres.predict(start=len(df),end=len(df)+30,typ='levels').rename('ARIMA Predictions')
pred_pres_fut.index=index_future_dates
pred_pres_fut.plot(figsize=(12,5),legend=True)
pred_pres_fut.to_excel('predicciones_presion.xlsx')
#####################################################33
# Entrenar el modelo con la columna Lluvia_Diaria
arima_model_llu=arima.ARIMA(train['Lluvia_Diaria'],order=(3,0,3))
arima_model_llu=arima_model_llu.fit()

# Predecir la lluvia para el conjunto de prueba
pred_llu=arima_model_llu.predict(start=start,end=end,typ='levels').rename('ARIMA Predictions')
test['Lluvia_Diaria'].plot(legend=True) #plot con los datos predichos

# Calcular el error cuadrático medio
rmse_llu=sqrt(mean_squared_error(pred_llu,test['Lluvia_Diaria']))
#print("RMSE= ",rmse_hum)

# Predecir la presion atmosferica para el futuro
model2_llu=arima.ARIMA(df['Lluvia_Diaria'],order=(3,0,3))
model2_llu=model2_llu.fit()
pred_llu_fut=model2_llu.predict(start=len(df),end=len(df)+30,typ='levels').rename('ARIMA Predictions')
pred_llu_fut.index=index_future_dates
pred_llu_fut.plot(figsize=(12,5),legend=True)
pred_llu_fut.to_excel('predicciones_Lluvia.xlsx')
