import numpy as np
import pandas as pd
import seaborn as sns
import scipy.stats as stats
import matplotlib.pyplot as plt

# Sample DataFrame
df = pd.read_excel("bilgisayar.xlsx")
df = df.iloc[:, 2:]

# Calculate the correlation matrix and p-values
correlation_matrix = df.corr()
p_values = pd.DataFrame(np.zeros_like(correlation_matrix), columns=df.columns, index=df.columns)

for col1 in df.columns:
    for col2 in df.columns:
        if col1 != col2:  # Skip self-correlation
            _, p_value = stats.pearsonr(df[col1], df[col2])
            p_values.loc[col1, col2] = p_value

# Create a mask to hide the upper triangle
mask = np.triu(np.ones_like(correlation_matrix, dtype=bool))

# Plot the correlation matrix with only the lower triangle
plt.figure(figsize=(12, 9))
ax = sns.heatmap(
    correlation_matrix, 
    annot=True, 
    fmt=".2f", 
    cmap='Spectral',  # You can replace 'Spectral' with 'coolwarm' or 'RdYlBu' for variety
    vmin=-1, 
    vmax=1, 
    cbar_kws={'shrink': 1.0}, 
    mask=mask,
    annot_kws={"size": 14, "weight": "bold"}  # Making annotations bold for readability
)

ax.tick_params(axis='x', labelsize=14, rotation=45)  # X-axis: larger font, rotated
ax.tick_params(axis='y', labelsize=14, rotation=0)   # Y-axis: larger font, no rotation

# Overlay p-values in a second line below the correlation coefficients
for i in range(len(p_values)):
    for j in range(i):  # Only go through the lower triangle
        ax.text(j + 0.5, i + 0.7, f"p={p_values.iloc[i, j]:.2g}",
                ha='center', va='center', color='black', fontsize=12)

plt.tight_layout()
plt.show()
