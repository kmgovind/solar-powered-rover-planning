import numpy as np
import matplotlib.pyplot as plt

# Time (seconds)
time = [30, 60, 90, 120, 150, 180, 210, 240, 270, 300, 330, 360, 390, 420]

# Voltage datasets k = 8 N = 2 
array_1 = [12.40, 12.34, 12.29, 12.20, 12.13, 12.02, 11.92, 11.79, 11.66, 11.54]
array_2 = [12.43, 12.35, 12.25, 12.15, 12.00, 11.84, 11.66, 11.44]
array_3 = [12.31, 12.26, 12.20, 12.10, 11.99, 11.86, 11.73, 11.59, 11.44, 11.27]

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
plt.title('Energy vs Time with slopes and average slope line')
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()
