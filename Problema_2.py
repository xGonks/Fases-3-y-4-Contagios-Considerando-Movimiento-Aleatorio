"""
Problema 3: Simulación de una ciudad circular con distribución de personas uniforme.
"""

import math
import random
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import webbrowser


def polares_rectangulares(a, r):
    """
    Convierte cordenadas polares (angulo, radio) a rectangulares.
    """
    x = r * math.cos(a)
    y = r * math.sin(a)
    return x, y


def distancia(x1, y1, x2, y2, r):
    """
    Dados dos puntos P1 y P2 (en coordenadas rectangulares),
    devuelve True si la distancia entre ellos es menor que r.
    """
    if (math.sqrt(((x1 - x2)**2)+((y1 - y2)**2)) < r):
        return True
    else:
        return False


# Valores Iniciales
D = 100
N = 1000
R = 0
I = 1
S = N - I - R
radio_infeccion = 3
razon_recuperacion = 0.1
iteraciones = 60

# Recolección de Datos para el DataFrame
posicion_x = []
posicion_y = []
# Crear Coordenadas Cerca del Cluster (con la Dist. Normal)
while (len(posicion_x) < N):
    a = random.uniform(0, 2*np.pi)
    r = random.uniform(0, D/2)
    x, y = polares_rectangulares(a, r)
    # Solo Agregar la Coordenada si está Dentro del Circulo
    if ((x**2) + (y**2) < (D/2)**2):
        posicion_x.append(x)
        posicion_y.append(y)
estado = []
for i in range(int(S)):
    estado.append("Susceptible")
for j in range(int(I)):
    estado.append("Infectado")
for k in range(int(R)):
    estado.append("Recuperado")
id = []
iteracion = []
for m in range(int(N)):
    id.append(m)
    iteracion.append(0)

# Crear el DataFrame
d = {'posición x': posicion_x, 'posición y': posicion_y,
     'estado': estado, 'id único': id, 'iteracion': iteracion}
df = pd.DataFrame(data=d)
df = pd.concat([df, pd.DataFrame({'posición x': [D + 10],'posición y': [D + 10],'estado': ["Recuperado"],'id único': [-1],'iteracion': [0]})], ignore_index=True)

# Parametrizar el Circulo para Graficarlo
theta = np.linspace(0, 2 * np.pi, 100)
circle_x = (D / 2) * np.cos(theta)
circle_y = (D / 2) * np.sin(theta)

# Crear la Gráfica
plt.figure(figsize=(8, 8))
plt.plot(circle_x, circle_y, color="blue", label="(x^2) + (y^2) = (D/2)^2")

# Asignar Colores Según el Estado
colores = {'Susceptible': 'black', 'Infectado': 'red', 'Recuperado': 'blue'}
for estado, color in colores.items():
    plt.scatter(df[df['estado'] == estado]['posición x'],
                df[df['estado'] == estado]['posición y'],
                color=color, s=10, label=f"{estado}", zorder=3)
plt.axhline(0, color='gray', linewidth=0.5)
plt.axvline(0, color='gray', linewidth=0.5)

# Configuración de la Gráfica
plt.gca().set_aspect('equal', adjustable='box')
plt.xlim(-D / 2 - 5, D / 2 + 5)
plt.ylim(-D / 2 - 5, D / 2 + 5)
plt.xlabel("x")
plt.ylabel("y")
plt.legend(loc="upper right", bbox_to_anchor=(1.1, 1.1))
plt.grid(True)

# Visualización
plt.show()
print(df)

def rutina(df, D, radio_infeccion, razon_recuperacion):
    # Recolección de Datos para el DataFrame
    df_return = df.copy()
    
    # Actualizar Coordenadas de cada Persona
    posicion_x_new = []
    posicion_y_new = []
    for row in df_return.itertuples():
        while (True):
            x = row[1]
            y = row[2]
            sum_x, sum_y = polares_rectangulares(random.uniform(0, 2*np.pi), random.uniform(0, 1))
            new_x = x + sum_x
            new_y = y + sum_y
            if ((new_x**2) + (new_y**2) < (D/2)**2):
                posicion_x_new.append(new_x)
                posicion_y_new.append(new_y)
                break
    df_return['posición x'] = posicion_x_new
    df_return['posición y'] = posicion_y_new
    
    # Guardar los Infectados Originales antes de Propagar la Infección
    infectados_previos = df_return[df_return['estado'] == "Infectado"].index

    # Propagar la Infección a Susceptibles
    for i, row_i in df_return.iterrows():
        if row_i['estado'] == "Susceptible":
            for j, row_j in df_return.loc[infectados_previos].iterrows():
                if distancia(row_i['posición x'], row_i['posición y'], row_j['posición x'], row_j['posición y'], radio_infeccion):
                    df_return.at[i, 'estado'] = "Infectado"
                    break

    # Recuperar Infectados Previos según la Tasa de Recuperación
    for i in infectados_previos:
        probabilidad = random.random()
        if probabilidad < razon_recuperacion:
            df_return.at[i, 'estado'] = "Recuperado"
            
    return df_return

# Crear una Lista de Frames para la Animación
frames = []
frames.append(df)
df = df.drop(df.index[-1])
plt.show()
print(df)
for iteracion in range(iteraciones):
    # Aplicar la Rutina
    df = rutina(df, D, radio_infeccion, razon_recuperacion)
    # Agregar la Iteración al DataFrame
    df['iteracion'] = iteracion
    frames.append(df)
    print(iteracion)

# Concatenar los Frames en un solo DataFrame
df_anim = pd.concat(frames)

# Crear Animación con Plotly
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
    range_x=[-D / 2 - 5, D / 2 + 5],
    range_y=[-D / 2 - 5, D / 2 + 5]
)

# Agregar la Frontera del Círculo
fig.update_layout(
    shapes=[dict(
        type="circle",
        x0=-D / 2,  # Agregar un margen de 5 unidades
        y0=-D / 2,
        x1=D / 2,
        y1=D / 2,
        line=dict(color="blue", width=2)
    )]
)
fig.update_layout(
    width=1000,
    height=1000,
    xaxis_title="Posición X",
    yaxis_title="Posición Y",
    legend_title="Estado",
    showlegend=True
)

# Mostrar la Animación
fig.show()

# Resumen Final
final_count = df['estado'].value_counts()
print("\nResumen final de estados:")
print(f"Susceptibles: {final_count.get('Susceptible', 0)}")
print(f"Infectados: {final_count.get('Infectado', 0)}")
print(f"Recuperados: {final_count.get('Recuperado', 0)}")

# Guardar la Animación en un archivo HTML
html_file = "animacion_infeccion.html"
fig.write_html(html_file)

# Visualización
webbrowser.open_new_tab(html_file)

# uso de la función de distancia
#x1, y1 = data.loc[0, ['x', 'y']]
#x2, y2 = data.loc[1, ['x', 'y']]
#print(f"¿Dentro del radio de infección?: {distancia_euclidiana(x1, y1, x2, y2)}")
