# Guía de Ingeniería: NumPy Avanzado (Internals & Optimization)

> **Dominio**: High-Performance Computing (HPC)
> **Nivel**: Avanzado / Experto
> **Filosofía**: "Controla la memoria, controlarás la velocidad."

---

## 1. 🧠 Modelo Mental (Deep Dive)

*   **¿Qué es realmente?**: Un gestor de punteros a bloques de memoria C contiguos. El objeto `ndarray` es solo una "vista" (metadatos) sobre esos bytes crudos.
*   **Objeto Clave: `strides` (Zancadas)**: El concepto más importante para entender la performance. Define cuántos bytes debe saltar el puntero para llegar al siguiente elemento en cada dimensión.
    *   *Ejemplo*: En un array C-order (row-major) `(3, 3)` de `int64` (8 bytes), los strides son `(24, 8)`. Moverse una fila cuesta 24 bytes, moverse una columna cuesta 8 bytes.
*   **Buffer Protocol**: NumPy implementa la interfaz de buffer de Python, permitiendo compartir memoria "Zero-Copy" con C, C++, Cython y otras librerías.

---

## 2. 🧱 Sintaxis Crítica (Herramientas de Poder)

### Einstein Summation (`einsum`)
La navaja suiza del álgebra lineal. Más rápido y legible que cadenas de `dot`, `transpose`, `sum`.
*   Sintaxis: `"ejes_input,ejex_input -> ejes_output"`

```python
A = np.array([[1, 2], [3, 4]])
B = np.array([[5, 6], [7, 8]])

# Multiplicación de matrices (dot product)
# ij: filas A, cols A (o filas B)
# jk: filas B, cols B
# ik: resultado (filas A, cols B) -> suma sobre j implícita
C = np.einsum('ij,jk->ik', A, B) 

# Diagonal (trace) -> 'ii->' (suma índices repetidos)
traza = np.einsum('ii->', A)

# Transpuesta -> 'ij->ji'
transpuesta = np.einsum('ij->ji', A)
```

### Broadcasting Avanzado & `newaxis`
Control explícito de dimensiones para forzar broadcasting.
```python
arr = np.arange(5) # (5,)
col = arr[:, np.newaxis] # (5, 1) - Transforma vector a columna
row = arr[np.newaxis, :] # (1, 5) - Transforma vector a fila

# Outer product manual
outer = col * row # (5, 1) * (1, 5) -> (5, 5)
```

### Structured Arrays (Tablas estilo C)
Permite mezclar tipos de datos en un solo bloque de memoria (similar a `structs` en C o DataFrames, pero nativo).
```python
data = np.zeros(3, dtype={'names':('name', 'age'), 'formats':('U10', 'i4')})
data[0] = ('Alice', 25)
# Acceso por campo (extremadamente rápido, devuelve vista)
edades = data['age'] 
```

---

## 3. 💎 Patrones de Diseño y Best Practices

### Manipulación de Strides (`as_strided`)
**Warning**: Magia negra. Permite crear vistas (ventanas deslizantes) sin copiar memoria.
Usa `lib.stride_tricks.sliding_window_view` (más seguro) para convoluciones manuales.

```python
from numpy.lib.stride_tricks import sliding_window_view

x = np.arange(6)
# Crea ventanas de tamaño 3
v = sliding_window_view(x, 3) 
# [[0, 1, 2], [1, 2, 3], [2, 3, 4], [3, 4, 5]]
# Costo de memoria: Casi 0 (es una vista).
```

### Memory Mapping (`memmap`)
Manejo de arrays más grandes que la RAM, mapeando un archivo en disco como su fuera memoria virtual.
```python
# Crea un archivo en disco y lo mapea como array
fp = np.memmap('data.dat', dtype='float32', mode='w+', shape=(10000, 10000))
fp[:] = data_masiva[:]
# El SO gestiona el paging (carga/descarga de RAM) automáticamente.
```

### Contigüidad y Performance (C vs Fortran)
NumPy prefiere `C-contiguous` (row-major). Operaciones que rompen la contigüidad (como transponer `arr.T` o slicing con pasos grandes) pueden degradar el cache hit rate de la CPU.
*   *Patrón*: Si vas a iterar/operar mucho sobre un array transpuesto o muy fragmentado, evalúa hacer `.copy()` o `np.ascontiguousarray()` para reordenar la memoria y ganar velocidad de CPU.

---

## 4. ⚠️ Zona de Peligro (Anti-patterns & Gotchas)

### 1. Memory Leaks con Vistas (El problema del "Base")
Si cortas un pedacito pequeño de un array gigante, el array gigante **NO** se libera de la memoria (Garbage Collection) porque la vista tiene un puntero a él (`.base`).

```python
video_gigante = load_4k_video() # 10 GB
thumbnail = video_gigante[0, :100, :100] 
del video_gigante 
# ¡Cuidado! Los 10GB siguen en RAM porque 'thumbnail' los mantiene vivos.
# Solución:
thumbnail = video_gigante[0, :100, :100].copy()
```

### 2. `nanmean` vs `mean`
En computación científica real, los `NaN` aparecen. Operaciones estándar (`sum`, `mean`) propagan el `NaN` y arruinan todo el cálculo.
*   Usa siempre las variantes "nan-safe": `np.nansum`, `np.nanmean`, `np.nanstd`.

### 3. Precisión Flotante (Floating Point Error)
Nunca compares floats con `==`. 
*   **Mal**: `if x == 0.1:`
*   **Bien**: `if np.isclose(x, 0.1):` o `np.allclose(arr1, arr2)`.
