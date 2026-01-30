# Guía de Ingeniería: Pandas Data Cleaning

> **Dominio**: Data Quality & Preparation
> **Nivel**: Fundamental / Intermedio
> **Filosofía**: "Tidy Data: Cada variable es una columna, cada observación es una fila."

---

## 1. 🧠 Modelo Mental (The Big Picture)

*   **¿Qué es?**: El proceso de detectar y corregir (o eliminar) datos corruptos, inexactos, irrelevantes o incompletos.
*   **¿Para qué sirve realmente?**: El 80% del trabajo de un Data Scientist. Los modelos de ML y los reportes de BI son basura si la entrada es basura ("Garbage In, Garbage Out").
*   **Conceptos Clave**:
    1.  **Missing Data**: `NaN`, `None`, o valores centinela como `-999`. No son errores, son información.
    2.  **Tidy Data**: Estructura estándar donde limpiar es fácil.
    3.  **Sanitización**: Convertir tipos (string "100" -> int 100) y estandarizar formatos (cadenas, fechas).

---

## 2. 🧱 Sintaxis Crítica (Pareto 80/20)

### Manejo de Nulos (Missing Values)
```python
# Detección
df.isna().sum()           # Conteo de nulos por columna (Vital)
df[df['col'].isna()]      # Filtrar filas que tienen nulos en 'col'

# Eliminación
df.dropna()               # Elimina cualquier fila con al menos un nulo
df.dropna(subset=['col']) # Elimina si el nulo está en columnas específicas
df.dropna(thresh=2)       # Mantener fila si tiene al menos 2 valores NO nulos

# Imputación (Relleno)
df.fillna(0)              # Rellenar todo con 0
df.fillna({'colA': 0, 'colB': 'Desconocido'}) # Relleno específico por columna
# Relleno inteligente (hacia adelante/atrás - común en series temporales)
df.ffill()                # Forward fill (usa el valor anterior)
```

### Duplicados
```python
# Detección
duplicados = df.duplicated()       # Retorna Series booleana
conteo = df.duplicated().sum()

# Eliminación
# keep='first' (defecto), 'last', o False (elimina todos)
df.drop_duplicates(subset=['id', 'fecha'], keep='last')
```

### Manipulación de Strings (`.str` accessor)
Vectorizado y mucho más rápido que bucles.
```python
s = df['nombre']

# Limpieza básica
s = s.str.strip()         # Quitar espacios al inicio/final
s = s.str.lower()         # Minúsculas
s = s.str.replace('$', '') # Quitar caracteres especiales

# Splitting
df[['nombre', 'apellido']] = s.str.split(' ', n=1, expand=True)
```

### Conversión de Tipos (Casting)
```python
# Explícito
df['precio'] = df['precio'].astype(float)

# Numérico forzado (coerción de errores)
# Convierte 'error' en NaN en lugar de fallar el script
df['edad'] = pd.to_numeric(df['edad'], errors='coerce')

# Fechas (El parseo es lento, optimiza el formato si puedes)
df['fecha'] = pd.to_datetime(df['fecha'], format='%Y-%m-%d')
```

---

## 3. 💎 Patrones de Diseño y Best Practices

### Cleaning Pipelines (`.pipe`)
La forma más elegante y mantenible de limpiar. Separa cada tarea de limpieza en una función pequeña.

```python
def limpiar_nombres(df):
    df['nombre'] = df['nombre'].str.strip().str.title()
    return df

def arreglar_precios(df):
    # Quitar '$' y convertir a float
    df['precio'] = (
        df['precio']
        .astype(str)
        .str.replace('$', '', regex=False)
        .astype(float)
    )
    return df

# Ejecución limpia
df_clean = (
    pd.read_csv('raw_data.csv')
    .pipe(limpiar_nombres)
    .pipe(arreglar_precios)
    .drop_duplicates()
)
```

### Snippet de Oro: Detección de Outliers (IQR)
Detectar valores extremos que pueden romper promedios.
```python
Q1 = df['valor'].quantile(0.25)
Q3 = df['valor'].quantile(0.75)
IQR = Q3 - Q1

# Define límites
lower = Q1 - 1.5 * IQR
upper = Q3 + 1.5 * IQR

# Filtra lo que está dentro del rango válido
df_normal = df[df['valor'].between(lower, upper)]
```

### Caso Real: Unidades Mixtas (Netflix)
Un problema clásico: tienes una columna `duration` que mezcla "90 min" (Películas) con "1 Season" (Series).

**Estrategia: Divide y Vencerás**
No intentes forzar todo a un solo número. Separa la cantidad de la unidad.

```python
# 1. Check what we have
# df['duration'].unique() -> ['90 min', '2 Seasons', ...]

# 2. Extract number and unit (Regex is your friend)
# (\d+) -> Capture numeric digits
# (\s+) -> Space
# (\w+) -> Capture words (min, Season, Seasons)
df[['amount', 'unit']] = df['duration'].str.extract(r'(\d+)\s+(\w+)')

# 3. Convert to numeric (now safe)
df['amount'] = pd.to_numeric(df['amount'])

# 4. Separate into clean columns by type
df['duration_minutes'] = np.where(df['unit'] == 'min', df['amount'], np.nan)
df['duration_seasons'] = np.where(df['unit'].str.contains('Season'), df['amount'], np.nan)

# 5. Drop temporary columns (Cleanup)
df = df.drop(columns=['amount', 'unit'])
```

### Caso Real: Listas en Celdas (One-to-Many)
Columna `listed_in`: "Comedies, Dramas, International Movies".
Tienes 1 película, pero pertenece a 3 géneros. ¿Cómo cuentas cuántos Dramas hay?

**Opción A: Explode (Para Análisis)**
Multiplica la fila por cada elemento de la lista. Si tenías 1 fila, ahora tienes 3.

```python
# 1. Convertir string a lista real
df['genre_list'] = df['listed_in'].str.split(', ')

# 2. Explode (La bomba atómica de Pandas 💣)
df_exploded = df.explode('genre_list')
# Ahora puedes agrupar:
# df_exploded['genre_list'].value_counts()
```

**Opción B: One-Hot (Para Machine Learning)**
Crea una columna por cada género posible (is_Comedy, is_Drama...)

```python
# Separa por coma y dummyfícalo
df_dummies = df['listed_in'].str.get_dummies(sep=', ')
df_final = pd.concat([df, df_dummies], axis=1)
```

---

## 4. ⚠️ Zona de Peligro (Anti-patterns & Gotchas)

### 1. Espacios Invisibles (" Phantom Strings ")
Un string `'Python '` (con espacio final) no es igual a `'Python'`.
*   Esto rompe `groupby`, `merge` y filtros de igualdad.
*   *Solución*: Siempre aplica `.str.strip()` a columnas string categóricas al cargar los datos.

### 2. Fechas Ambiguas
`01/02/2020`: ¿Es 1 de Febrero o 2 de Enero?
*   Pandas intentará adivinar, a veces mal.
*   *Siempre* especifica `dayfirst=True` o `format` explícito en `to_datetime`.

### 3. Mixed Types (DtypeWarning)
Al leer CSVs grandes, Pandas lee por chunks. Si un chunk tiene solo números y el siguiente tiene un string en la misma columna, Pandas entra en pánico. 
*   *Resultado*: Columna tipo `object` (la más lenta y memoria-ineficiente).
*   *Solución*: Define `dtype={...}` al cargar el CSV o fuerza la conversión con `to_numeric(errors='coerce')` inmediatamente.
