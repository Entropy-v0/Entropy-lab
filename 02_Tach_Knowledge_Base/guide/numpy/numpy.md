# Guía de Ingeniería: NumPy (Numerical Python)

> **Dominio**: Data Science & Scientific Computing
> **Nivel**: Fundamental
> **Filosofía**: "Vectoriza, no iteres."

---

## 1. 🧠 Modelo Mental (The Big Picture)

*   **¿Qué es?**: El bloque fundacional para la computación numérica eficiente en Python; provee arrays multidimensionales de alto rendimiento y herramientas para trabajar con ellos.
*   **¿Para qué sirve realmente?**: Para realizar operaciones matemáticas masivas sobre conjuntos de datos numéricos (álgebra lineal, transformadas, estadística) a velocidades cercanas a C/C++, sin perder la sintaxis de Python. Es el motor bajo el capó de Pandas, Scikit-Learn y TensorFlow.
*   **¿Cuándo NO usarlo?**:
    *   Si necesitas etiquetas en tus datos (Columnas con nombres) -> Usa **Pandas**.
    *   Si tienes datos tabulares heterogéneos (mezcla de strings, ints, objects) -> Usa **Pandas** o una base de datos.
    *   Para listas pequeñas o genéricas de Python donde el overhead de NumPy no justifica la ganancia.
*   **Conceptos Clave**:
    1.  **ndarray (N-dimensional array)**: Un bloque de memoria contiguo y tipado (todos los elementos son del mismo tipo), infinitamente más rápido que una lista de Python para matemáticas.
    2.  **Vectorización**: Aplicar operaciones a todo el array de una vez (sin bucles `for`).
    3.  **Broadcasting**: La regla mágica que permite operar arrays de diferentes formas (shapes) de manera inteligente.

---

## 2. 🧱 Sintaxis Crítica (Pareto 80/20)

Lo que usarás el 80% del tiempo en el día a día.

### Creación e Inspección
```python
import numpy as np

# Desde lista
arr = np.array([1, 2, 3])

# Generadores comunes
zeros = np.zeros((3, 3))        # Matriz 3x3 de ceros
ones = np.ones((2, 5))          # Matriz 2x5 de unos
range_arr = np.arange(0, 10, 2) # [0, 2, 4, 6, 8] (como range)
linspace = np.linspace(0, 1, 5) # [0. , 0.25, 0.5 , 0.75, 1. ] (5 puntos equiespaciados)

# Aleatorio (muy usado en ML)
rand = np.random.rand(3, 2)     # Distribución uniforme [0, 1)
randn = np.random.randn(3, 2)   # Distribución normal (Gaussiana)

# Inspección
print(arr.shape)  # Dimensiones: (3,)
print(arr.dtype)  # Tipo de dato: int64
print(arr.ndim)   # Número de ejes: 1
```

### Selección y Filtrado (Indexing & Slicing)
```python
mat = np.array([[10, 20, 30], [40, 50, 60]])

# Slicing básico [filas, columnas]
elemento = mat[0, 1]    # 20 (Fila 0, Col 1)
fila = mat[0, :]        # [10, 20, 30]
columna = mat[:, 1]     # [20, 50]

# Boolean Masking (¡Súper Poder!)
mask = mat > 30         # Retorna matriz booleana
filtrado = mat[mat > 30] # [40, 50, 60] - Retorna array 1D aplanado
```

### Operaciones Matemáticas (Agregaciones)
```python
# A todo el array
total = mat.sum()
promedio = mat.mean()
maximo = mat.max()

# Por ejes (axis 0 = colapsar filas/vertical, axis 1 = colapsar columnas/horizontal)
suma_cols = mat.sum(axis=0) # [50, 70, 90]
suma_filas = mat.sum(axis=1) # [60, 150]
```

---

## 3. 💎 Patrones de Diseño y Best Practices

### Idiomatic Code: "Death to For-Loops"
Escribir bucles `for` en Python puro sobre arrays de NumPy es un pecado capital de rendimiento.

**❌ Amateur (Lento):**
```python
# Sumar dos listas elemento a elemento
a = [1, 2, 3]
b = [4, 5, 6]
c = []
for i in range(len(a)):
    c.append(a[i] + b[i])
```

**✅ Pro (Vectorizado - Rápido):**
```python
a = np.array([1, 2, 3])
b = np.array([4, 5, 6])
c = a + b  # La operación se aplica en C, a nivel de CPU
```

### Snippet de Oro: Reshape & Flatten
Cambiar la forma de los datos es vital para preparar inputs de redes neuronales o matrices.
```python
arr = np.arange(12)  # [0, ..., 11]

# Reshape (debe mantener el número total de elementos)
matriz = arr.reshape(3, 4) # 3 filas, 4 columnas

# Flatten (aplanar)
plano = matriz.flatten()   # Crea una COPIA 1D
ravel = matriz.ravel()     # Crea una VISTA 1D (más rápido, pero cuidado al modificar)
```

### Snippet de Oro: np.where (If-Else vectorizado)
Reemplaza lógica condicional compleja.
```python
# Si valor > 5, pon 1, sino 0
datos = np.array([3, 6, 2, 8, 5])
binarizado = np.where(datos > 5, 1, 0) # [0, 1, 0, 1, 0]
```

---

## 4. ⚠️ Zona de Peligro (Anti-patterns & Gotchas)

### 1. The "View" Trap (Slicing no copia)
A diferencia de las listas de Python, **el slicing de NumPy devuelve una vista (referencia), no una copia**.
```python
arr = np.array([1, 2, 3, 4])
sub_arr = arr[0:2]
sub_arr[0] = 99

print(arr) # ¡[99, 2, 3, 4]! El original fue modificado.
# Solución: Usa .copy() si necesitas independencia.
sub_arr = arr[0:2].copy()
```

### 2. Tipos de Datos Silenciosos
NumPy infiere tipos y es estricto. Si intentas meter un float en un array de ints, truncará sin avisar (en versiones antiguas) o casteará todo el array a float al crearlo.
```python
enteros = np.array([1, 2, 3])
enteros[0] = 3.99  # Se convierte en 3 (truncado) si el array ya era int.
```

### 3. Broadcasting Errors
El broadcasting es genial hasta que falla silenciosamente o explota.
*   Regla: Las dimensiones deben ser iguales, o una de ellas debe ser 1.
*   Error común: Operar un array `(10,)` con uno `(10, 1)`. A veces funciona inesperadamente generando matrices gigantes `(10, 10)`.
*   *Tip*: Siempre verifica `.shape` cuando debuguees bugs matemáticos.

---


> "NumPy es la base. Si entiendes cómo piensa NumPy (bloques de memoria, ejes y vectorización), entiendes la computación científica moderna."
