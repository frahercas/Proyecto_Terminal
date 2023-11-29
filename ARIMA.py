import pandas as pd
df = pd.read_excel("Data_Sin_Outliers.xlsx")
df.columns = df.columns.str.strip()
df.columns = df.columns.str.replace('[^a-zA-Z0-9]', '_', regex=True)
##############################################################################
df.drop(['Velocidad_Viento', 'Direccion_Viento', 'Lluvia_Actual','Lluvia_Diaria','Presion_Atmosferica','Humedad'], axis=1, inplace=True)
df["Fecha_Hora"] = pd.to_datetime(df["Fecha_Hora"], format='%d/%m/%Y %H:%M')
df['Fecha'] = df["Fecha_Hora"].dt.date
df_promedio_dia_tem = df.groupby('Fecha')['Temperatura'].mean().reset_index()
print(df_promedio_dia_tem)
##############################################################################
df_hum = pd.read_excel("Data_Sin_Outliers.xlsx")
df_hum.drop(['Velocidad_Viento', 'Direccion_Viento', 'Lluvia_Actual','Lluvia_Diaria','Presion_Atmosferica','Temperatura'], axis=1, inplace=True)
df_hum["Fecha_Hora"] = pd.to_datetime(df_hum["Fecha_Hora"], format='%d/%m/%Y %H:%M')
df_hum['Fecha'] = df_hum["Fecha_Hora"].dt.date
df_promedio_dia_Hum = df_hum.groupby('Fecha')['Humedad'].mean().reset_index()
print(df_promedio_dia_Hum)
##############################################################################
df_pres = pd.read_excel("Data_Sin_Outliers.xlsx")
df_pres.drop(['Velocidad_Viento', 'Direccion_Viento', 'Lluvia_Actual','Lluvia_Diaria','Humedad','Temperatura'], axis=1, inplace=True)
df_pres["Fecha_Hora"] = pd.to_datetime(df_pres["Fecha_Hora"], format='%d/%m/%Y %H:%M')
df_pres['Fecha'] = df_pres["Fecha_Hora"].dt.date
df_promedio_dia_pres = df_pres.groupby('Fecha')['Presion_Atmosferica'].mean().reset_index()
print(df_promedio_dia_pres)
##############################################################################
df_llu = pd.read_excel("Data_Sin_Outliers.xlsx")
df_llu.drop(['Velocidad_Viento', 'Direccion_Viento', 'Lluvia_Actual','Presion_Atmosferica','Humedad','Temperatura'], axis=1, inplace=True)
df_llu["Fecha_Hora"] = pd.to_datetime(df_llu["Fecha_Hora"], format='%d/%m/%Y %H:%M')
df_llu['Fecha'] = df_llu["Fecha_Hora"].dt.date
df_promedio_dia_llu = df_llu.groupby('Fecha')['Lluvia_Diaria'].mean().reset_index()
print(df_promedio_dia_llu)
##############################################################################
union_ar=pd.merge(df_promedio_dia_tem, df_promedio_dia_Hum,on="Fecha", how="outer").merge(df_promedio_dia_pres, on="Fecha",how="outer").merge(df_promedio_dia_llu,on="Fecha",how="outer")
print(union_ar)
