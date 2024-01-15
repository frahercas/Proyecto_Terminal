import pandas as pd




# Humidity
df_horas = pd.read_excel("Data_Sin_Outliers.xlsx")
df_horas.drop(['Velocidad_Viento', 'Direccion_Viento', 'Lluvia_Actual'], axis=1, inplace=True)
df_horas["Fecha_Hora"] = pd.to_datetime(df_horas["Fecha_Hora"], format='%d/%m/%Y %H:%M')

# Save to Excel
df_horas.to_excel('Datos_Preparatorios_Hora.xlsx', index=False)


