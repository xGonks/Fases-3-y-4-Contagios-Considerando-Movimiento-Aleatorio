"""
Problema 4: Simulación de una ciudad circular con distribución de personas en cluster.
"""

import math
import random
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


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
radio_infeccion = 0.6
razon_recuperacion = 0.6

# Punto Cluster (aleatorio)
cluster_a = random.uniform(0, 2*np.pi)
cluster_r = random.uniform(0, D/2)
cluster_x, cluster_y = polares_rectangulares(cluster_a, cluster_r)

# Recolección de Datos para el DataFrame
posicion_x = []
posicion_y = []
# Crear Coordenadas Cerca del Cluster (con la Dist. Normal)
while (len(posicion_x) < N):
    x = np.random.normal(loc=cluster_x, scale=D/8)
    y = np.random.normal(loc=cluster_y, scale=D/8)
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
plt.scatter(cluster_x, cluster_y, color="green",
            s=50, label="Cluster (centro)", zorder=5)

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
