# Suggested Structure for Data Cleaning Notebook

A professional notebook reads like a story: Introduction, Body, and Conclusion. Here is the ideal structure to refactor your work in `01-Data_Cleaning.ipynb`.

## 1. Init & Config
Load all libraries at the very beginning.
```python
import pandas as pd
import numpy as np
# Optional config to see all columns
pd.set_option('display.max_columns', None)
```

## 2. Data Ingestion (Load)
Read the raw file. Do not perform transformations here, just reading.
```python
df = pd.read_csv('../data/raw/netflix1.csv')
```

## 3. Initial Audit
Before touching anything, see what you have.
```python
# Quick view
df.head()
# Metadata (Types and Nulls)
df.info()
# Raw duplicate check
print(f"Duplicates: {df.duplicated().sum()}")
```

## 4. Cleaning (The Meat)
Divide this into logical sections with Markdown headers.

### 4.1. Type Conversion (Cast)
Fix incorrect types first (`date_added`, `show_id`).
```python
df['date_added'] = pd.to_datetime(df['date_added'])
# Optional if not read correctly
df['show_id'] = df['show_id'].astype(str) 
```

### 4.2. Duration Fix (Divide & Conquer)
Separate minutes from seasons.
```python
# Extract and conversion
# ... your regex code ...
# Cleaning temporary columns
df = df.drop(columns=['amount', 'unit'])
```

### 4.3. List Handling
The `listed_in` and `genre_list` column.
```python
df['genre_list'] = df['listed_in'].str.split(', ')
```

### 4.4. Null Handling (Imputation)
Decide what to do with remaining NaNs.
```python
# Optional: Fill director nulls with 'Unknown'
df['director'] = df['director'].fillna('Unknown')
```

## 5. Final Verification (QA)
Ensure the result is what you expected.
```python
# Check final types
df.info()
# Control statistics
df[['duration_minutes', 'duration_seasons']].describe()
```

## 6. Export
Save the clean result to avoid running everything again.
```python
# Save to parquet (faster and preserves types) or csv
df.to_parquet('../data/processed/netflix_cleaned.parquet')
# df.to_csv('../data/processed/netflix_cleaned.csv', index=False)
```
