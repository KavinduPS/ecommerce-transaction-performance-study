import pandas as pd

df = pd.read_csv('ecommerce_transactions.csv')
df['Timestamp'] = pd.to_datetime(df['Timestamp'])
df = df.sort_values(by='Timestamp').reset_index(drop=True)

print("=" * 70)
print("BASIC PERFORMANCE ANALYSIS")
print("=" * 70)

slice_ids = df['Network Slice ID'].unique()

print("\n1. OVERALL SYSTEM PERFORMANCE")
print("-" * 70)

for slice_id in slice_ids:
    slice_df = df[df['Network Slice ID'] == slice_id]

    success_rate = slice_df['Transaction Success (1/0)'].mean()
    avg_latency = slice_df['Latency (ms)'].mean()
    avg_queue = slice_df['Queue Length (Packets)'].mean()

    requested = slice_df['Requested Bandwidth (Mbps)'].mean()
    allocated = slice_df['Actual Bandwidth Allocated (Mbps)'].mean()
    fulfillment = (allocated / requested) * 100

    print(f"\n{slice_id}:")
    print(f"  Transactions: {len(slice_df)}")
    print(f"  Success Rate: {success_rate:.2%}")
    print(f"  Avg Latency: {avg_latency:.2f} ms")
    print(f"  Avg Queue Length: {avg_queue:.2f} packets")
    print(f"  Bandwidth Fulfillment: {fulfillment:.1f}%")

print("\n" + "=" * 70)