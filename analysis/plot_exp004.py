from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATA_FILE = PROJECT_ROOT / "data" / "exp004_pot_sweep.csv"
OUTPUT_FILE = PROJECT_ROOT / "docs" / "images" / "exp004_pot_sweep_filters.png"


df = pd.read_csv(
    DATA_FILE,
    header=None,
    names=["time_ms", "raw", "voltage"],
)

# Converting the absolute Pico time to experiment-relative(?) seconds.
df["time_s"] = (df["time_ms"] - df["time_ms"].iloc[0]) / 1000.0

#   The moving averages
#
# A moving average replaces each sample with the average of several recent
# samples. Here we use a trailing/causal window, which seems to be appropriate for a
# real-time system because future samples are not available yet
#
# Moving-average filters:
# https://www.dspguide.com/ch15.htm
#
# FIR filters:
# https://www.dspguide.com/ch06.htm

df["ma_5"] = df["voltage"].rolling(window=5).mean()
df["ma_10"] = df["voltage"].rolling(window=10).mean()
df["ma_20"] = df["voltage"].rolling(window=20).mean()


#       The  timing statistics 
#
# Sampling frequency is the reciprocal of sampling period.
#
# A roughly 50 ms sample interval corresponds to roughly:
#
#     1/0.050 s = 20 Hz
#
# Sampling and sampling rate:
# https://www.dspguide.com/ch03.htm

sample_intervals_ms = df["time_ms"].diff().dropna()

mean_interval_ms = sample_intervals_ms.mean()
sample_rate_hz = 1000.0 / mean_interval_ms

sample_intervals_ms = df["time_ms"].diff().dropna()

mean_interval_ms = sample_intervals_ms.mean()
sample_rate_hz = 1000.0 / mean_interval_ms

print("Experiment 004 - Potentiometer Sweep")
print()
print(f"Samples:              {len(df)}")
print(f"Duration:             {df['time_s'].iloc[-1]:.3f} s")
print(f"Mean sample interval: {mean_interval_ms:.3f} ms")
print(f"Minimum interval:     {sample_intervals_ms.min():.0f} ms")
print(f"Maximum interval:     {sample_intervals_ms.max():.0f} ms")
print(f"Sample rate:          {sample_rate_hz:.3f} Hz")
print()
print(f"ADC minimum:          {df['raw'].min()}")
print(f"ADC maximum:          {df['raw'].max()}")
print(f"Voltage minimum:      {df['voltage'].min():.3f} V")
print(f"Voltage maximum:      {df['voltage'].max():.3f} V")


#     The approx. moving-average delay 
#
# An N-point moving average is a simple FIR filter.
#
# Its effective/group delay is approximately:
#
#     (N -1) / 2 samples
#
# Larger windows therefore shouldreduce short-term noise more strongly but also
# make the output respond later to real changes in the input.
#
# Moving-average response:
# https://www.dspguide.com/ch15.htm
#
# Group delay:
# https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.group_delay.html

print()
print("Approximate moving-average delay:")

for window in (5, 10, 20):
    delay_samples = (window - 1) / 2
    delay_ms = delay_samples * mean_interval_ms

    print(
        f"{window:>2}-sample MA: "
        f"{delay_samples:.1f} samples, "
        f"{delay_ms:.1f} ms"
    )


#  The endpoint statistics 
#
# The potentiometer was held near its endpoints during parts of the capture.
# Those approximately constant regions let us examine measurement variation
# without the deliberate motion of the potentiometer dominating the result.
#
# Standard deviation is used here as a simple measure of that spread.
#
# Noise and statistics in DSP:
# https://www.dspguide.com/ch02.htm

low_region = df[df["voltage"] < 0.1]
high_region = df[df["voltage"] > 3.1]

print()
print("Endpoint regions:")

if not low_region.empty:
    print(
        f"Low (<0.1 V):         "
        f"{len(low_region)} samples, "
        f"mean={low_region['voltage'].mean():.3f} V, "
        f"std={low_region['voltage'].std():.4f} V"
    )

if not high_region.empty:
    print(
        f"High (>3.1 V):        "
        f"{len(high_region)} samples, "
        f"mean={high_region['voltage'].mean():.3f} V, "
        f"std={high_region['voltage'].std():.4f} V"
    )

 

plt.figure(figsize=(12, 7))

plt.plot(
    df["time_s"],
    df["voltage"],
    label="Raw",
    linewidth=1,
    alpha=0.65,
)

plt.plot(
    df["time_s"],
    df["ma_5"],
    label="5-sample moving average",
    linewidth=1.5,
)

plt.plot(
    df["time_s"],
    df["ma_10"],
    label="10-sample moving average",
    linewidth=1.5,
)

plt.plot(
    df["time_s"],
    df["ma_20"],
    label="20-sample moving average",
    linewidth=1.5,
)

plt.xlabel("Time (s)")
plt.ylabel("Voltage (V)")
plt.title("Experiment 004 - Dynamic ADC Input and Moving-Average Response")
plt.grid(True, alpha=0.25)
plt.legend()
plt.tight_layout()

plt.savefig(OUTPUT_FILE, dpi=160)
plt.show()

print()
print(f"Saved plot to: {OUTPUT_FILE}")
