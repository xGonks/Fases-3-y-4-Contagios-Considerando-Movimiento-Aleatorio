""" Solución Probelma 4"""


import math
import random
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def polares_rectangulares(a, r):
    x = r * math.cos(a)
    y = r * math.sin(a)
    return x, y


def distancia(x1, y1, x2, y2, r):
    if (math.sqrt(((x1 - x2)**2)+((y1 - y2)**2)) < r):
        return True
    else:
        return False


D = int(input("Diametro = "))
N = int(input("No. de personas = "))


R = 0
I = 1
S = N - I - R


radio_infeccion = float(input("Radio de infeccion = "))
razon_recuperacion = float(input("Razon de recuperacion = "))


cluster_a = random.uniform(0, 2*np.pi)
cluster_r = random.uniform(0, D/2)
cluster_x, cluster_y = polares_rectangulares(cluster_a, cluster_r)


posicion_x = []
posicion_y = []
while (len(posicion_x) < N):
    x = np.random.normal(loc=cluster_x, scale=D/20)
    y = np.random.normal(loc=cluster_y, scale=D/20)
    if ((x**2) + (y**2) < (D/2)**2):
        posicion_x.append(x)
        posicion_y.append(y)
estado = []
for i in range(int(S)):
    estado.append("Suceptible")
for j in range(int(I)):
    estado.append("Infectado")
for k in range(int(R)):
    estado.append("Recuperado")
id = []
iteracion = []
for m in range(int(N)):
    id.append(m)
    iteracion.append(0)


d = {'posición x': posicion_x, 'posición y': posicion_y,
     'estado': estado, 'id único': id, 'iteracion': iteracion}
df = pd.DataFrame(data=d)
print(df)
print(df.info())


theta = np.linspace(0, 2 * np.pi, 100)
circle_x = (D / 2) * np.cos(theta)
circle_y = (D / 2) * np.sin(theta)
# Crear la gráfica
plt.figure(figsize=(8, 8))
plt.plot(circle_x, circle_y, color="blue", label="(x^2) + (y^2) = (D/2)^2")
plt.scatter(posicion_x, posicion_y, color="black",
            s=10, label="Puntos (personas)")
plt.axhline(0, color='gray', linewidth=0.5)
plt.axvline(0, color='gray', linewidth=0.5)
plt.scatter(cluster_x, cluster_y, color="green",
            s=50, label="Cluster (centro)", zorder=5)
# Configuración de la gráfica
plt.gca().set_aspect('equal', adjustable='box')
plt.xlim(-D / 2 - 5, D / 2 + 5)
plt.ylim(-D / 2 - 5, D / 2 + 5)
plt.xlabel("X")
plt.ylabel("Y")
plt.legend()
plt.title("Distribución de puntos alrededor del cluster")
plt.grid(True)
plt.show()
