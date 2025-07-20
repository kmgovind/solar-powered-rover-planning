import numpy as np 
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d # Importing the scipy interpolation for 1D function 


time = np.array([0, 30, 60, 90, 120, 150, 180, 210,240, 270, 300, 330, 360, 390, 420, 450, 480, 510, 540, 570, 600])

voltages = np.array([12.38, 12.34, 12.30, 12.23, 12.17, 12.08, 12.00, 11.91, 11.81, 11.70, 11.58, 11.45, 11.27, 11.12, 11.02, 10.94, 10.87, 10.80, 10.73, 10.63 , 10.51])



interpolated_voltage = interp1d(voltages, time, 'linear')

# Upper Bound 
# Allowing the rover to discharge going full-throthle at some nearly constant velocity

# Approximate Amps of the system

idle_amps_drawn = 4.18 # Gathered from voltage data

approximate_amps_from_motors = 7 # Estimate of the motor's current draw 

total_amps_drawn = approximate_amps_from_motors + idle_amps_drawn # Total amps draw during the experiment 


def voltage_to_power(data):
    power = []
    for voltage_value in data:
        values = voltage_value * total_amps_drawn # P = V X I
        power.append(values) # Appending the values to the power array 
    return power

power = voltage_to_power(voltages) 

def average_power(power):
    sum = 0
    average_wattage = 0
    for power_values in power:
        sum += power_values
        average_wattage = sum/len(power)
    return average_wattage




total_energy = np.trapz(time, power) # Integrating power vs time to get total Energy 

average_watts = average_power(power)

# print(average_watts)

plt.figure(figsize=(10,10))
plt.plot(time, power, marker = 'o', label = f'Discharge Rate: {average_watts: .2f} J/s') 
plt.xlabel("Time: Seconds")
plt.ylabel("Energy: J/S")
plt.title("Energy vs Time: Robot Discharge")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()