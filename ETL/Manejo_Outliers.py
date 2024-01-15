# -*- coding: utf-8 -*-
#Código para verificar los datos "outlayers":
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
df=pd.read_excel('variables_meteorologicas_ordenado.xlsx',index_col=0)
df.drop(["Id_Estacion"], axis=1,inplace=True)
######################################### TEMPERATURA
df['Temperatura'] = df['Temperatura'].replace(0, np.nan)
x=df["Temperatura"].dropna()
#cuartiles
Q1t=np.percentile(x,25)# separa el 25% inferior del 75% superior
Q3t=np.percentile(x,75) #sepra el 75% inferior del 25% superior
rangointert=Q3t-Q1t #Obtenemos el rango intercuartilico
print("valor del quartil 1= ", Q1t)
print("valor del quartil 3= ", Q3t)
print("valor del rango intecuartilico= ", rangointert)
"""
un criterio clasico de identificacion de outliers es la definicion de dos umbrales
un umbral superior y un umbral inferior.
Lo que esto esta diciendo que que todos los valores que se encientren por encima de nuestro "Umbral superior en un outlier"
y todos los valores que se encuentren por de bajo  de nuestro "umbral inferior" tambien es un outlier
"""
umbralsuperiortemp=Q3t+1.5*rangointert
umbralinferiortemp=Q1t-1.5*rangointert
print("valor del umbral superior de temperatura",umbralsuperiortemp, " grados centigrados") #todos los valores que se encuentren por encina de este valor es un outlier
print("Valor del umbral inferior de teperatura",umbralinferiortemp," grados centigrados") #todos los valores que se encuentren por debajo de este valor es un outlier
########################################### PRESION ATMOSFERICOS
df['Presion_Atmosferica'] = df['Presion_Atmosferica'].replace(0, np.nan)
y=df["Presion_Atmosferica"].dropna()
Q1p=np.percentile(y,25)
Q3p=np.percentile(y,75)
rangointerp=Q3p-Q1p
print("valor del quartil 1= ", Q1p)
print("valor del quartil 3= ", Q3p)
print("valor del rango intecuartilico= ", rangointerp)
umbralsuperiorpres=Q3p+1.5*rangointerp
umbralinferiorpres=Q1p-1.5*rangointerp
print("valor de umbral superior ", umbralsuperiorpres, " mmhg")
print("valor de umbral inferior ", umbralinferiorpres, " mmhg")
###########################################HUMEDAD
df['Humedad'] = df['Humedad'].replace(0, np.nan)
z=df["Humedad"].dropna()
Q1h=np.percentile(z,25)
Q3h=np.percentile(z,75)
rangointerHum=Q3h-Q1h
print("valor del quartil 1= ", Q1h)
print("valor del quartil 3= ", Q3h)
print("valor del rango intecuartilico= ", rangointerHum)
umbralsuperiorhum=Q3h+1.5*rangointerHum
umbralinferiorhum=Q1h-1.5*rangointerHum
print("valor de umbral superior ", umbralsuperiorhum, " %")
print("valor de umbral inferior ", umbralinferiorhum, " %")
###########################################

# Remove outliers from the "Temperatura" column
df = df[(df["Temperatura"] >= umbralinferiortemp) & (df["Temperatura"] <= umbralsuperiortemp)]
# Remove outliers from the "Prsion_Atmosferica" column
df = df[(df["Presion_Atmosferica"] >= umbralinferiorpres) & (df["Presion_Atmosferica"] <= umbralsuperiorpres)]
# Remove outliers from the "Humedad" column
df = df[(df["Humedad"] >= umbralinferiorhum) & (df["Humedad"] <= umbralsuperiorhum)]

# Save the DataFrame to an Excel file
df.to_excel('Data_Sin_Outliers.xlsx', index=False)
