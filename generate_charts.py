# ============================================
# generate_charts.py - Run this once
# ============================================

import matplotlib.pyplot as plt
import seaborn as sns
import os
import numpy as np

# Create static folder
os.makedirs('static', exist_ok=True)

print("Generating charts...")

# 1. Hourly Consumption Chart
plt.figure(figsize=(12, 6))
hours = list(range(24))
values = [18, 17, 16, 15, 14, 15, 18, 22, 28, 32, 36, 40, 42, 41, 38, 35, 32, 30, 28, 25, 22, 20, 19, 18]
plt.plot(hours, values, marker='o', linewidth=2.5, color='#2E86AB', markersize=8)
plt.fill_between(hours, values, alpha=0.2, color='#2E86AB')
plt.xlabel('Hour of Day', fontsize=12)
plt.ylabel('Average Energy (kWh)', fontsize=12)
plt.title('Energy Consumption by Hour of Day', fontsize=14, fontweight='bold')
plt.grid(True, alpha=0.3)
plt.xticks(range(0, 24))
plt.ylim(0, 50)
plt.tight_layout()
plt.savefig('static/hourly_consumption.png', dpi=100)
plt.close()
print("✅ hourly_consumption.png created")

# 2. Load Type Chart
plt.figure(figsize=(10, 6))
load_types = ['Light Load', 'Medium Load', 'Maximum Load']
values = [13.04, 19.95, 45.31]
colors = ['#FF6B6B', '#4ECDC4', '#45B7D1']
bars = plt.bar(load_types, values, color=colors, edgecolor='black', linewidth=1.5)
plt.xlabel('Load Type', fontsize=12)
plt.ylabel('Average Energy (kWh)', fontsize=12)
plt.title('Energy Consumption by Load Type', fontsize=14, fontweight='bold')
plt.grid(True, alpha=0.3, axis='y')
for bar, val in zip(bars, values):
    plt.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 1.5,
             f'{val:.2f} kWh', ha='center', va='bottom', fontweight='bold')
plt.ylim(0, 55)
plt.tight_layout()
plt.savefig('static/load_type_analysis.png', dpi=100)
plt.close()
print("✅ load_type_analysis.png created")

# 3. Correlation Heatmap
plt.figure(figsize=(10, 8))
# Create sample correlation data
corr_data = np.array([
    [1.00, 0.97, 0.12, 0.85, 0.45],
    [0.97, 1.00, 0.08, 0.82, 0.42],
    [0.12, 0.08, 1.00, 0.15, 0.10],
    [0.85, 0.82, 0.15, 1.00, 0.38],
    [0.45, 0.42, 0.10, 0.38, 1.00]
])
sns.heatmap(corr_data, annot=True, fmt='.2f', cmap='coolwarm', center=0,
            xticklabels=['Usage', 'Reactive', 'PF', 'NSM', 'Hour'],
            yticklabels=['Usage', 'Reactive', 'PF', 'NSM', 'Hour'],
            square=True, linewidths=0.5)
plt.title('Correlation Heatmap', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('static/correlation_heatmap.png', dpi=100)
plt.close()
print("✅ correlation_heatmap.png created")

print("\n All charts created successfully in 'static/' folder!")