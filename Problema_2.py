import random
import math
import pandas as pd
import matplotlib.pyplot as plt

# Parámetros iniciales
D = 100  # Diámetro
N = 1000  # Total de personas
I = 1  # Inicialmente infectados
S = N - I  # Inicialmente susceptibles
R = 0  # Inicialmente recuperados
r_infeccion = 0.6  # Radio de infección
razon_recuperacion = 0.1  # Razón de recuperación

# Verificar que N = I + S + R
assert N == I + S + R, "El total de personas no coincide con N."

# Listas para las variables
x_positions = []
y_positions = []
estados = ['Infectado'] * I + ['Susceptible'] * S + ['Recuperado'] * R  # Lista inicial de estados
ids = list(range(1, N + 1))  # Identificadores únicos
iteraciones = [0] * N  # Iteración inicial para todas las personas

# posiciones iniciales para cada persona
for _ in range(N):
    a = random.random() * 2 * math.pi  # Ángulo aleatorio en radianes
    r = (D / 2) * math.sqrt(random.random())  # Distancia radial
    x = r * math.cos(a)  # Coordenada x
    y = r * math.sin(a)  # Coordenada y
    x_positions.append(x)
    y_positions.append(y)

# dataframe con las variables
data = pd.DataFrame({
    'id': ids,
    'x': x_positions,
    'y': y_positions,
    'estado': estados,
    'iteracion': iteraciones
})
print(data)

# Función para calcular la distancia euclidiana
def distancia_euclidiana(x1, y1, x2, y2):
    distancia = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    return distancia < r_infeccion  # Retorna True si está dentro del radio de infección

# Graficar la ciudad con los estados iniciales
plt.figure(figsize=(8, 8))
for estado, color in zip(['Susceptible', 'Infectado', 'Recuperado'], ['green', 'red', 'blue']):
    subset = data[data['estado'] == estado]
    plt.scatter(subset['x'], subset['y'], s=5, alpha=0.6, label=estado, color=color)

# Contorno del círculo
circle = plt.Circle((0, 0), D / 2, color='black', fill=False, linestyle='-', linewidth=1.5)
plt.gca().add_artist(circle)
plt.gca().set_aspect('equal', adjustable='box')
plt.title("Ciudad Circular con Estados Iniciales")
plt.xlabel("Coordenada x")
plt.ylabel("Coordenada y")
plt.legend()
plt.grid(True)
plt.show()

# uso de la función de distancia
#x1, y1 = data.loc[0, ['x', 'y']]
#x2, y2 = data.loc[1, ['x', 'y']]
#print(f"¿Dentro del radio de infección?: {distancia_euclidiana(x1, y1, x2, y2)}")
