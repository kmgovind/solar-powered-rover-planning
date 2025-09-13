import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
from numpy import trapz
from scipy.integrate import cumtrapz 


# Time interval  
time = [0, 300, 600, 900, 1200, 1500, 1800, 2100, 2400] 

# Dataset 1 
voltage_1 = [12.54, 12.47, 12.38, 12.27, 12.15, 12.00, 11.84, 11.72, 11.45]


# Dataset 2 
voltage_2 = [12.53, 12.44, 12.33, 12.21, 12.07, 11.92, 11.73, 11.52, 11.32]


# Dataset 3 
voltage_3 = [12.53, 12.46, 12.39, 12.28, 12.14, 12.0, 11.85, 11.56, 11.35]


# Dataset 4 
voltage_4 = [12.5, 12.4, 12.3, 12.2 , 12.1 , 12.0, 11.8, 11.6, 11.4]


# Constants 
idle_amps_drawn = 4.18 # Units amps (Estimated guess obtained from the electronics onboard)


# Interpolate voltages

voltages = [voltage_1, voltage_2, voltage_3, voltage_4]


def interpolate_voltages(voltages, time):

    interpolated_time = np.linspace(min(time), max(time), num = 100) # Making time smooth and continous

    interpolated_voltages = []

    for i in range(len(voltages)):

        interpolated_voltage = interp1d(time, voltages[i], kind = 'linear')

        voltage_values = interpolated_voltage(interpolated_time)

        interpolated_voltages.append(voltage_values) # Storing each interpolated voltage in the array 

    return interpolated_voltages, interpolated_time

interpolated_voltages, interpolated_time = interpolate_voltages(voltages, time) # Returns an array of interpolated voltages and the interpolated time 

# Plotting interpolated voltages 
# for i in range(len(interpolated_voltages)):
#     plt.plot(interpolated_time, interpolated_voltages[i])


# Using P = V X I We can multiply the entire interpolated voltages vector by amps to get the power vector 
def convert_to_power(interpolated_voltages, amps: float):
    power_array = []
    for i in range(len(interpolated_voltages)):
        power_vectors = interpolated_voltages[i] * amps
        power_array.append(power_vectors)
    return power_array

power = convert_to_power(interpolated_voltages, idle_amps_drawn) # Extracting power power array composed of power vectors 


# for i in range(len(interpolated_voltages)):
#     plt.plot(interpolated_time, power[i], label = f"Dataset {i+1}")
#     plt.legend()
    
# Converting those power values into Energy values by integrating them over that period in time 

# def convert_power_energy(power_vectors):
#     energy_vectors = [] # An array composed of Energy Vectors 
#     for i in range(len(power)):
#         energy_vector = cumtrapz(power[i], interpolated_time) # initial = 0 makes the input and output the same length 
#         energy_vectors.append(energy_vector)
#     return energy_vectors

# energy_vectors = convert_power_energy(power)


energy_curves = []

for p_vec in power:
    cumulative_energy = []
    for i in range(1, len(interpolated_time) + 1):
        energy = np.trapz(p_vec[:i], interpolated_time[:i])
        cumulative_energy.append(energy)
    energy_curves.append(cumulative_energy)


# Plotting energy curves 
for i in range(len(energy_curves)):
    plt.plot(interpolated_time, energy_curves[i], label = f"Dataset {i+1}")
    plt.legend()
    

def average_wattage_all_datasets(power_array): # Averaging the wattage of all the functions by integrating them over time 

    average_watts_for_each_dataset = []

    value = 0

    # Getting the average of the power arrays and storing them in the wattage_values array 
    for i in range(len(power_array)):

        watt_avg_for_i_dataset = np.mean(power_array[i])

        average_watts_for_each_dataset.append(watt_avg_for_i_dataset)

    for i in range(len(average_watts_for_each_dataset)):
        value += average_watts_for_each_dataset[i] # Summing all the values in the array 
    return value / len(average_watts_for_each_dataset) # Returning the average 

average_watts = average_wattage_all_datasets(power) # Passing in power which is an array containing power vectros 

print(average_watts)


plt.grid(True)

plt.xlabel("Time: Seconds")

plt.ylabel("Energy: J")

plt.title("Energy Vs Time: V = 0")

plt.show()

