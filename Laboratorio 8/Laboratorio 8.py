import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.colors import ListedColormap
#Flores Estopier Rodrigo


# Parámetros de la simulación
num_rows = 10  # Tamaño de la cuadrícula
num_cols = 80
nr = 3         # Número de pasos que una célula permanece refractaria
c = 0.1        # Umbral promedio (reducido)
delta_c = 0.05 # Variación del umbral
R = 2          # Radio de influencia
w0 = 0.1       # Peso direccional fuerte hacia la derecha

# Estados de las células: 0 = inactiva, 1 = activa, 2 a nr+1 = refractaria
grid = np.zeros((num_rows, num_cols), dtype=int)

# Iniciar con un punto activado
grid[5, 0] = 1
grid[6, 0] = 1
grid[7, 0] = 1

# Definir el mapa de colores: cada número representa un estado específico
cmap = ListedColormap(['black', 'red', 'orange', 'yellow', 'green'])  # Colores para inactivo, activo y diferentes estados refractarios

# Función para actualizar el estado de la cuadrícula
def update_grid(grid):
    new_grid = np.copy(grid)
    for i in range(num_rows):
        for j in range(num_cols):
            if grid[i, j] == 1:
                new_grid[i, j] = 2  # Pasar a estado refractario
            elif 2 <= grid[i, j] < 2 + nr:
                new_grid[i, j] += 1  # Avanzar en el estado refractario
            elif grid[i, j] >= 2 + nr:
                new_grid[i, j] = 0
            elif grid[i, j] == 0:
                # Calcular el nivel de activación desde las células vecinas
                activation_sum = 0
                num_neighbors = 0
                for di in range(-R, R + 1):
                    for dj in range(-R, R + 1):
                        ni, nj = i + di, j + dj
                        if 0 <= ni < num_rows and 0 <= nj < num_cols and (di != 0 or dj != 0):
                            weight = w0 if dj > 0 else (1 - w0)  # Preferencia hacia la derecha
                            activation_sum += weight * (grid[ni, nj] == 1)
                            num_neighbors += 1
                avg_activation = activation_sum / num_neighbors if num_neighbors > 0 else 0
                threshold = c + delta_c * (np.random.rand() - 0.5)
                if avg_activation > threshold:
                    new_grid[i, j] = 1  # Activar célula
    return new_grid

# Configurar la animación
fig, ax = plt.subplots()
im = ax.imshow(grid, cmap=cmap, vmin=0, vmax=nr + 1)

def animate(frame):
    global grid
    grid = update_grid(grid)
    im.set_array(grid)
    print(grid)
    return [im]

ani = animation.FuncAnimation(fig, animate, frames=300, interval=50, blit=True)

plt.show()
