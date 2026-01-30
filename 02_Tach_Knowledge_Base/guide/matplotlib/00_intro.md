# 00. Introducción a Matplotlib

## ¿Qué es Matplotlib?

Matplotlib es la biblioteca fundamental para la visualización de datos en Python. Es extremadamente potente y flexible, permitiendo crear gráficos estáticos, animados e interactivos de alta calidad.

Aunque existen bibliotecas de más alto nivel como Seaborn (que se construye sobre Matplotlib), entender Matplotlib es crucial para tener un control total sobre tus visualizaciones.

## Instalación

Para instalar Matplotlib, utiliza pip:

```bash
pip install matplotlib
```

## Importación Convencional

La forma estándar de importar la biblioteca es:

```python
import matplotlib.pyplot as plt
```

`pyplot` es el módulo que nos da una interfaz similar a MATLAB y es la forma principal de interactuar con la biblioteca.

## Anatomía de un Gráfico

Es fundamental entender los dos objetos principales en Matplotlib:

1.  **Figure (Figura)**: Es el contenedor de todo (el "lienzo" o ventana). Puede contener uno o más gráficos.
2.  **Axes (Ejes)**: Es lo que comúnmente llamamos "el gráfico" (plot). Contiene los datos, ejes x/y, etiquetas, título, etc. Una `Figure` puede tener múltiples `Axes`.

### El Enfoque Orientado a Objetos (Recomendado)

Aunque existe un estilo "rápido" (state-based), se recomienda usar el estilo orientado a objetos para mayor control:

```python
import matplotlib.pyplot as plt
import numpy as np

# Datos
x = np.linspace(0, 10, 100)
y = np.sin(x)

# 1. Crear Figura y Ejes
fig, ax = plt.subplots()

# 2. Graficar en el objeto ax
ax.plot(x, y)

# 3. Personalizar usando métodos del objeto ax
ax.set_title("Gráfico de Seno")
ax.set_xlabel("Eje X")
ax.set_ylabel("Eje Y")

# 4. Mostrar
plt.show()
```
