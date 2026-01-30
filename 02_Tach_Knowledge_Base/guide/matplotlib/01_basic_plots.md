# 01. Gráficos Básicos

En esta sección exploraremos los tipos de gráficos más comunes en Matplotlib.

Importaciones necesarias para los ejemplos:

```python
import matplotlib.pyplot as plt
import numpy as np
```

## 1. Gráfico de Línea (`plot`)

Es el gráfico por defecto. Ideal para series temporales o funciones matemáticas.

```python
x = np.linspace(0, 10, 100)
y = np.sin(x)

fig, ax = plt.subplots()
ax.plot(x, y)
plt.show()
```

## 2. Gráfico de Dispersión (`scatter`)

Muestra la relación entre dos variables numéricas usando puntos.

```python
x = np.random.rand(50)
y = np.random.rand(50)
colors = np.random.rand(50)
sizes = 100 * np.random.rand(50)

fig, ax = plt.subplots()
ax.scatter(x, y, c=colors, s=sizes, alpha=0.5) # alpha controla la transparencia
plt.show()
```

## 3. Gráfico de Barras (`bar` y `barh`)

Útil para comparar categorías.

### Vertical

```python
categorias = ['A', 'B', 'C', 'D']
valores = [10, 24, 36, 15]

fig, ax = plt.subplots()
ax.bar(categorias, valores)
plt.show()
```

### Horizontal

Para barras horizontales usamos `barh`:

```python
fig, ax = plt.subplots()
ax.barh(categorias, valores)
plt.show()
```

## 4. Histograma (`hist`)

Muestra la distribución de una variable numérica.

```python
data = np.random.randn(1000) # Distribución normal

fig, ax = plt.subplots()
ax.hist(data, bins=30, edgecolor='black')
plt.show()
```

## 5. Boxplot (`boxplot`)

Para ver medidas estadísticas (mediana, cuartiles, outliers).

```python
data = [np.random.normal(0, std, 100) for std in range(1, 4)]

fig, ax = plt.subplots()
ax.boxplot(data, vert=True, patch_artist=True)
plt.show()
```
