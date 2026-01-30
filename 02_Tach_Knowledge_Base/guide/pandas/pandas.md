# Guía de Ingeniería: Pandas

> **Dominio**: Data Analysis & Manipulation
> **Nivel**: Fundamental
> **Filosofía**: "Excel con esteroides y programable."

---

## 1. 🧠 Modelo Mental (The Big Picture)

*   **¿Qué es?**: La herramienta estándar de facto para la manipulación y análisis de datos estructurados (tabulares) en Python. Piénsalo como un Excel programable súper potente o SQL en memoria.
*   **¿Para qué sirve realmente?**: Para limpiar, transformar, agregar y preparar datos heterogéneos ("Data Wrangling") antes de alimentarlos a modelos de ML o visualizaciones.
*   **¿Cuándo NO usarlo?**:
    *   **Big Data real**: Si los datos no caben en la RAM -> Usa **Polars, Dask o Spark**.
    *   **Matrices puras**: Si solo son números sin etiquetas -> Usa **NumPy**.
    *   **Datos no estructurados**: Imágenes, audio, texto libre masivo -> Usa herramientas específicas.
*   **Conceptos Clave**:
    1.  **DataFrame**: Una tabla (hoja de cálculo). Colección de Series alineadas por un índice común.
    2.  **Series**: Una columna de la tabla. Es un array de NumPy con un índice etiquetado.
    3.  **Index**: El ADN de Pandas. Etiquetas para filas que permiten alineación automática y búsquedas rápidas (como una Primary Key).

---

## 2. 🧱 Sintaxis Crítica (Pareto 80/20)

### I/O (Entrada/Salida)
```python
import pandas as pd

# Lectura
df = pd.read_csv("data.csv")
df = pd.read_parquet("data.parquet") # Formato columnar binario eficiente

# Escritura
df.to_csv("output.csv", index=False) # ¡Ojo con index=False!
```

### Inspección Rápida
```python
df.head()        # Primeras 5 filas
df.sample(5)     # 5 filas aleatorias (mejor para ver diversidad)
df.info()        # Tipos de datos, memoria y nulos (Vital)
df.describe()    # Estadísticas básicas (min, max, mean, cuartiles)
df.shape         # (filas, columnas)
```

### Selección y Filtrado
**Olvida `df.ix`. Usa `loc`, `iloc` o máscaras.**

```python
# Selección por ETIQUETA (loc)
# df.loc[filas, columnas]
valor = df.loc[0, 'nombre']
subset = df.loc[:, ['nombre', 'edad']]

# Selección por POSICIÓN (iloc) - Estilo NumPy
fila_raw = df.iloc[0, :]

# Filtrado Booleano (Súper Común)
mask = (df['edad'] > 18) & (df['pais'] == 'AR')
adultos_ar = df[mask]

# Query (Syntax Sugar estilo SQL, bueno para cadenas largas)
adultos_ar = df.query("edad > 18 and pais == 'AR'")
```

### Manipulación y Agregación (Groupby style)
```python
# Agrupación simple
df.groupby('categoria')['precio'].mean()

# Agregaciones múltiples y nombradas
resumen = df.groupby('pais').agg(
    precio_promedio=('precio', 'mean'),
    total_ventas=('cantidad', 'sum'),
    clientes_unicos=('user_id', 'nunique')
)
```

### Limpieza Básica
```python
df.dropna()                    # Elimina filas con nulos
df.fillna(0)                   # Rellena nulos con un valor
df.drop_duplicates()           # Elimina filas repetidas
df['col'] = df['col'].astype('category') # Optimización de memoria
```

---

## 3. 💎 Patrones de Diseño y Best Practices

### Idiomatic: Method Chaining (Tuberías)
Evita crear cientos de variables temporales (`df1`, `df2`, `df_final`). Usa encadenamiento o `.pipe()`.

**❌ Amateur (Spaghetti):**
```python
df = pd.read_csv("data.csv")
df = df.dropna()
df = df[df['valor'] > 0]
df['doble'] = df['valor'] * 2
```

**✅ Pro (Fluent Interface):**
```python
df = (
    pd.read_csv("data.csv")
    .dropna()
    .query("valor > 0")
    .assign(doble=lambda x: x['valor'] * 2) # .assign es clave para nuevas cols en cadena
)
```

### Snippet de Oro: Vectorización sobre `apply()`
`df.apply()` es básicamente un bucle `for` disfrazado. Es LENTO.

*   **Malo**: `df['col'].apply(lambda x: x + 1)`
*   **Bueno**: `df['col'] + 1` (Vectorizado con NumPy)

Si tienes que procesar texto y no queda otra, usa `.str` accessor que está optimizado, o listas de comprensión.

### Snippet de Oro: `isin()` para Filtros Múltiples
Evita cadenas de `OR`.
```python
# Malo
df[(df['color'] == 'rojo') | (df['color'] == 'verde') | (df['color'] == 'azul')]

# Bueno (SQL IN)
df[df['color'].isin(['rojo', 'verde', 'azul'])]
```

---

## 4. ⚠️ Zona de Peligro (Anti-patterns & Gotchas)

### 1. `SettingWithCopyWarning`
Este es el error más famoso de Pandas. Ocurre cuando intentas modificar una **vista** de un DataFrame en lugar del original.

```python
# Malo: Chained indexing
df[df['A'] > 5]['B'] = 10  # Pandas no sabe si quieres modificar df o la copia temporal.

# Solución: Usa .loc
df.loc[df['A'] > 5, 'B'] = 10
```

### 2. Iterar filas (`iterrows`)
Si te encuentras escribiendo `for index, row in df.iterrows():`, detente. Estás matando el rendimiento. Casi siempre hay una forma vectorizada. Si **realmente** necesitas iterar, usa `itertuples()` que es mucho más rápido.

### 3. El infierno de `inplace=True`
Aunque parece eficiente, `inplace=True` raramente ahorra memoria bajo el capó y a menudo impide el encadenamiento de métodos (method chaining). El equipo de Pandas está considerando depreciarlo.
*   *Recomendación*: Asigna el resultado de vuelta (`df = df.drop(...)`) en lugar de usar `inplace=True`.

### 4. NaN vs None
Pandas usa `NaN` (float) para indicar datos faltantes en números, lo que puede convertir columnas de enteros a floats mágicamente.
*   *Gotcha*: `int` no soporta `NaN`.
*   *Solución moderna*: Usa el tipo de dato `Int64` (con mayúscula) de Pandas que permite nulos.
