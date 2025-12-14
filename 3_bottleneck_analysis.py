import pandas as pd
import numpy as np

df = pd.read_csv('ecommerce_transactions.csv')
df['Timestamp'] = pd.to_datetime(df['Timestamp'])

print("=" * 70)
print("BOTTLENECK ANALYSIS")
print("=" * 70)

slice_ids = df['Network Slice ID'].unique()

print("\n1. LATENCY BOTTLENECK")
print("-" * 70)

latency_ratios = []
for slice_id in slice_ids:
    slice_df = df[df['Network Slice ID'] == slice_id]

    success = slice_df[slice_df['Transaction Success (1/0)'] == 1]
    failure = slice_df[slice_df['Transaction Success (1/0)'] == 0]

    lat_success = success['Latency (ms)'].mean()
    lat_failure = failure['Latency (ms)'].mean()
    ratio = lat_failure / lat_success
    latency_ratios.append(ratio)

    print(f"\n{slice_id}:")
    print(f"  Success Latency: {lat_success:.2f} ms")
    print(f"  Failure Latency: {lat_failure:.2f} ms")
    print(f"  Difference: +{lat_failure - lat_success:.2f} ms")
    print(f"  Ratio: {ratio:.2f}x")

avg_ratio = np.mean(latency_ratios)
print(f"\nAverage Latency Ratio: {avg_ratio:.2f}x")

print("\n\n2. CONGESTION BOTTLENECK")
print("-" * 70)

for slice_id in slice_ids:
    slice_df = df[df['Network Slice ID'] == slice_id]

    print(f"\n{slice_id}:")
    for cong in ['Low', 'Medium', 'High']:
        subset = slice_df[slice_df['Congestion Level'] == cong]
        if len(subset) > 0:
            success_rate = subset['Transaction Success (1/0)'].mean()
            count = len(subset)
            print(f"  {cong}: {success_rate:.2%} ({count} transactions)")

print("\n\n3. CONGESTION DISTRIBUTION")
print("-" * 70)
total = len(df)
for level in ['Low', 'Medium', 'High']:
    count = len(df[df['Congestion Level'] == level])
    pct = (count / total) * 100
    print(f"  {level}: {pct:.1f}% ({count} transactions)")

print("\n" + "=" * 70)