import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_style("whitegrid")

df = pd.read_csv('ecommerce_transactions.csv')
df['Timestamp'] = pd.to_datetime(df['Timestamp'])

slice_ids = df['Network Slice ID'].unique()

print("Generating visualizations...")

fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('Network Slice Performance Analysis', fontsize=16, fontweight='bold')

# Chart 1: Success Rate by Slice
ax1 = axes[0, 0]
success_rates = [df[df['Network Slice ID'] == s]['Transaction Success (1/0)'].mean() * 100
                 for s in slice_ids]
bars = ax1.bar(slice_ids, success_rates, color=['#ff6b6b', '#4ecdc4', '#45b7d1'], alpha=0.7)
ax1.set_ylabel('Success Rate (%)')
ax1.set_title('Success Rate by Network Slice', fontweight='bold')
ax1.axhline(y=50, color='red', linestyle='--', alpha=0.5)
for bar, rate in zip(bars, success_rates):
    ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 2,
             f'{rate:.1f}%', ha='center', fontweight='bold')

# Chart 2: Latency Comparison
ax2 = axes[0, 1]
x = np.arange(len(slice_ids))
width = 0.35

success_lat = []
failure_lat = []
for sid in slice_ids:
    slice_df = df[df['Network Slice ID'] == sid]
    success = slice_df[slice_df['Transaction Success (1/0)'] == 1]
    failure = slice_df[slice_df['Transaction Success (1/0)'] == 0]
    success_lat.append(success['Latency (ms)'].mean())
    failure_lat.append(failure['Latency (ms)'].mean())

ax2.bar(x - width/2, success_lat, width, label='Success', color='#2ecc71', alpha=0.8)
ax2.bar(x + width/2, failure_lat, width, label='Failure', color='#e74c3c', alpha=0.8)
ax2.set_ylabel('Latency (ms)')
ax2.set_title('Latency: Success vs Failure', fontweight='bold')
ax2.set_xticks(x)
ax2.set_xticklabels(slice_ids)
ax2.legend()

# Chart 3: Congestion Impact
ax3 = axes[1, 0]
cong_order = ['Low', 'Medium', 'High']
x_pos = np.arange(len(cong_order))

for sid in slice_ids:
    slice_df = df[df['Network Slice ID'] == sid]
    rates = []
    for level in cong_order:
        subset = slice_df[slice_df['Congestion Level'] == level]
        rates.append(subset['Transaction Success (1/0)'].mean() * 100)
    ax3.plot(x_pos, rates, marker='o', linewidth=2, markersize=8, label=sid)

ax3.set_xlabel('Congestion Level')
ax3.set_ylabel('Success Rate (%)')
ax3.set_title('Impact of Congestion on Success', fontweight='bold')
ax3.set_xticks(x_pos)
ax3.set_xticklabels(cong_order)
ax3.axhline(y=0, color='red', linestyle='--', alpha=0.7)
ax3.legend()
ax3.grid(True, alpha=0.3)

# Chart 4: Queue Length Distribution
ax4 = axes[1, 1]
queue_data = [df[df['Network Slice ID'] == s]['Queue Length (Packets)'] for s in slice_ids]
bp = ax4.boxplot(queue_data, tick_labels=slice_ids, patch_artist=True)
for patch in bp['boxes']:
    patch.set_facecolor('lightblue')
    patch.set_alpha(0.7)

ax4.set_ylabel('Queue Length (Packets)')
ax4.set_title('Queue Length Distribution', fontweight='bold')

plt.tight_layout()
plt.savefig('performance_analysis.png', dpi=300, bbox_inches='tight')
print("✓ Saved: performance_analysis.png")

# Chart 5: Congestion Distribution
fig2, ax = plt.subplots(figsize=(8, 6))
total = len(df)
levels = ['Low', 'Medium', 'High']
counts = [len(df[df['Congestion Level'] == l]) for l in levels]
percentages = [(c/total)*100 for c in counts]

colors = ['#2ecc71', '#f39c12', '#e74c3c']
bars = ax.bar(levels, percentages, color=colors, alpha=0.7)
ax.set_ylabel('Percentage (%)')
ax.set_title('Congestion Level Distribution', fontsize=14, fontweight='bold')

for bar, pct, count in zip(bars, percentages, counts):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
            f'{pct:.1f}%\n({count})', ha='center', fontweight='bold')

plt.tight_layout()
plt.savefig('congestion_distribution.png', dpi=300, bbox_inches='tight')
print("✓ Saved: congestion_distribution.png")

plt.show()

# Traffic Intensity Chart
fig, ax = plt.subplots(figsize=(10, 6))

slices = ['Slice-1', 'Slice-2', 'Slice-3']
rho_values = [0.962, 0.962, 0.962]
colors = ['#e74c3c', '#e74c3c', '#e74c3c']

bars = ax.bar(slices, rho_values, color=colors, alpha=0.7, edgecolor='black', linewidth=2)

# Add threshold lines
ax.axhline(y=0.8, color='orange', linestyle='--', linewidth=2,
           label='High Load Threshold (ρ=0.8)', alpha=0.7)
ax.axhline(y=1.0, color='darkred', linestyle='--', linewidth=2,
           label='Unstable (ρ=1.0)', alpha=0.7)

ax.set_ylabel('Traffic Intensity (ρ)', fontsize=12, fontweight='bold')
ax.set_title('Network Capacity Utilization - Critical Load', fontsize=14, fontweight='bold')
ax.set_ylim(0, 1.1)
ax.legend(fontsize=10)
ax.grid(axis='y', alpha=0.3)

# Add percentage labels
for bar, rho in zip(bars, rho_values):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.02,
            f'{rho:.3f}\n(96.2%)', ha='center', fontweight='bold', fontsize=11)

# Add warning zone
ax.axhspan(0.8, 1.0, alpha=0.1, color='red', label='Danger Zone')

plt.tight_layout()
plt.savefig('traffic_intensity.png', dpi=300, bbox_inches='tight')
print("✓ Saved: traffic_intensity.png")
plt.show()

print("\nAll visualizations generated successfully!")
print("="*70)