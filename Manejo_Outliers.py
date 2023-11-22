import pandas as pd
import numpy as np
df=pd.read_excel('variables_meterorologocas.xlsx',index_col=0)
df['Temperatura']=df['Temperatura'].replace(0,np.nan)
x=df["Temperatura"].dropna()
Q1=np.percentile(x, 25)
Q3= np.percentile(x, 75)
rangointer=Q3-Q1
umbralsuperior=Q3+1.5*rangointer
umbralinferior=Q3-1.5*rangointer
df=df[(df["Temperatura"]>= umbralinferior)&(df["Temperatura"]<=umbralsuperior)]
df.to_excel('Temperatura_Sin_Outliers.xlsx',index=False)