import math
import random
import pandas as pd
import numpy as np
import plotly.express as px

# Parámetros iniciales
D = 75  # Dimensión del área cuadrada
N = 1000  # Número de personas
radio_infeccion = 2  # Distancia para infección
razon_recuperacion = 0.4  # Probabilidad de recuperación
num_iteraciones = 30  # Número de iteraciones

# Inicialización de variables I, S, R
I = 1  # Infectados iniciales
R = 0  # Recuperados iniciales
S = N - I - R  # Susceptibles iniciales

# Asignar estados iniciales
estado = ["Infectado"] * I + ["Susceptible"] * S + ["Recuperado"] * R
random.shuffle(estado)

# Generar posiciones iniciales de las personas
cluster_x = random.uniform(-D / 2, D / 2)
cluster_y = random.uniform(-D / 2, D / 2)

posicion_x = []
posicion_y = []
while len(posicion_x) < N:
    x = np.random.normal(loc=cluster_x, scale=D / 4)
    y = np.random.normal(loc=cluster_y, scale=D / 4)
    if (-D / 2 <= x <= D / 2) and (-D / 2 <= y <= D / 2):
        posicion_x.append(x)
        posicion_y.append(y)

# Crear DataFrame inicial
df = pd.DataFrame({
    'posición x': posicion_x,
    'posición y': posicion_y,
    'estado': estado,
    'id único': list(range(N)),
    'iteracion': [0] * N
})

# Función para calcular distancia entre dos puntos
def distancia(p1, p2):
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2) < radio_infeccion

# Simulación de iteraciones
frames = []
for iteracion in range(num_iteraciones):
    # Vectores de desplazamiento
    desplazamiento_x = np.random.normal(0, 1, N)
    desplazamiento_y = np.random.normal(0, 1, N)

    # Actualizar posiciones
    df['posición x'] = df['posición x'] + desplazamiento_x
    df['posición y'] = df['posición y'] + desplazamiento_y

    # Mantener dentro del área
    df['posición x'] = np.clip(df['posición x'], -D / 2, D / 2)
    df['posición y'] = np.clip(df['posición y'], -D / 2, D / 2)


    # Crear copia del DataFrame para actualizaciones
    df_nueva = df.copy()

    # Infectar susceptibles
    infectados_actuales = df[df['estado'] == 'Infectado']
    for i, persona in df.iterrows():
        if persona['estado'] == 'Susceptible':
            for _, infectado in infectados_actuales.iterrows():
                if distancia((persona['posición x'], persona['posición y']),
                             (infectado['posición x'], infectado['posición y'])):
                    df_nueva.at[i, 'estado'] = 'Infectado'
                    break

    # Recuperar infectados
    for i, persona in df.iterrows():
        if persona['estado'] == 'Infectado' and random.random() < razon_recuperacion:
            df_nueva.at[i, 'estado'] = 'Recuperado'

    # Actualizar iteración
    df_nueva['iteracion'] = iteracion
    frames.append(df_nueva)

    # Reemplazar DataFrame
    df = df_nueva.copy()

# Concatenar todos los frames en un solo DataFrame
df_anim = pd.concat(frames)

# Crear animación con Plotly
fig = px.scatter(
    df_anim,
    x="posición x",
    y="posición y",
    color="estado",
    animation_frame="iteracion",
    animation_group="id único",
    title="Simulación de propagación de infección",
    labels={"estado": "Estado"},
    color_discrete_map={"Susceptible": "black", "Infectado": "red", "Recuperado": "blue"},
    range_x=[-D / 2-5, D / 2+5],
    range_y=[-D / 2-5, D / 2+5]
)

# Agregar la frontera del cuadrado
fig.update_layout(
    shapes=[
        dict(
            type="rect",
            x0=-D / 2 ,  # Agregar un margen de 5 unidades
            y0=-D / 2 ,
            x1=D / 2 ,
            y1=D / 2 ,
            line=dict(color="blue", width=2)
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

final_count = df['estado'].value_counts()
print("\nResumen final de estados:")
print(f"Susceptibles: {final_count.get('Susceptible', 0)}")
print(f"Infectados: {final_count.get('Infectado', 0)}")
print(f"Recuperados: {final_count.get('Recuperado', 0)}")
