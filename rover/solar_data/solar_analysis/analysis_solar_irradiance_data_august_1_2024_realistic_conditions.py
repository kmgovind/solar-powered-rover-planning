import matplotlib.pyplot as plt 
import numpy as np 
from scipy.interpolate import interp1d # Importing interpolation function 
from numpy import trapz # Importing trapezodial integration 

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

def calculate_avg(data):
    # Iterating over the array values and taking the average
    if not data: 
        return 0 # Prevent's division by zero 
    total = 0 # Initializing total 
    average = 0 #Initializing average 
    for value in data:
        total += value # Summing the values 
        average = total /len(data)
    return average

# Data Calculations 
avg = float(calculate_avg(gih_values)) # Calculating the average w/m^2 over a 24 hour period 

# Integrating the total Energy over a 0-24 hour interval
# ENERGY = trapz(gih_values, time) * 3600 # getting J/m^2


plt.figure(figsize=(10,10)) # Figure size of the pop up GUI
plt.plot(time, gih_values, marker = 'o', label = f"Average Solar Irradiance:{avg: .4f}  w/m^2" ) # Average w/m^2
plt.legend(loc='upper right')  # places legend Upper right of the plot 
plt.xlabel("Time: Hours")
plt.ylabel("Solar Irradiance: w/m^2")
plt.title("Ann Arbor Solar Irradiance Data for August 1st 2024 Realistic Conditions (not Ideal)")
plt.grid(True)
plt.show()
print(float(calculate_avg(gih_values)))


