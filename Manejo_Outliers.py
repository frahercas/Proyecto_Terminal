import pandas as pd
import numpy as np
df=pd.read_excel('variables_meteorologicas.xlsx',index_col=0)
df['Temperatura']=df['Temperatura'].replace(0,np.nan)
x=df["Temperatura"].dropna()
Q1=np.percentile(x, 25) #Separa el 25% inferior del 75% superior
Q3= np.percentile(x, 75)# Sepra el 75% inferior del 25% superior
rangointer=Q3-Q1 #Obtenemos el rango intercuartilico
umbralsuperior=Q3+1.5*rangointer #todos los valores por encima de este umbral se considera una valor atipico
umbralinferior=Q1-1.5*rangointer #todos los valores por debajo de este umbral se considera un valor atipico
print("primer cuartil",Q1)
print("tercer cuartil",Q3)
print("rango intercuartilico", rangointer)
print("umbrak superior", umbralsuperior)
print("umbral inferior", umbralinferior)
df=df[(df["Temperatura"]>= umbralinferior)&(df["Temperatura"]<=umbralsuperior)] # aqui removemos los datos considerdos outliers de la columan de temperatura
df.to_excel('Temperatura_Sin_Outliers.xlsx',index=False)
