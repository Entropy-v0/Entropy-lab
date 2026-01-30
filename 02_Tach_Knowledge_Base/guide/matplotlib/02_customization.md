# 02. Personalización y Estilo

Una vez que sabes crear gráficos básicos, el siguiente paso es hacerlos informativos y estéticamente agradables.

```python
import matplotlib.pyplot as plt
import numpy as np
x = np.linspace(0, 10, 100)
y = np.sin(x)
```

## 1. Títulos y Etiquetas

Es esencial etiquetar tus ejes para que el gráfico tenga sentido.

```python
fig, ax = plt.subplots()
ax.plot(x, y)

ax.set_title("Onda Sinusoidal")
ax.set_xlabel("Tiempo (s)")
ax.set_ylabel("Amplitud (V)")
plt.show()
```

## 2. Leyendas

Si tienes múltiples series, necesitas una leyenda.

```python
y2 = np.cos(x)

fig, ax = plt.subplots()
ax.plot(x, y, label='Seno')
ax.plot(x, y2, label='Coseno')

ax.legend() # Muestra la leyenda usando las etiquetas definidas en 'label'
plt.show()
```

## 3. Estilos de Línea y Marcadores

Puedes personalizar el color (`color` o `c`), estilo de línea (`linestyle` o `ls`) y marcadores (`marker`).

```python
fig, ax = plt.subplots()
ax.plot(x, y, color='red', linestyle='--', marker='o', markevery=10)
# shorthand: 'r--o' (red, dashed, circle)
plt.show()
```

## 4. Rejilla (Grid)

Ayuda a leer mejor los valores.

```python
fig, ax = plt.subplots()
ax.plot(x, y)
ax.grid(True, linestyle=':', alpha=0.6)
plt.show()
```

## 5. Límites de los Ejes

Para hacer zoom o fijar una vista específica.

```python
fig, ax = plt.subplots()
ax.plot(x, y)
ax.set_xlim(0, 5)
ax.set_ylim(-1, 1)
plt.show()
```

## 6. Guardar Gráficos

Para exportar tu gráfico a una imagen.

```python
fig.savefig('mi_grafico.png', dpi=300, bbox_inches='tight')
```
