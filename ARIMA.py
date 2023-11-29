#IMPORTAR LIBRERIAS
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import mean_squared_error, r2_score
# Lectura de los datos

df = pd.read_excel("Data_Sin_Outliers.xlsx")
df.columns = df.columns.str.strip()
df.columns = df.columns.str.replace('[^a-zA-Z0-9]', '_', regex=True)
############################################################# agrupacio por dia de la temperatura
df.drop(['Velocidad_Viento', 'Direccion_Viento', 'Lluvia_Actual','Lluvia_Diaria','Presion_Atmosferica','Humedad'], axis=1, inplace=True)

# Supongamos que tienes un DataFrame llamado 'df' con las columnas 'Fecha_Hora' y 'Temperatura'

# Convierte 'Fecha_Hora' a formato datetime
df["Fecha_Hora"] = pd.to_datetime(df["Fecha_Hora"], format='%d/%m/%Y %H:%M')

# Extrae la fecha para agrupar por día
df['Fecha'] = df["Fecha_Hora"].dt.date

# Calcula el promedio de 'Temperatura' por día
df_promedio_dia_tem = df.groupby('Fecha')['Temperatura'].mean().reset_index()

# Imprime el nuevo DataFrame con el promedio de temperatura por día
print(df_promedio_dia_tem)
df.drop(['Fecha_Hora'], axis=1, inplace=True)
# # Guardar el DataFrame resultante en un nuevo archivo Excel
#df_promedio_dia.to_excel('preARIMA.xlsx', index=False) aqui escribimos el datframe en un archivo de excel
#####################################################
df_hum = pd.read_excel("Data_Sin_Outliers.xlsx")
df_hum.drop(['Velocidad_Viento', 'Direccion_Viento', 'Lluvia_Actual','Lluvia_Diaria','Presion_Atmosferica','Temperatura'], axis=1, inplace=True)

# Supongamos que tienes un DataFrame llamado 'df' con las columnas 'Fecha_Hora' y 'Temperatura'

# Convierte 'Fecha_Hora' a formato datetime
df_hum["Fecha_Hora"] = pd.to_datetime(df_hum["Fecha_Hora"], format='%d/%m/%Y %H:%M')

# Extrae la fecha para agrupar por día
df_hum['Fecha'] = df_hum["Fecha_Hora"].dt.date

# Calcula el promedio de 'Temperatura' por día
df_promedio_dia_Hum = df.groupby('Fecha')['Humedad'].mean().reset_index()

# Imprime el nuevo DataFrame con el promedio de temperatura por día
print(df_promedio_dia_Hum)

# # Guardar el DataFrame resultante en un nuevo archivo Excel
#df_promedio_dia.to_excel('preARIMA.xlsx', index=False) aqui escribimos el datframe en u







######################################ARIMA###################################
df = pd.read_excel("datos-ARIMA.xlsx", parse_dates=['Fecha'])
# Mostrar el resultado
print(df)
# Seleccionamos la Fecha como el índice del DataFrame y ordenamos por esta
df.set_index('Fecha', inplace=True)
df.sort_index(inplace=True)
# Establecemos la frecuencia de los datos de forma explícita
df = df.asfreq('D')
mod = ARIMA(df['Defectos'], order=(3,1,4))
res = mod.fit()
# Generamos las predicciones y su intervalo de confianza
pred = res.get_prediction(start=pd.to_datetime('1981-01-01'), end=pd.to_datetime('2023-12-01'), dynamic=False)
pred_ci = pred.conf_int()
# Creamos el gráfico
ax = df['Defectos']['1981':].plot(label='Datos observados')
pred.predicted_mean.plot(ax=ax, label='Datos simulados', alpha=.7, figsize=(18, 6))
ax.fill_between(pred_ci.index,
                pred_ci.iloc[:, 0],
                pred_ci.iloc[:, 1], color='k', alpha=.2)
ax.set_ylim([0, df['Defectos'].max() + 100]) 
ax.set_xlabel('Fecha')
ax.set_ylabel('Número de defectos')
plt.legend()
plt.show()

# Crea el DataFrame a partir de un diccionario que contiene pred.predicted_mean
df_pred = pd.DataFrame({'Defectos simulados': pred.predicted_mean})
df_pred.to_excel('datos_simulados.xlsx')
#COEFICIENTE DE CORRELACIÓN Y ERROR CUADRATICO
pred = res.get_prediction(start=pd.to_datetime('1981-01-01'), end=pd.to_datetime('2022-12-01'), dynamic=False)
pred_ci = pred.conf_int()
# Cálculo del MSE y R2
mse = mean_squared_error(df['Defectos'][pred.predicted_mean.index[0]:pred.predicted_mean.index[-1]], pred.predicted_mean)
r2 = r2_score(df['Defectos'][pred.predicted_mean.index[0]:pred.predicted_mean.index[-1]], pred.predicted_mean)
print(f"El error cuadrático medio (MSE) es: {mse}")
print(f"El coeficiente de determinación (R2) es: {r2}")
