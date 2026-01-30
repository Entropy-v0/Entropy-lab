# Guía de Ingeniería: Pandas Data Types (dtypes)

> **Dominio**: Optimización y Tipado
> **Nivel**: Fundamental
> **Filosofía**: "Tipos correctos = 10x Velocidad + 1/10 Memoria"

---

## 1. 🧠 Modelo Mental (The Big Picture)

*   **¿Qué es?**: La definición de cómo se guardan los bits en memoria RAM para cada columna. Pandas usa tipos de NumPy (`int64`, `float64`) más sus propias extensiones (`Category`, `Int64`, `DatetimeTZ`).
*   **La Pregunta del Millón**: *¿Por qué "Nombres" es `object`/`string` y no `Category`?*
    *   **Cardinalidad**: `Category` es eficiente cuando hay **pocos valores únicos repetidos muchas veces** (ej: "Argentina", "Brasil", "Chile").
    *   **Nombres Propios**: Si tienes 1 millón de usuarios, probablemente tengas 900,000 nombres únicos. Crear un índice (`Category`) es más pesado que guardar el texto crudo.
    *   **Regla**: Usa `Category` si `unique_values < total_values / 2` (o idealmente mucho menos).
*   **`object` vs `string`**: Históricamente, Pandas usaba `object` (punteros a objetos Python) para texto. Desde Pandas 1.0+, existe `string` (o `string[pyarrow]`) que es más estricto y seguro.

---

## 2. 🧱 Sintaxis Crítica (Pareto 80/20)

### Los Tipos Estándar
| Pandas dtype | Python type | Uso | Notas |
| :--- | :--- | :--- | :--- |
| `int64` | `int` | Números enteros | **NO** acepta `NaN`. |
| `float64` | `float` | Decimales | Acepta `NaN` (si un int tiene NaN, se vuelve float). |
| `bool` | `bool` | True/False | - |
| `object` | `str` / `mixed` | Texto o mezclas | Lento. Es el "catch-all". |
| `category` | - | Enums / Pocos valores | Ahorra RAM en baja cardinalidad. |
| `datetime64[ns]` | `datetime` | Fechas y tiempo | Muy rápido para filtrar por tiempo. |
| `timedelta64[ns]` | `timedelta` | Diferencias de tiempo | Resta de dos fechas. |

### Conversión (`astype`)
```python
# Explícita
df['precio'] = df['precio'].astype(float)
df['pais'] = df['pais'].astype('category')

# Masiva
df = df.astype({'id': 'int32', 'activo': bool})

# Numérico Seguro (Manejo de errores)
df['input_sucio'] = pd.to_numeric(df['input_sucio'], errors='coerce')
# '10' -> 10, 'abc' -> NaN (en lugar de crashear)
```

### Inspección
```python
df.dtypes               # Lista de tipos por columna
df.info(memory_usage='deep') # ¡Vital! Muestra uso real de RAM (incluyendo strings)
```

---

## 3. 💎 Patrones de Diseño y Best Practices

### Nullable Integers (`Int64`)
Históricamente, si tenías una columna de enteros y **un** solo `NaN`, Pandas convertía toda la columna a `float64` (perdiendo precisión si eran IDs largos).
*   **Solución**: Usa `Int64` (mayúscula I).

```python
# Entero normal (dtype='float64' si hay nulos)
s = pd.Series([1, 2, np.nan]) 

# Nullable Integer (dtype='Int64')
s_new = pd.Series([1, 2, np.nan], dtype="Int64")
```

### Optimización de Memoria (Downcasting)
No siempre necesitas 64 bits.
*   `int8`: -128 a 127 (Ej: Edad)
*   `float32`: Menos precisión, mitad de RAM.

```python
# Ahorro masivo en datasets grandes
df['edad'] = df['edad'].astype('int8') 
```

### Categorical Optimization
Transforma strings repetitivos a enteros bajo el capó.
```python
# 1GB de strings repetidos ("Rojo", "Verde", "Azul") 
# -> se convierte en pocos KBs de enteros (0, 1, 2) + diccionario.
df['color'] = df['color'].astype('category')
```

---

## 4. ⚠️ Zona de Peligro (Anti-patterns & Gotchas)

### 1. `object` no es solo String
Si una columna es `object`, puede contener CUALQUIER COSA: enteros, strings, listas, diccionarios, o todo mezclado.
*   *Peligro*: Las operaciones vectorizadas fallan.
*   *Check*: `df['col'].apply(type).value_counts()` para ver qué hay realmente ahí dentro.

### 2. La trampa del bool
En CSVs, `"False"` (string) es evaluado como `True` si haces `bool("False")` en Python básico.
*   Pandas `read_csv` suele ser inteligente, pero ten cuidado al convertir manualmente. Usa map:
    `df['col'].map({'True': True, 'False': False})`

### 3. Fechas como Strings
Lo peor que puedes hacer es dejar fechas como `object`.
*   Ordenar `"01/02/2021"` vs `"02/01/2021"` alfabéticamente da resultados incorrectos.
*   *Siempre* convierte a `datetime64`.
