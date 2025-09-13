import numpy as np
import matplotlib.pyplot as plt

# Time array in seconds (30s intervals)
time = [30 * i for i in range(1, 15)]  # 30, 60, ..., 420 seconds

# Voltage data for N=1.3, K=2
array_1 = [12.13, 12.10, 12.06, 12.01, 11.94, 11.88, 11.80, 11.71, 11.62, 11.53, 11.40]
array_2 = [12.32, 12.28, 12.17, 12.11, 12.04, 11.96, 11.87, 11.78, 11.67, 11.56, 11.43, 11.34]
array_3 = [12.38, 12.35, 12.31, 12.26, 12.21, 12.14, 12.07, 11.19, 11.90, 11.80, 11.70, 11.60, 11.49, 11.37]

data = [array_1, array_2, array_3]
labels = ['data1', 'data2', 'data3']

# Voltage to SOC (%) mapping (linear approx)
voltage_soc_map = {
    12.6: 100,
    11.85: 75,
    11.55: 50,
    11.1: 25,
    9.0: 0
}

E_max = 57.72  # Maximum energy in Wh

def voltage_to_wh(voltage):
    voltages = np.array(list(voltage_soc_map.keys()))
    soc_percent = np.array(list(voltage_soc_map.values()))
    soc_interp = np.interp(voltage, voltages[::-1], soc_percent[::-1])
    return soc_interp / 100 * E_max

plt.figure(figsize=(10,6))

slopes = []

for i, dataset in enumerate(data):
    t_array = np.array(time[:len(dataset)])
    v_array = np.array(dataset)
    
    # Convert voltage to energy in Wh then to Joules
    energy_wh = voltage_to_wh(v_array)
    energy_j = energy_wh * 3600  # Wh to Joules
    
    # Plot energy vs time
    plt.plot(t_array, energy_j, 'o-', label=labels[i])
    
    # Linear fit to get slope (J/s)
    coeffs = np.polyfit(t_array, energy_j, 1)
    slope = coeffs[0]
    slopes.append(slope)
    print(f"Slope (J/s) for {labels[i]}: {slope:.4f}")

# Average slope
avg_slope = np.mean(slopes)
print(f"\nAverage slope (J/s) across all datasets: {avg_slope:.4f}")

# Plot average slope line
t_line = np.array([min(time), max(time)])
# Starting energy for average slope line: use mean of first energies
start_energies = [voltage_to_wh(np.array(d))[0] * 3600 for d in data]
E0 = np.mean(start_energies)
avg_line = E0 + avg_slope * (t_line - t_line[0])

plt.plot(t_line, avg_line, 'k--', linewidth=2, label='Average slope line')

plt.xlabel('Time (seconds)')
plt.ylabel('Energy (Joules)')
plt.title('Energy vs Time with slopes and average slope line (N=1.3, K=2)')
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()
