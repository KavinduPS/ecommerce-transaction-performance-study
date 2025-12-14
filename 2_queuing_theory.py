import pandas as pd

df = pd.read_csv("ecommerce_transactions.csv")
df["Timestamp"] = pd.to_datetime(df["Timestamp"])
df = df.sort_values(by="Timestamp").reset_index(drop=True)

PACKET_SIZE_BITS = 1500 * 8   # 1500 bytes per packet
BITS_IN_MB = 1e6

print("=" * 70)
print("PACKET-LEVEL QUEUING THEORY ANALYSIS (NETWORK LAYER)")
print("=" * 70)

for slice_id in df["Network Slice ID"].unique():

    slice_df = df[df["Network Slice ID"] == slice_id]

    # Arrival Rate (λ) - packets/sec
    avg_traffic_mbps = slice_df["Traffic Volume (Mbps)"].mean()

    arrival_rate = (
        avg_traffic_mbps * BITS_IN_MB
    ) / PACKET_SIZE_BITS   # packets/sec

    avg_allocated_bw = slice_df["Actual Bandwidth Allocated (Mbps)"].mean()

    service_rate = (
        avg_allocated_bw * BITS_IN_MB
    ) / PACKET_SIZE_BITS   # packets/sec

    rho = arrival_rate / service_rate

    # Latency (W) in seconds
    W = slice_df["Latency (ms)"].mean() / 1000  # seconds

    # Little’s Law: L = λW
    L_theoretical = arrival_rate * W
    L_observed = slice_df["Queue Length (Packets)"].mean()

    print(f"\n{slice_id}")
    print("-" * 50)

    print(f"Arrival Rate (λ): {arrival_rate:.2f} packets/sec")
    print(f"Service Rate (μ): {service_rate:.2f} packets/sec")
    print(f"Traffic Intensity (ρ): {rho:.3f}")

    if rho >= 1:
        print("→ UNSTABLE SYSTEM (λ ≥ μ)")
    elif rho > 0.8:
        print("→ High utilization (risk of congestion)")
    else:
        print("→ Stable system")

    print("\nLittle’s Law Validation:")
    print(f"  Theoretical Queue Length (L = λW): {L_theoretical:.2f} packets")
    print(f"  Observed Queue Length:             {L_observed:.2f} packets")
    print(f"  Absolute Difference:               {abs(L_theoretical - L_observed):.2f}")

print("\n" + "=" * 70)
