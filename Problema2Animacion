import random
import math
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px


# Parámetros iniciales
D = 100  
N = 1000 
I = 1  
R = 0  
S = N - I - R 
r_infeccion = 3  
razon_recuperacion = 0.1  
num_iteraciones = 50
desplazamiento_promedio = 1.0

# Verificar que N = I + S + R
assert N == I + S + R, "El total de personas no coincide con N."

# Listas para las variables
x_positions = []
y_positions = []
estados = ['Infectado'] * I + ['Susceptible'] * S + ['Recuperado'] * R  
ids = list(range(1, N + 1))  
iteraciones = [0] * N  

# Generar posiciones iniciales para cada persona
for _ in range(N):
    a = random.random() * 2 * math.pi  
    r = (D / 2) * math.sqrt(random.random())  
    x = r * math.cos(a) 
    y = r * math.sin(a)  
    x_positions.append(x)
    y_positions.append(y)

# DataFrame inicial
data = pd.DataFrame({
    'id': ids,
    'x': x_positions,
    'y': y_positions,
    'estado': estados,
    'iteracion': iteraciones
})

# Función para calcular la distancia euclidiana
def distancia_euclidiana(x1, y1, x2, y2):
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2) < r_infeccion  

# Lista para almacenar los datos de cada iteración
frames = []

# Simulación
for iteracion in range(1, num_iteraciones + 1): 
    # Generar desplazamientos aleatorios
    desplazamientos_x = np.random.normal(0, desplazamiento_promedio, N)
    desplazamientos_y = np.random.normal(0, desplazamiento_promedio, N)

    # Actualizar posiciones
    data['x'] += desplazamientos_x
    data['y'] += desplazamientos_y

    # Mantener dentro del área circular
    radios = np.sqrt(data['x']**2 + data['y']**2)
    fuera_circulo = radios > (D / 2)
    data.loc[fuera_circulo, 'x'] *= (D / 2) / radios[fuera_circulo]
    data.loc[fuera_circulo, 'y'] *= (D / 2) / radios[fuera_circulo]

    # Crear copia del DataFrame para actualizaciones
    data_nueva = data.copy()

    # Infectar susceptibles
    infectados_actuales = data[data['estado'] == 'Infectado']
    for i, persona in data.iterrows():
        if persona['estado'] == 'Susceptible':
            for _, infectado in infectados_actuales.iterrows():
                if distancia_euclidiana(persona['x'], persona['y'], infectado['x'], infectado['y']):
                    data_nueva.at[i, 'estado'] = 'Infectado'
                    break

    # Recuperar infectados
    for i, persona in data.iterrows():
        if persona['estado'] == 'Infectado' and random.random() < razon_recuperacion:
            data_nueva.at[i, 'estado'] = 'Recuperado'

    # Actualizar iteración
    data_nueva['iteracion'] = iteracion
    frames.append(data_nueva)

    # Reemplazar DataFrame
    data = data_nueva.copy()

# Concatenar todos los frames en un solo DataFrame
df_anim = pd.concat(frames)

# Crear animación con Plotly
fig = px.scatter(
    df_anim,
    x="x",
    y="y",
    color="estado",
    animation_frame="iteracion",
    animation_group="id",
    title="Simulación de propagación de infección",
    labels={"estado": "Estado"},
    color_discrete_map={"Susceptible": "green", "Infectado": "red", "Recuperado": "blue"},
    range_x=[-D / 2, D / 2],
    range_y=[-D / 2, D / 2]
)

# Agregar la frontera del círculo
fig.update_layout(
    shapes=[
        dict(
            type="circle",
            x0=-D / 2, y0=-D / 2, x1=D / 2, y1=D / 2,
            line=dict(color="black", width=2)
        )
    ]
)

fig.update_layout(
    width=700,
    height=700,
    xaxis_title="Posición X",
    yaxis_title="Posición Y",
    legend_title="Estado",
    showlegend=True
)

fig.show()

# Resumen final
final_count = data['estado'].value_counts()
print("\nResumen final de estados:")
print(f"Susceptibles: {final_count.get('Susceptible', 0)}")
print(f"Infectados: {final_count.get('Infectado', 0)}")
print(f"Recuperados: {final_count.get('Recuperado', 0)}")
