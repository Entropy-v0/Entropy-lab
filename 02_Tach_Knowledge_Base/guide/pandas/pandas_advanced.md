# Guía de Ingeniería: Pandas Avanzado (Internals & Arquitectura)

> **Dominio**: Data Engineering & Optimization
> **Nivel**: Avanzado
> **Filosofía**: "Optimiza el almacenamiento, vectoriza la lógica."

---

## 1. 🧠 Modelo Mental (Deep Dive)

*   **Block Manager**: Pandas no almacena columnas individualmente como diccionarios (usualmente). Agrupa columnas del **mismo tipo de dato** en bloques contiguos de NumPy (`numpy.ndarray`).
    *   *Consecuencia*: Añadir una columna de un tipo nuevo puede disparar una copia costosa y reestructuración de la memoria interna.
*   **Index**: Es una estructura Hash Table (hash map) optimizada. Permite búsquedas `O(1)` (constante) en lugar de `O(N)` (lineal). Es lo que diferencia a Pandas de NumPy.
*   **Alignment**: La característica "mágica" (y peligrosa) de Pandas. Todas las operaciones binarias (`+`, `-`, `*`) alinean datos por **ÍNDICE**, no por posición física.

---

## 2. 🧱 Sintaxis Crítica (Herramientas de Poder)

### MultiIndex (Hierarchical Indexing)
Permite trabajar con altas dimensiones en estructura tabular 2D.
```python
# Creación
df.set_index(['pais', 'anio'], inplace=True)

# Slicing Avanzado (IndexSlice)
idx = pd.IndexSlice
# Seleccionar todas las filas de 'Argentina', años 2020 a 2025
subset = df.loc[idx['Argentina', 2020:2025], :]

# Pivot / Unstack (Mover índices a columnas)
tabla = df.unstack(level='anio') # Transforma formato 'largo' a 'ancho'
```

### pd.eval() & df.query() (NumExpr Engine)
Para DataFrames grandes (> 1M filas), Python es lento evaluando expresiones complejas por la creación de arrays temporales intermedios. `eval` compila la expresión a código byte de C (usando `numexpr`).

```python
# Lento (Python puro genera temporales: a+b, luego resultado > c)
mask = (df['a'] + df['b']) > df['c']

# Rápido & Memoria eficiente
mask = df.eval('(a + b) > c')
# O filtrado directo
subset = df.query('a + b > c')
```

### Categorical Data (La optimización #1)
Si tienes columnas de strings con baja cardinalidad (pocos valores únicos repetidos muchas veces, ej: "País", "Género", "Estado"), conviértelas a `Category`.
*   **Internals**: Pandas guarda un array de enteros (códigos) y un diccionario de mapeo.
*   **Ahorro**: Puede reducir uso de RAM en 10x-100x y acelerar GroupBy brutalmente.

```python
df['estado'] = df['estado'].astype('category')
```

---

## 3. 💎 Patrones de Diseño y Best Practices

### Custom Accessors (Extender Pandas)
El patrón oficial para agregar métodos propios a DataFrames (como plugins).
```python
@pd.api.extensions.register_dataframe_accessor("geo")
class GeoAccessor:
    def __init__(self, pandas_obj):
        self._obj = pandas_obj

    def centroide(self):
        # Lógica custom geoespacial
        return self._obj['lat'].mean(), self._obj['lon'].mean()

# Uso natural
df.geo.centroide()
```

### Explode (Desanidar listas)
Convierte listas dentro de celdas en filas duplicadas. Esencial para trabajar con datos JSON anidados.
```python
# Fila: {'id': 1, 'tags': ['A', 'B']}
df_exploded = df.explode('tags')
# Resultado:
# {'id': 1, 'tags': 'A'}
# {'id': 1, 'tags': 'B'}
```

### Pipe & Functional Patterns
Encapsula lógica de transformación compleja en funciones puras y encadénalas.
```python
def limpiar_precios(df, moneda='USD'):
    # ... logica ...
    return df

def filtrar_outliers(df, sigma=3):
    # ... logica ...
    return df

# Pipeline legible
df_limpio = (
    raw_data
    .pipe(limpiar_precios, moneda='EUR')
    .pipe(filtrar_outliers)
)
```

---

## 4. ⚠️ Zona de Peligro (Anti-patterns & Gotchas)

### 1. Fragmentation (Performance Killer)
Si haces muchos `df['nueva_col'] = ...` iterativamente, el Block Manager se fragmenta en cientos de bloques pequeños, degradando la performance.
*   *Solución*: Crea un diccionario o lista de todas las columnas nuevas y usa `pd.concat` o `assign` de una vez. O llama a `df = df.copy()` ocasionalmente para desfragmentar (compactar memoria).

### 2. reindex vs loc
Un error sutil:
*   `loc['A']`: Falla si 'A' no existe (KeyError).
*   `reindex(['A'])`: **NO** falla. Devuelve una fila llena de `NaN` si 'A' no existe.
*   *Peligro*: Si usas `reindex` y tienes un typo en un ID, inyectarás `NaN`s silenciosamente en tus datos.

### 3. Mutabilidad de Índices
Aunque el objeto `Index` es inmutable, la columna asignada como índice puede no ser única (a diferencia de una PK en SQL).
*   `df.loc['duplicado']` devolverá un DataFrame, no una Series (una fila). Esto rompe pipelines que esperan siempre un solo resultado.
*   *Best Practice*: Usa `df.index.is_unique` para verificar integridad antes de operaciones críticas.
