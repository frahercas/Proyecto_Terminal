#HUMEDAD, TEMPERATURA,DIRECCION DEL VIENTO,VELOCIDAD DEL VIENTO
import pandas as pd
import os
import glob 
import numpy as np
from sqlalchemy import create_engine,text
import sqlalchemy
all_files=glob.glob(r"C:\Users\herca\OneDrive\Documentos\Python Scripts\datos direccion cdmx\Meteorologia\*.csv")
file_list=[]
for f in all_files:
    data=pd.read_csv(f)
    nombre=os.path.basename(f)
    data['source_file']=nombre  # en este for leemos todos los archivos que obtuvimos en este directorio
    file_list.append(data)
    
df=pd.concat(file_list, ignore_index=True) #Mostramos el Dataframe concatenado
df.drop(['unit', 'source_file'], axis=1, inplace=True)# #### quitando columnas que no sirven
df.dropna(inplace=True)#### quitando las filas que no sirven (contienen valores nulos)
df.drop(df[(df['id_station'] !='TLA') ].index, inplace=True) ##conservando solo los datos de las estaciones que nos interesan
numelist=list(range(41, 50))
my_dict = "41|42|43|44|45|46|47|48|49"
df=df [df ["date"]. str .contains (my_dict) == False ] ##Qitando los datos que no son fechas
df_rh=df[df["id_parameter"].str.contains("RH")] #Datframe de humedad
df_rh.rename(columns={'id_parameter':'Parametro_Humedad','value':'Humedad'}, inplace=True)
df_rh.drop(['id_station'], axis=1, inplace=True)# #### quitando columnas que no sirven
df_tmp=df[df["id_parameter"].str.contains("TMP")] #Datframe de temnperatura
df_tmp.rename(columns={'id_parameter':'Parametro_tmp','value':'Temperatura'}, inplace=True)
df_tmp.drop(['id_station'], axis=1, inplace=True)# #### quitando columnas que no sirven
df_wdr=df[df["id_parameter"].str.contains("WDR")] #Dataframe de direccion de viento
df_wdr.rename(columns={'id_parameter':'Parametro_Dir','value':'Direccion_Viento'}, inplace=True)
df_wsp=df[df["id_parameter"].str.contains("WSP")] #Dataframe de velocidad del viento
df_wsp.rename(columns={'id_parameter':'Parametro_Velocidad','value':'Velocidad_Viento'}, inplace=True)
df_wsp.drop(['id_station'], axis=1, inplace=True)# #### quitando columnas que no sirven
df_rh.drop(['Parametro_Humedad'], axis=1, inplace=True)# #### quitando columnas que no sirven
df_tmp.drop(['Parametro_tmp'], axis=1, inplace=True)# #### quitando columnas que no sirven
df_wdr.drop(['Parametro_Dir'], axis=1, inplace=True)# #### quitando columnas que no sirven
df_wsp.drop(['Parametro_Velocidad'], axis=1, inplace=True)# #### quitando columnas que no sirven
union=pd.merge(df_wdr, df_wsp,on="date", how="outer").merge(df_tmp, on="date",how="outer").merge(df_rh,on="date",how="outer")
union.drop(['id_station'], axis=1, inplace=True)
union.rename(columns={'date':'Fecha_Hora'}, inplace=True)
union.to_excel('Met_limpio_cdmx.xlsx', index=False) ##Escribir el dataframe resultante en un excel
##################################################################################################
#LLUVIA ACUMULADA
all_files = glob.glob(r"C:\Users\herca\OneDrive\Documentos\Python Scripts\datos observatorio\acumulada por año\*.csv")
file_list = []
for f in all_files:
    data = pd.read_csv(f)
    nombre = os.path.basename(f)
    data['source_file'] = nombre  # en este for leemos todos los archivos que obtuvimos en este directorio
    file_list.append(data)
    
df = pd.concat(file_list, ignore_index=True) #Mostramos el Dataframe concatenado
df.dropna(inplace=True)  # quitando las filas que no sirven (contienen valores nulos)
df.drop(['source_file'], axis=1, inplace=True)  # quitando columnas que no sirven
df['Fecha/hora'] = pd.to_datetime(df['Fecha/hora']).dt.strftime('%d/%m/%Y %H:%M')# Convertir el formato de la columna 'Fecha/hora'
df_filtered_acum = df[df['Fecha/hora'].str[-2:] == '00']# Filtrar los registros que tienen la hora exacta sin minutos
df_filtered_acum.to_excel('Lluvia_Acumulada_limpio_cdmx.xlsx', index=False)# Escribir el DataFrame resultante en un archivo de Excel
##################################################################################################
#LLUVIA INTENSIDAD
all_files = glob.glob(r"C:\Users\herca\OneDrive\Documentos\Python Scripts\datos observatorio\intensidad por año\*.csv")
file_list = []
for f in all_files:
    data = pd.read_csv(f)
    nombre = os.path.basename(f)
    data['source_file'] = nombre  # en este for leemos todos los archivos que obtuvimos en este directorio
    file_list.append(data)
    
df = pd.concat(file_list, ignore_index=True) #Mostramos el Dataframe concatenado
df.dropna(inplace=True)  # quitando las filas que no sirven (contienen valores nulos)
df.drop(['source_file'], axis=1, inplace=True)  # quitando columnas que no sirven
df.drop(['Estación'], axis=1, inplace=True)
df['Fecha/hora'] = pd.to_datetime(df['Fecha/hora']).dt.strftime('%d/%m/%Y %H:%M')# Convertir el formato de la columna 'Fecha/hora'
df_filtered_inten= df[df['Fecha/hora'].str[-2:] == '00']# Filtrar los registros que tienen la hora exacta sin minutos
df_filtered_inten.to_excel('Lluvia_intesidad_limpio_cdmx.xlsx', index=False)# Escribir el DataFrame resultante en un archivo de Excel
union_lluvia=pd.merge(df_filtered_acum,df_filtered_inten, on="Fecha/hora", how="outer")
union_lluvia.drop(['Estación'], axis=1, inplace=True)
union_lluvia.rename(columns={'Fecha/hora':'Fecha_Hora','Acumulada [mm]':'Lluvia_Diaria','Intensidad [mm/h]':'Lluvia_Actual'}, inplace=True)
union_lluvia.to_excel('lluvia_union.xlsx',index=False)
##################################################################################################
#PRESION
all_files=glob.glob(r"C:\Users\herca\OneDrive\Documentos\Python Scripts\datos direccion cdmx\MeteologiaPresion\*.csv")
file_list=[]
for f in all_files:
    data=pd.read_csv(f)
    nombre=os.path.basename(f)
    data['source_file']=nombre  # en este for leemos todos los archivos que obtuvimos en este directorio
    file_list.append(data)
    
df=pd.concat(file_list, ignore_index=True) #Mostramos el Dataframe concatenado
df.drop(['unit', 'source_file', 'parameter'], axis=1, inplace=True)# #### quitando columnas que no sirven
df.dropna(inplace=True)#### quitando las filas que no sirven (contienen valores nulos)
df.drop(df[(df['cve_station'] !='TLA') ].index, inplace=True) ##conservando solo los datos de las estaciones que nos interesan
my_dict = "41|42|43|44|45|46|47|48|49"
df=df [df ["Date"]. str .contains (my_dict) == False ] ##Qitando los datos que no son fechas
df.drop(['cve_station'], axis=1, inplace=True)
df.rename(columns={'Date':'Fecha_Hora','value':'Presion_Atmosferica'}, inplace=True)
df.to_excel('presion_limpio.xlsx', index=False) ##Escribir el dataframe resultante en un excel
#####################################################################################################
#DATOS TABLA "variables_meteorologicas"
variables_totales=pd.merge(union, union_lluvia,on="Fecha_Hora", how="outer").merge(df, on="Fecha_Hora",how="outer")
variables_totales["Id_Resgistro_Datos"] = range(1, len(variables_totales) + 1)
variables_totales["Id_Estacion"] = ""
variables_totales = variables_totales[["Id_Resgistro_Datos", "Id_Estacion", "Fecha_Hora", "Temperatura", "Velocidad_Viento", "Direccion_Viento","Lluvia_Actual","Lluvia_Diaria","Presion_Atmosferica","Humedad"]]
variables_totales=variables_totales.replace(np.nan,0)
variables_totales.to_excel('variables_meteorologicas.xlsx',index=False)
#####################################################################################################
#DATOS TABLA "cdmx_historico"
cdmx_historico=variables_totales
cdmx_historico["Id_CDMX"] = range(1, len(variables_totales) + 1)
cdmx_historico = variables_totales[["Id_CDMX","Id_Estacion", "Fecha_Hora", "Temperatura", "Velocidad_Viento", "Direccion_Viento","Presion_Atmosferica","Humedad"]]
cdmx_historico.to_excel('cdmx_historico.xlsx',index=False)
#####################################################################################################
#DATOS TABLA "cdmx_unam"
cdmx_unam=variables_totales
cdmx_unam["Id_UNAM"] = range(1, len(variables_totales) + 1)
cdmx_unam = variables_totales[["Id_UNAM","Id_Estacion", "Fecha_Hora", "Lluvia_Actual","Lluvia_Diaria"]]
cdmx_unam.to_excel('cdmx_unam.xlsx', index=False)
#####################################################################################################
#DATOS TABLA "upiita"
ruta_directorio = r'C:\Users\herca\OneDrive\Documentos\Python Scripts\Davis'
nombre_archivo = 'DatosFiltrados.txt'
ruta_archivo = f'{ruta_directorio}\\{nombre_archivo}'
names = ['Date', 'Time', 'Temp Out', 'Hi Temp', 'Low Temp', 'Out Hum', 'Dew Pt.', 'Wind Speed', 'Wind Dir', 'Wind Run',
         'Hi Speed', 'Hi Dir', 'Wind Chill', 'Heat Index', 'THW Index', 'Bar', 'Rain', 'Rain Rate', 'Heat D-D',
         'Cool D-D', 'In Temp', 'In Hum', 'In Dew', 'In Heat', 'In EMC', 'In Air Density', 'Wind Samp', 'Wind Tx',
         'ISS Recept', 'Arc. Int']
df_inicial = pd.read_csv(ruta_archivo, delimiter='\s+', error_bad_lines=False, header=None, names=names)
df_inicial["Id_UPIITA"] = range(1, len(df_inicial) + 1)
df_inicial["Id_Estacion"] = ""
df_upiita = df_inicial[["Id_UPIITA", "Id_Estacion", "Date", "Time", "Hi Temp", "In Hum", "Wind Speed", "Wind Dir", "Bar",
                        "Rain", "Rain Rate"]]
df_upiita.rename(columns={'Hi Temp': 'Temperatura', 'In Hum': 'Humedad', 'Wind Speed': 'Velocidad_Viento',
                          'Wind Dir': 'Direccion_Viento', 'Bar': 'Presion_Atmosferica', 'Rain': 'Lluvia_Acumulada',
                          'Rain Rate': 'Lluvia_Actual'}, inplace=True)
df_upiita['Date'] = pd.to_datetime(df_upiita['Date'], format='%d/%m/%y', errors='coerce').dt.strftime('%d/%m/%Y')
def convertir_a_24_horas(time_str):
    hora, minutos = map(int, time_str[:-1].split(':'))
    if time_str.endswith('p') and hora != 12:
        hora += 12
    elif time_str.endswith('a') and hora == 12:
        hora = 0
    return f'{hora:02d}:{minutos:02d}'

df_upiita['Time'] = df_upiita['Time'].apply(convertir_a_24_horas)
direccion_viento_mapping = {
    'N': 0,
    'NNE': 22.5,
    'NE': 45,
    'ENE': 67.5,
    'E': 90,
    'ESE': 112.5,
    'SE': 135,
    'SSE': 157.5,
    'S': 180,
    'SSW': 202.5,
    'SW': 225,
    'WSW': 247.5,
    'W': 270,
    'WNW': 292.5,
    'NW': 315,
    'NNW': 337.5,
    "---":-1
}
df_upiita['Direccion_Viento'] = df_upiita['Direccion_Viento'].map(direccion_viento_mapping)
df_upiita['Fecha_Hora'] = df_upiita['Date'] + ' ' + df_upiita['Time']
# Convertir 'Fecha_Hora' a formato de fecha y hora
df_upiita['Fecha_Hora'] = pd.to_datetime(df_upiita['Fecha_Hora'], format='%d/%m/%Y %H:%M', errors='coerce')

# Filtrar solo las horas cerradas sin minutos
df_upiita = df_upiita[df_upiita['Fecha_Hora'].dt.minute == 0]
df_upiita.drop(['Date', 'Time'], axis=1, inplace=True)
df_upiita['Temperatura'] = pd.to_numeric(df_upiita['Temperatura'], errors='coerce')
df_upiita = df_upiita[["Id_UPIITA", "Id_Estacion", "Fecha_Hora", "Temperatura", "Humedad", "Velocidad_Viento", "Direccion_Viento", "Presion_Atmosferica","Lluvia_Acumulada", "Lluvia_Actual"]]
df_upiita.to_excel('datos_filtrados_UPIITA.xlsx', index=False)
################################################################################################################
#DATOS TABLA escom
ruta_directorio = r'C:\Users\herca\OneDrive\Documentos\Python Scripts\Davis\davis ESCOM'
nombre_archivo = 'DatosFiltrados.txt'
ruta_archivo = f'{ruta_directorio}\\{nombre_archivo}'
names = ['Date', 'Time', 'Temp Out', 'Hi Temp', 'Low Temp', 'Out Hum', 'Dew Pt.', 'Wind Speed', 'Wind Dir', 'Wind Run',
         'Hi Speed', 'Hi Dir', 'Wind Chill', 'Heat Index', 'THW Index', 'Bar', 'Rain', 'Rain Rate', 'Heat D-D',
         'Cool D-D', 'In Temp', 'In Hum', 'In Dew', 'In Heat', 'In EMC', 'In Air Density', 'Wind Samp', 'Wind Tx',
         'ISS Recept', 'Arc. Int']
df_inicial = pd.read_csv(ruta_archivo, delimiter='\s+', error_bad_lines=False, header=None, names=names)
df_inicial["Id_ESCOM"] = range(1, len(df_inicial) + 1)
df_inicial["Id_Estacion"] = ""
df_escom = df_inicial[["Id_ESCOM", "Id_Estacion", "Date", "Time", "Hi Temp", "In Hum", "Wind Speed", "Wind Dir", "Bar",
                        "Rain", "Rain Rate"]]
df_escom.rename(columns={'Hi Temp': 'Temperatura', 'In Hum': 'Humedad', 'Wind Speed': 'Velocidad_Viento',
                          'Wind Dir': 'Direccion_Viento', 'Bar': 'Presion_Atmosferica', 'Rain': 'Lluvia_Acumulada',
                          'Rain Rate': 'Lluvia_Actual'}, inplace=True)
df_escom['Date'] = pd.to_datetime(df_escom['Date'], format='%d/%m/%y', errors='coerce').dt.strftime('%d/%m/%Y')
def convertir_a_24_horas(time_str):
    hora, minutos = map(int, time_str[:-1].split(':'))
    if time_str.endswith('p') and hora != 12:
        hora += 12
    elif time_str.endswith('a') and hora == 12:
        hora = 0
    return f'{hora:02d}:{minutos:02d}'

df_escom['Time'] = df_escom['Time'].apply(convertir_a_24_horas)
direccion_viento_mapping = {
    'N': 0,
    'NNE': 22.5,
    'NE': 45,
    'ENE': 67.5,
    'E': 90,
    'ESE': 112.5,
    'SE': 135,
    'SSE': 157.5,
    'S': 180,
    'SSW': 202.5,
    'SW': 225,
    'WSW': 247.5,
    'W': 270,
    'WNW': 292.5,
    'NW': 315,
    'NNW': 337.5,
    "---":-1
}
df_escom['Direccion_Viento'] = df_escom['Direccion_Viento'].map(direccion_viento_mapping)
df_escom['Fecha_Hora'] = df_escom['Date'] + ' ' + df_escom['Time']
# Convertir 'Fecha_Hora' a formato de fecha y hora
df_escom['Fecha_Hora'] = pd.to_datetime(df_escom['Fecha_Hora'], format='%d/%m/%Y %H:%M', errors='coerce')

# Filtrar solo las horas cerradas sin minutos
df_escom = df_escom[df_escom['Fecha_Hora'].dt.minute == 0]
df_escom.drop(['Date', 'Time'], axis=1, inplace=True)
df_escom['Temperatura'] = pd.to_numeric(df_escom['Temperatura'], errors='coerce')
df_escom = df_escom[["Id_ESCOM", "Id_Estacion", "Fecha_Hora", "Temperatura", "Humedad", "Velocidad_Viento", "Direccion_Viento", "Presion_Atmosferica","Lluvia_Acumulada", "Lluvia_Actual"]]
df_escom.to_excel('datos_filtrados_ESCOM.xlsx', index=False)
################################################################################################################
#ESTABLECIENDO CONEXION CON BASE DE DATOS
cadena_conexion='mysql+mysqldb://root:oktoberfest@localhost:3306/revision'
conexion=create_engine(cadena_conexion)
#################################################################################################################
nombres_tablas = ['zonas_estaciones', 'direccion_estaciones', 'estaciones_meteorologicas', 
                  'variables_meteorologicas', 'cdmx_historico', 'cdmx_unam', 'upiita', 'escom']

# Desactivar restricciones de clave externa
with conexion.connect() as connection:
    connection.execute(text('SET FOREIGN_KEY_CHECKS=0'))

    # Eliminar registros existentes en cada tabla
    for nombre_tabla in nombres_tablas:
        delete_statement = text(f'DELETE FROM revision.{nombre_tabla}')
        connection.execute(delete_statement)

    # Activar restricciones de clave externa nuevamente
    connection.execute(text('SET FOREIGN_KEY_CHECKS=1'))

# Leer el DataFrame desde el archivo Excel
cdmx_unam = pd.read_excel("datos_filtrados_UPIITA.xlsx")

# Escribir el DataFrame en cada tabla de la base de datos
for nombre_tabla in nombres_tablas:
    try:
        cdmx_unam.to_sql(name=nombre_tabla, con=conexion, schema="revision", index=False, if_exists='append')
    except sqlalchemy.exc.IntegrityError as e:
        # Manejar duplicados si es una clave primaria
        if 'Duplicate entry' in str(e):
            if 'PRIMARY' in str(e):
                update_statement = text(f'INSERT INTO revision.{nombre_tabla} VALUES :data ON DUPLICATE KEY UPDATE')
                connection.execute(update_statement, data=cdmx_unam.to_dict(orient='records'))
        else:
            raise e
        
#####################################################################################################
#ESCRIBIENDO LOS DATOS EN SUS RESPECTIVAS TABLAS
df = pd.read_excel("zona_estaciones.xlsx")
df.to_sql(name='zonas_estaciones', con=conexion, schema="revision", index=False, if_exists='append')
df1 = pd.read_excel("direccion_estaciones.xlsx")
df1.to_sql(name='direccion_estaciones', con=conexion, schema="revision", index=False, if_exists='append')
df1 = pd.read_excel("estaciones_meteorologicas.xlsx")
df1.to_sql(name='estaciones_meteorologicas', con=conexion, schema="revision", index=False, if_exists='append')
variables_totales = pd.read_excel("variables_meteorologicas.xlsx")
variables_totales.to_sql(name='variables_meteorologicas', con=conexion, schema="revision", index=False, if_exists='append')
cdmx_historico= pd.read_excel("cdmx_historico.xlsx")
cdmx_historico.to_sql(name='cdmx_historico', con=conexion, schema="revision", index=False, if_exists='append')
cdmx_unam= pd.read_excel("cdmx_unam.xlsx")
cdmx_unam.to_sql(name='cdmx_unam', con=conexion, schema="revision",index=False,if_exists='append')
cdmx_unam= pd.read_excel("datos_filtrados_UPIITA.xlsx")
cdmx_unam.to_sql(name='upiita', con=conexion, schema="revision",index=False,if_exists='append')
cdmx_unam= pd.read_excel("datos_filtrados_ESCOM.xlsx")
cdmx_unam.to_sql(name='escom', con=conexion, schema="revision",index=False,if_exists='append')
