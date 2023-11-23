import pandas as pd
import numpy as np
#######################################################################################
#MAnejo de Outliers de Temperatura
df=pd.read_excel('variables_meteorologicas.xlsx',index_col=0)
df['Temperatura']=df['Temperatura'].replace(0,np.nan)
x=df["Temperatura"].dropna()
Q1=np.percentile(x, 25) #Separa el 25% inferior del 75% superior
Q3= np.percentile(x, 75)# Sepra el 75% inferior del 25% superior
rangointer=Q3-Q1 #Obtenemos el rango intercuartilico
umbralsuperior=Q3+1.5*rangointer #todos los valores por encima de este umbral se considera una valor atipico
umbralinferior=Q1-1.5*rangointer #todos los valores por debajo de este umbral se considera un valor atipico
df=df[(df["Temperatura"]>= umbralinferior)&(df["Temperatura"]<=umbralsuperior)] # aqui removemos los datos considerdos outliers de la columan de temperatura
#df.to_excel('Temperatura_Sin_Outliers.xlsx',index=False)
####################################################################################
# Manejo de Outliers de Presion Atmosferica
df['Presion_Atmosferica']=df['Presion_Atmosferica'].replace(0,np.nan)
y=df["Presion_Atmosferica"].dropna()
Q1pa=np.percentile(y, 25) 
Q3pa= np.percentile(y, 75)
rangointer=Q3pa-Q1pa 
umbralsuperior=Q3pa+1.5*rangointer 
umbralinferior=Q1pa-1.5*rangointer 
# print("primer cuartil",Q1pa)
# print("tercer cuartil",Q3pa)
# print("rango intercuartilico", rangointer)
# print("umbrak superior", umbralsuperior)
# print("umbral inferior", umbralinferior)
df=df[(df["Presion_Atmosferica"]>= umbralinferior)&(df["Presion_Atmosferica"]<=umbralsuperior)] 
#df.to_excel('Humedad_Sin_Outliers.xlsx',index=False)
####################################################################################
# Manejo de Outliers de Lluvia    
df['Lluvia_Diaria']=df['Lluvia_Diaria'].replace(0,np.nan)
z=df["Lluvia_Diaria"].dropna()
Q1llu=np.percentile(z, 25) 
Q3llu= np.percentile(z, 75)
rangointer=Q3llu-Q1llu 
umbralsuperior=Q3llu+1.5*rangointer 
umbralinferior=Q1llu-1.5*rangointer 
print("primer cuartil",Q1llu)
print("tercer cuartil",Q3llu)
print("rango intercuartilico", rangointer)
print("umbrak superior", umbralsuperior)
print("umbral inferior", umbralinferior)
df=df[(df["Lluvia_Diaria"]>= umbralinferior)&(df["Lluvia_Diaria"]<=umbralsuperior)] 
