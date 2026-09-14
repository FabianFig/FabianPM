from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_FILE = PROJECT_ROOT / "data" / "adc_capture.csv"

MOVING_AVERAGE_WINDOW = 5


def main():
    df = pd.read_csv(
        DATA_FILE,
        header=None,
        names=["time_ms", "raw_adc", "voltage_v"],
    )

    # start elapsed time at zeros
    df["time_s"] = (
        df["time_ms"] - df["time_ms"].iloc[0]
    ) / 1000.0

    intervals_ms = df["time_ms"].diff().dropna()

    # averageing each sample with the four measurements before it.
    df["voltage_filtered_v"] = (
        df["voltage_v"]
        .rolling(window=MOVING_AVERAGE_WINDOW)
        .mean()
    )

    print(f"Samples: {len(df)}")
    print(f"Duration: {df['time_s'].iloc[-1]:.3f} s")
    print(f"Mean sample interval: {intervals_ms.mean():.3f} ms")
    print(f"Mean sample rate: {1000.0 / intervals_ms.mean():.2f} Hz")

    print()
    print("ADC")
    print(f"  Mean: {df['raw_adc'].mean():.2f} counts")
    print(f"  Std dev: {df['raw_adc'].std():.2f} counts")
    print(f"  Min: {df['raw_adc'].min()} counts")
    print(f"  Max: {df['raw_adc'].max()} counts")

    print()
    print("Voltage")
    print(f"  Mean: {df['voltage_v'].mean():.4f} V")
    print(f"  Std dev: {df['voltage_v'].std():.4f} V")
    print(f"  Min: {df['voltage_v'].min():.3f} V")
    print(f"  Max: {df['voltage_v'].max():.3f} V")

    print()
    print("Filtered voltage")
    print(f"  Std dev: {df['voltage_filtered_v'].std():.4f} V")

    plt.figure(figsize=(10, 5))

    plt.plot(
        df["time_s"],
        df["voltage_v"],
        linewidth=0.8,
        label="Raw",
    )

    plt.plot(
        df["time_s"],
        df["voltage_filtered_v"],
        linewidth=2,
        label=f"{MOVING_AVERAGE_WINDOW}-sample moving average",
    )

    plt.xlabel("Time (s)")
    plt.ylabel("Voltage (V)")
    plt.title("FabianPM - Pico ADC capture")
    plt.grid(alpha=0.25)
    plt.legend()

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
