import matplotlib.pyplot as plt 
import numpy as np 
from scipy.interpolate import interp1d # Importing interpolation function 
from numpy import trapz # Importing trapezodial integration 

# Using 

with open("nasa_solar_irridiance_data_08_08_2024_realistic_conditions.csv") as file:
    read = file.readlines() # Read each line of the file

# Data Arrangment 
# YEAR,MO,DY,HR,ALLSKY_SFC_SW_DWN
time = [] # In hours 

gih_values = [] # Solar Irradiance Data: Units w/m^2 


for line in read: # Grabbing the index and item associated with the read object 
    clean_data = line.strip().split(',') # Seperate the items in an array by the commas and remove the \n 
    if len(clean_data) >= 5: # Check the length of the array passed in 
        time.append(float(clean_data[3])) # Appending the time 
        gih_values.append(float(clean_data[4])) # Appending the gih values to the array 

def calculate_avg(data): # The average value is nice to have but does not amount to having the area under the curve from an integral
    # Iterating over the array values and taking the average
    if not data: 
        return 0 # Prevent's division by zero 
    total = 0 # Initializing total 
    average = 0 #Initializing average 
    for value in data:
        total += value # Summing the values 
        average = total /len(data)
    return average


# Solar Panel Simulation 

SURFACE_AREA_PANNELS = 0.549918

EFFICENCY = 0.195 # Average 19.5 Percent Solar Cell Efficency 

MPPT_EFFICENCY = 0.98 # MPPT Efficency for our particular solar charge controller 

time_hours = np.array(time)

irradiance = np.array(gih_values)

p_in = (SURFACE_AREA_PANNELS * irradiance * EFFICENCY) * MPPT_EFFICENCY # Power into the system 


# Constraints 
E_MAX = 57.72 # Maximum Watt-hours: it's full charge E(0)

P_OUT = 128.75  # Unit w, what we're trting to minimize 


index_of_max = np.argmax(irradiance) # Findining peak irradiance indexes in the data 

# Utilizng peak indexes to to find the times at which the power_in is at it's peak

t_peak = time_hours[index_of_max:] # Getting peak times using peak indexes 

p_in_peak = p_in[index_of_max:] #Getting the power_in at the peak indexes 


dt_peak = np.diff(t_peak, prepend=t_peak[0]) # Calculating the difference between the time values 


E_peak = np.zeros_like(t_peak) # Intitalaizing n energy array considering only peak sunlight hours 


E_peak[0] = E_MAX

def state_of_charge(): # Simulating from peak sunlight until it is empty 
    depletion_time = None # Unkown 
    # Calculating the dt's from each point  
    for i in range(1, len(t_peak)): # Loop starting from one so we can find the difference between a previous and next time step
        delta_E = (p_in_peak[i-1] - P_OUT) * dt_peak[i] # Calulating the difference in energy at every time step
        E_peak[i] = np.clip(E_peak[i-1]+ delta_E, 0 ,E_MAX)

        if E_peak[i] == 0 and depletion_time is None:
            fraction = E_peak[i-1] / (P_OUT - p_in_peak[i-1])
            depletion_time = t_peak[i-1] + fraction
            print(f"Battery depletes: {depletion_time - t_peak[0]: .3f} h after peak")
    SoC = (E_peak/E_MAX) * 100
    return SoC



SoC = state_of_charge()

# Interpolating results 
interpolated_state_of_charge = interp1d(t_peak, SoC, kind = 'linear')
t_fine = np.linspace(t_peak[0], t_peak[-1], 100)
SoC_fine = interpolated_state_of_charge(t_fine)

# Plotting the battery 
plt.figure(figsize=(10,10))
plt.plot(t_fine, SoC_fine , marker = 'x')
plt.xlabel("Time (hours)")
plt.ylabel("Battery State of Charge (%)")
plt.title("Battery SoC over Time")
plt.grid(True)
plt.show()

# PLotting the power into the system 
plt.plot(time_hours, p_in, label='Input Power (W)')
plt.xlabel("Time (hours)")
plt.ylabel("Power (W)")
plt.title("Instantaneous Power Input from Solar Panel")
plt.grid(True)
plt.legend()
plt.show()

