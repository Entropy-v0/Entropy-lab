# 03. Styling & Aesthetics

Transform your charts from "basic" to "professional" by mastering styles, color palettes, and global configurations.

## 1. Built-in Styles
Matplotlib comes with pre-defined style sheets that instantly change the look of your plots.

```python
import matplotlib.pyplot as plt

# See available styles
print(plt.style.available)

# Apply a specific style
plt.style.use('ggplot')
# or
plt.style.use('seaborn-v0_8-darkgrid')
```

## 2. The Power of Seaborn
Seaborn is built on top of Matplotlib and makes styling incredibly easy. Even if you use plotting commands from Matplotlib, importing Seaborn and setting its style will upgrade your visuals.

```python
import seaborn as sns

# Basic professional style
sns.set_style("whitegrid")  # Options: darkgrid, whitegrid, dark, white, ticks

# Context scaling (adjusts font sizes for different mediums)
sns.set_context("notebook") # Options: paper, notebook, talk, poster
```

## 3. Fine-Grained Control (rc/rcParams)
For standardizing visuals across all your notebooks/projects, modify the global `rcParams`. This is efficient for setting company brand colors or specific font sizes once.

```python
# Set figure size globally
plt.rcParams['figure.figsize'] = (10, 6)

# Font sizes
plt.rcParams['font.size'] = 12
plt.rcParams['axes.titlesize'] = 16
plt.rcParams['axes.labelsize'] = 14

# Line thickness
plt.rcParams['lines.linewidth'] = 2
```

## 4. Color Palettes
Choosing the right colors is crucial for accessibility and aesthetics.

```python
# Seaborn Color Palettes
sns.color_palette("husl", 8)
sns.color_palette("coolwarm", as_cmap=True)

# Using specific hex codes
custom_colors = ["#FF5733", "#33FF57", "#3357FF"]
sns.set_palette(custom_colors)
```

## 5. Removing "Chart Junk"
Minimalism often leads to better communication.
```python
# Remove top and right spines (borders)
sns.despine()

# Remove specific spines manually
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
```

## Summary Checklist for Professional Plots
1.  **Grid**: Use a subtle grid (`whitegrid`) for readability.
2.  **Size**: Ensure figure size is adequate (`figsize=(10,6)`).
3.  **Fonts**: Increase label and title sizes for clarity.
4.  **Colors**: Use distinct, colorblind-friendly palettes.
5.  **Clean**: Remove unnecessary borders (`despine`).
