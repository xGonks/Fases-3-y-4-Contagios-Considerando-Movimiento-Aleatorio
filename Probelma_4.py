""" Solución Problema 4"""

import math
import random
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Función para calcular la distancia euclidiana entre dos puntos
def distancia(p1, p2):
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2) < radio_infeccion

# Entradas con verificación de datos
while True:
    try:
        D = int(input("Lado del cuadrado (entero) = "))
        N = int(input("Número de personas (entero) = "))
        break  # Salir del bucle si las entradas son correctas
    except ValueError:
        print("Por favor, ingrese un número entero válido para el lado del cuadrado y el número de personas.")

# Definición del radio de infección y razón de recuperación
radio_infeccion = float(input("Radio de infección (ej. 0.6) = "))
razon_recuperacion = float(input("Razón de recuperación = "))

# Inicialización de variables I, S, R
I = 1  # Al menos una persona infectada
R = 0  # Inicialmente no hay recuperados
S = N - I - R  # Resto de personas son susceptibles

# Asignar estados iniciales
estado = ["Infectado"] * I + ["Susceptible"] * S + ["Recuperado"] * R
random.shuffle(estado)  # Mezclar los estados para distribuirlos al azar

# Definir el punto de preferencia en el área cuadrada
cluster_x = random.uniform(-D/2, D/2)
cluster_y = random.uniform(-D/2, D/2)

# Generar posiciones de las personas alrededor del punto de preferencia
posicion_x = []
posicion_y = []
while len(posicion_x) < N:
    x = np.random.normal(loc=cluster_x, scale=D / 20)
    y = np.random.normal(loc=cluster_y, scale=D / 20)
    # Condición para asegurar que las personas estén dentro de los límites del cuadrado
    if (-D/2 <= x <= D/2) and (-D/2 <= y <= D/2):
        posicion_x.append(x)
        posicion_y.append(y)

# Crear identificadores únicos y asignar una iteración inicial
id_unico = list(range(N))
iteracion = [0] * N

# Crear el DataFrame con la información
df = pd.DataFrame({
    'posición x': posicion_x,
    'posición y': posicion_y,
    'estado': estado,
    'id único': id_unico,
    'iteracion': iteracion
})

print(df)
print(df.info())

# Graficar la distribución de personas en el cuadrado
plt.figure(figsize=(8, 8))
plt.plot([-D/2, D/2, D/2, -D/2, -D/2], [-D/2, -D/2, D/2, D/2, -D/2], color="blue", label="Frontera del cuadrado")
plt.scatter(posicion_x, posicion_y, color="black", s=10, label="Personas")
plt.scatter(cluster_x, cluster_y, color="green", s=50, label="Centro del cluster", zorder=5)
plt.axhline(0, color='gray', linewidth=0.5)
plt.axvline(0, color='gray', linewidth=0.5)

plt.gca().set_aspect('equal', adjustable='box')
plt.xlim(-D / 2 - 5, D / 2 + 5)
plt.ylim(-D / 2 - 5, D / 2 + 5)
plt.xlabel("X")
plt.ylabel("Y")
plt.legend()
plt.title("Distribución de personas alrededor del centro preferido en un área cuadrada")
plt.grid(True)
plt.show()
