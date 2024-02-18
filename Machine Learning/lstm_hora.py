import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from tensorflow.keras.callbacks import EarlyStopping
from sklearn.metrics import mean_squared_error, mean_absolute_error

# Leer el dataframe
df = pd.read_excel('Data_Sin_Outliers.xlsx', parse_dates=True, index_col='Fecha_Hora')
print(df.head())

# Seleccionar solo las columnas relevantes para el pronóstico
selected_columns = ['Temperatura', 'Lluvia_Actual', 'Presion_Atmosferica', 'Humedad']
df = df[selected_columns]

# Función para preparar los datos para el modelo LSTM
def prepare_data(data, n_steps):
    X, y = [], []
    for i in range(len(data)):
        end_ix = i + n_steps
        if end_ix > len(data)-1:
            break
        seq_x, seq_y = data[i:end_ix, :], data[end_ix, :]
        X.append(seq_x)
        y.append(seq_y)
    return np.array(X), np.array(y)

# Parámetros
n_steps = 24  # Número de pasos de tiempo para hacer la predicción (en este caso, 24 horas)
n_features = len(df.columns)  # Número de características (las columnas seleccionadas)

# Escalar los datos
scaler = MinMaxScaler(feature_range=(0, 1))
scaled_data = scaler.fit_transform(df)

# Preparar los datos en el formato adecuado para el modelo LSTM
X, y = prepare_data(scaled_data, n_steps)

# Dividir los datos en conjuntos de entrenamiento y prueba
split = int(0.8 * len(X))
X_train, X_test = X[:split], X[split:]
y_train, y_test = y[:split], y[split:]

# Construir el modelo LSTM
model = Sequential()
model.add(LSTM(50, activation='tanh', input_shape=(n_steps, n_features)))
model.add(Dense(n_features))
model.compile(optimizer='adam', loss='mse')

# Entrenar el modelo
es = EarlyStopping(monitor='val_loss', mode='min', verbose=1, patience=5)
history = model.fit(X_train, y_train, epochs=100, batch_size=32, validation_data=(X_test, y_test), callbacks=[es], verbose=1)

# Evaluar el modelo
y_pred = model.predict(X_test)
y_pred_inv = scaler.inverse_transform(y_pred)
y_test_inv = scaler.inverse_transform(y_test)
mse = mean_squared_error(y_test_inv, y_pred_inv)
mae = mean_absolute_error(y_test_inv, y_pred_inv)
print("Error cuadrático medio (MSE):", mse)
print("Error absoluto medio (MAE):", mae)


# Hacer predicciones solo para las siguientes 24 horas
last_data = scaled_data[-n_steps:].reshape((1, n_steps, n_features))
predictions = []
for _ in range(24):
    prediction = model.predict(last_data)
    predictions.append(prediction)
    last_data = np.concatenate([last_data[:, 1:, :], prediction.reshape(1, 1, n_features)], axis=1)

# Invertir la escala de las predicciones
predictions = np.array(predictions).squeeze()  # Reducir la dimensión del array
predictions = scaler.inverse_transform(predictions)

# Crear un rango de fechas para las predicciones
start_date = df.index[-1] + pd.Timedelta(hours=1)
predicted_index = pd.date_range(start=start_date, periods=24, freq='H')

# Crear un DataFrame para las predicciones
predicted_df = pd.DataFrame(predictions, columns=selected_columns, index=predicted_index)

# Renombrar la primera columna como "Fecha_Hora"
predicted_df = predicted_df.rename_axis("Fecha_Hora", axis='index')


# Imprimir el dataframe con las predicciones
print(predicted_df)
predicted_df.to_excel("Predicciones_24_horas.xlsx")
