import pandas as pd

                                                          #PROBLEMA 2

# Cargar archivos de pasajeros y vuelos
pasajeros_2016 = pd.read_csv(r"C:\Users\wilya\Downloads\Pasajeros\pasajeros2016.csv")
pasajeros_2017 = pd.read_csv(r"C:\Users\wilya\Downloads\Pasajeros\pasajeros2017.csv")
vuelos_2016 = pd.read_csv(r"C:\Users\wilya\Downloads\Vuelos\vuelos2016.csv")
vuelos_2017 = pd.read_csv(r"C:\Users\wilya\Downloads\Vuelos\vuelos2017.csv")

# Revisar columnas de cada archivo
print(pasajeros_2016.columns)
print(pasajeros_2017.columns)
print(vuelos_2016.columns)
print(vuelos_2017.columns)

# Unir los archivos de pasajeros de 2016 y 2017
pasajeros = pd.concat([pasajeros_2016, pasajeros_2017], ignore_index=True)

# Unir los archivos de vuelos de 2016 y 2017
vuelos = pd.concat([vuelos_2016, vuelos_2017], ignore_index=True)

#Se elimnaran datos duplicados
pasajeros = pasajeros.drop_duplicates()
vuelos = vuelos.drop_duplicates()


                                                          #PROBLEMA 3

# Unimos ambos DataFrames utilizando el campo común 'ID_Pasajero' y 'Cve_Cliente'
pasajeros_vuelos = pd.merge(pasajeros, vuelos, left_on='ID_Pasajero', right_on='Cve_Cliente', how='inner')

# Ver todas filas del DataFrame consolidado
pd.set_option('display.max_rows', None)
print(pasajeros_vuelos)


                                                           #PROBLEMA 4
# Cargar los datos de Líneas Aéreas
lineas_aereas = pd.read_csv(r"C:\Users\wilya\Downloads\DEACERO\LineasAereas.csv")

# Unir los datos consolidados con las Líneas Aéreas utilizando un left y right
pasajeros_vuelos_lineas = pd.merge(pasajeros_vuelos, lineas_aereas, left_on='Cve_LA', right_on='Code', how='left')

# Asignar "Otra" a las líneas aéreas que no se encontraron
pasajeros_vuelos_lineas['Linea_Aerea'].fillna('Otra', inplace=True)

# Seleccionar las columnas que se pidieron
result = pasajeros_vuelos_lineas[['Viaje', 'Clase', 'Precio', 'Ruta', 'Edad', 'Linea_Aerea']]


                                                           #PROBLEMA 5
                                                           
# Convertir 'Fecha del viaje' a tipo datetime
result['Viaje'] = pd.to_datetime(result['Viaje'], errors='coerce')

# Crear una columna para el Año
result['Año'] = result['Viaje'].dt.year

# Crear una columna para el semestre
result['Semestre'] = result['Viaje'].dt.month.apply(lambda x: 1 if x <= 6 else 2)

# Agrupar por Año, Semestre, Clase, Ruta y Línea Aérea, y calcular el promedio del precio
promedio_semestral = result.groupby(['Año', 'Semestre', 'Clase', 'Ruta', 'Linea_Aerea'])['Precio'].mean().reset_index()

# Renombrar la columna del precio a 'Promedio Precio'
promedio_semestral.rename(columns={'Precio': 'Promedio Precio'}, inplace=True)


# Se visualiza ya la tabla terminada
pd.set_option('display.max_rows', None)
print(promedio_semestral)
                                             
                                                           
#Se crea archivos CSV ya combinados
pasajeros.to_csv('Pasajeros_combinado.csv', index=False)
vuelos.to_csv('Vuelos_combinado.csv', index=False)
result.to_csv('Resultado_Final.csv', index=False)
promedio_semestral.to_csv('Promedio_Semestral.csv', index=False)