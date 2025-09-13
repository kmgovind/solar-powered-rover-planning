import numpy as np 
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d # Importing the scipy interpolation for 1D function 


time = np.array([0, 30, 60, 90, 120, 150, 180, 210,240, 270, 300, 330, 360, 390, 420, 450, 480, 510, 540, 570, 600])

voltage_1 = np.array([12.38, 12.34, 12.30, 12.23, 12.17, 12.08, 12.00, 11.91, 11.81, 11.70, 11.58, 11.45, 11.27, 11.12, 11.02, 10.94, 10.87, 10.80, 10.73, 10.63 , 10.51])
voltages = [voltage_1]

# Approximate Amps of the system (Constraints)

idle_amps_drawn = 4.18 # Approximation

approximate_amps_from_motors = 7 # Estimate of the motor's current draw 

total_amps_drawn = approximate_amps_from_motors + idle_amps_drawn # Total amps drawn during the experiment 


# Interpolating the voltage 
def interpolate_voltages(voltages, time):

    interpolated_time = np.linspace(min(time), max(time), num = 100) # Making time smooth and continous

    interpolated_voltages = []

    for i in range(len(voltages)):

        interpolated_voltage = interp1d(time, voltages[i], kind = 'linear')

        voltage_values = interpolated_voltage(interpolated_time)

        interpolated_voltages.append(voltage_values) # Storing each interpolated voltage in the array 

    return interpolated_voltages, interpolated_time

interpolated_voltages, interpolated_time = interpolate_voltages(voltages, time) # Returns an array of interpolated voltages and the interpolated time 



# Using P = V X I We can multiply the entire interpolated voltages vector by amps to get the power vector 
def convert_to_power(interpolated_voltages, amps: float):
    power_array = []
    for i in range(len(interpolated_voltages)):
        power_vectors = interpolated_voltages[i] * total_amps_drawn
        power_array.append(power_vectors)
    return power_array

power = convert_to_power(interpolated_voltages, idle_amps_drawn) # Extracting power power array composed of power vectors 


energy_curves = []

for p_vec in power:
    cumulative_energy = []
    for i in range(1, len(interpolated_time) + 1):
        energy = np.trapz(p_vec[:i], interpolated_time[:i])
        cumulative_energy.append(energy)
    energy_curves.append(cumulative_energy)

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

print(average_wattage_all_datasets(power))



plt.grid(True)

plt.xlabel("Time: Second")

plt.ylabel("Energy: J")

plt.title("Energy Vs Time: Idle Rover Discharge")

plt.show()


# def voltage_to_power(data):
#     power = [] # An array containing power vectors 
#     for voltage_value in data:
#         values = voltage_value * total_amps_drawn # P = V X I
#         power.append(values) # Appending the values to the power array 
#     return power

# power = voltage_to_power(voltages) # Power array    [array1]

# def average_power_of_all_datasets(power):
#    average_watts_of_each_dataset = []
#    average_of_each = 0
#    vals = 0
   
#    for i in range(len(power)):
#        average_of_each += np.mean(power[i]) # Getting the average from each power vector and summing them to values 
#        average_watts_of_each_dataset.append(average_of_each) # Appending each of these values to an array

#    for i in range(len(average_watts_of_each_dataset)):
#         vals += average_watts_of_each_dataset[i] 
#    return vals/ len(average_watts_of_each_dataset) 

# avg_watts = average_power_of_all_datasets(power)

# print(average_power_of_all_datasets(power))

# def get_energy_from_watts(power, time):
#     pass



# total_energy = np.trapz(time, power) # Integrating power vs time to get total Energy 

# average_watts = average_power(power)

# print(average_watts)

# plt.figure(figsize=(10,10))
# # plt.plot(time, power, marker = 'o', label = f'Discharge Rate: {average_watts: .2f} J/s') 
# plt.xlabel("Time: Seconds")
# plt.ylabel("Energy: J/S")
# plt.title("Energy vs Time: Robot Discharge")
# plt.grid(True)
# plt.legend()
# plt.tight_layout()
# plt.show()