# Guía de Ingeniería: Python Dictionaries

> **Dominio**: Estructuras de Datos Core
> **Nivel**: Fundamental
> **Filosofía**: "O(1) es vida. Si necesitas buscar rápido, usa un dict."

---

## 1. 🧠 Modelo Mental (The Big Picture)

*   **¿Qué es?**: Una colección desordenada (aunque preserva orden de inserción desde Python 3.7+) de pares Key-Value.
*   **¿Para qué sirve realmente?**: Para realizar búsquedas ("lookups") instantáneas. En Computer Science se llama **Hash Map** o **Hash Table**.
*   **¿Cuándo NO usarlo?**:
    *   Si necesitas ordenamiento por valor (Usa listas o `heap`).
    *   Si solo necesitas valores únicos sin asociar datos (Usa `feature_flags = {'A', 'B'}`, es decir, un `Set`).
*   **Conceptos Clave**:
    1.  **Hashable**: Las Keys DEBEN ser inmutables (Strings, Ints, Tuplas). No puedes usar una Lista como llave.
    2.  **O(1)**: El tiempo que tarda en encontrar un elemento es constante, no importa si el dict tiene 10 elementos o 10 millones.
    3.  **Key Uniqueness**: No puede haber llaves duplicadas. Si asignas de nuevo, sobrescribes.

---

## 2. 🧱 Sintaxis Crítica (Pareto 80/20)

### Creación y Acceso
```python
# Literal (La forma más rápida)
user = {
    "id": 1,
    "name": "Alice",
    "active": True
}

# Constructor (Bueno para kwargs)
config = dict(host='localhost', port=8080)

# Acceso
print(user['name'])       # "Alice"
# print(user['email'])    # ERROR: KeyError (si no existe)

# Acceso Seguro (Recomendado)
email = user.get('email') # Retorna None si no existe
role = user.get('role', 'guest') # Retorna 'guest' por defecto
```

### Modificación
```python
user['email'] = 'alice@mail.com'  # Insertar o Actualizar
del user['active']                # Eliminar (falla si no existe)
age = user.pop('age', 0)          # Elimina y devuelve valor (seguro)

# Merge (Python 3.9+)
extra_info = {"city": "NY", "id": 99}
# El segundo sobrescribe al primero en colisiones (id será 99)
merged = user | extra_info 
```

### Iteración (Lo más usado)
```python
# Iterar llaves (defecto)
for key in user:
    print(key)

# Iterar items (desempaquetado)
for k, v in user.items():
    print(f"{k}: {v}")
```

---

## 3. 💎 Patrones de Diseño y Best Practices

### Dictionary Comprehensions
La forma "Pythonic" de transformar diccionarios o crearlos desde listas.
```python
users = [('Alice', 25), ('Bob', 30)]

# Crear dict desde lista
user_age = {name: age for name, age in users}

# Filtrar y transformar
# { 'ALICE': 25, ... } solo si son mayores de 20
processed = {k.upper(): v for k, v in user_age.items() if v > 20}
```

### `defaultdict` (Adiós `KeyError`)
Ideal para contadores o agrupar datos. Inicializa valores automáticamente si la llave no existe.
```python
from collections import defaultdict

# Agrupar palabras por letra inicial
groups = defaultdict(list) 
words = ['apple', 'banana', 'apricot', 'cherry']

for word in words:
    # Si 'a' no existe, crea una lista vacía y hace append
    groups[word[0]].append(word) 
```

### `setdefault` (La alternativa built-in)
Si no quieres importar `defaultdict`.
```python
counts = {}
for char in "abracadabra":
    # Si char no está, ponlo en 0. Luego suma 1.
    counts[char] = counts.get(char, 0) + 1
```

---

## 4. ⚠️ Zona de Peligro (Anti-patterns & Gotchas)

### 1. Mutable Keys (El error de novato)
Las llaves deben ser **Hashables** (inmutables).
```python
# ❌ Error
coords = {[0, 1]: "Home"} # TypeError: unhashable type: 'list'

# ✅ Solución: Usa Tuplas
coords = {(0, 1): "Home"} 
```

### 2. Hash Collision Denial (DoS attack)
En versiones antiguas de Python (y otros lenguajes), si un atacante conoce tu función de hash, puede enviar miles de keys que colisionan (mismo hash), degradando el rendimiento de `O(1)` a `O(n)`.
*   *Nota*: Python moderno usa randomización de hash en cada reinicio del proceso para evitar esto.

### 3. Modificar mientras iteras
Nunca agregues o elimines llaves mientras iteras el mismo diccionario.
```python
data = {'a': 1, 'b': 2}
for k in data:
    if k == 'a':
        del data[k] # RuntimeError: dictionary changed size during iteration
        
# Solución: Itera sobre una copia de las llaves
for k in list(data.keys()):
    del data[k]
```
