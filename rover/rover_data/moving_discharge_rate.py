import numpy as np
import matplotlib.pyplot as plt

# Time interval arrays (in minutes)
time_3min = np.array([0, 3, 6, 9, 12, 15])
time_2min = np.array([0, 2, 4, 6, 8, 10, 12])

# Voltage data
data_1 = np.array([12.46, 12.34, 12.17, 11.96, 11.69, 11.32])       # 3 min intervals
data_2 = np.array([12.10, 12.00, 11.85, 11.65])                     # 2 min intervals (4 points)
data_3 = np.array([12.41, 12.31, 12.18, 12.01, 11.80, 11.54, 11.26]) # 2 min intervals
data_4 = np.array([12.44, 12.34, 12.20, 12.04, 11.85, 11.62, 11.34]) # 2 min intervals
data_5 = np.array([12.19, 12.12, 11.97, 11.77, 11.52])               # 2 min intervals

datasets = [data_1, data_2, data_3, data_4, data_5]

# Voltage → SOC (%) mapping and battery capacity (Wh)
voltage_soc_map = {12.6: 100, 11.85: 75, 11.55: 50, 11.1: 25, 9.0: 0}
E_max = 57.72  # Wh (given)

def voltage_to_wh(voltage):
    vs = np.array(list(voltage_soc_map.keys()))
    soc = np.array(list(voltage_soc_map.values()))
    # Interpolate SOC based on voltage, sorting keys in ascending order for interp
    soc_interp = np.interp(voltage, vs[::-1], soc[::-1])
    return soc_interp / 100 * E_max

# Prepare plot
plt.figure(figsize=(10,6))

# To accumulate slopes for averaging
slopes = []

# Plot each dataset separately and compute slopes
for i, data in enumerate(datasets):
    # Select proper time vector based on dataset index
    t_min = time_3min if i == 0 else time_2min
    t = t_min[:len(data)]
    
    # Convert voltage to energy (Wh), then to Joules
    energy_wh = voltage_to_wh(data)
    energy_j = energy_wh * 3600  # convert Wh to Joules
    
    # Convert time to seconds
    t_sec = t * 60
    
    # Plot raw data points
    plt.plot(t_sec, energy_j, 'o-', label=f'Dataset {i+1}')
    
    # Calculate slope (energy decrease rate) using linear fit
    # slope in Joules per second (negative value)
    coeffs = np.polyfit(t_sec, energy_j, 1)  # coeffs[0] is slope
    slope = coeffs[0]
    slopes.append(slope)
    
    print(f"Dataset {i+1} slope (J/s): {slope:.4f}")

# Compute average slope
avg_slope = np.mean(slopes)
print(f"\nAverage slope (J/s): {avg_slope:.4f}")

# Plot average slope line from start to end time of combined data
all_times = []
all_energies = []
for i, data in enumerate(datasets):
    t_min = time_3min if i == 0 else time_2min
    t = t_min[:len(data)]
    all_times.extend(t)
    energy_wh = voltage_to_wh(data)
    energy_j = energy_wh * 3600
    all_energies.extend(energy_j)

all_times_sec = np.array(all_times) * 60
all_energies = np.array(all_energies)

t_line = np.array([all_times_sec.min(), all_times_sec.max()])
# line = E0 + slope * t, where E0 is initial energy at t=all_times_sec.min()
E0 = all_energies[all_times_sec.argmin()]
avg_line = E0 + avg_slope * (t_line - t_line[0])

plt.plot(t_line, avg_line, 'k--', linewidth=2, label='Average slope line')

plt.xlabel('Time: Seconds')
plt.ylabel('Energy: J')
plt.title('Energy vs Time')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
