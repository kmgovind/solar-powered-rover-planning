import numpy as np

import matplotlib.pyplot as plt

# Data Arrangement
# YEAR,MO,DY,HR,CLRSKY_SFC_SW_DWN

with open('nasa_ClearSkyData_Solar_Irradiance_One_day_August.csv', 'r') as file: # Close the file after we're done reading 
    read = file.readlines() # Read line by line 

time = [] # Hours

gih_values = [] # w/m^2

for line in read: # For loop 
    clean_data = line.strip().split(',') # Strip the newline, seperate the items using the commas and extract
    # clean_data = [item,item, ....]
    if len(clean_data) >= 5: # If the length of the daya is greater than 4
        time.append(clean_data[3]) # Extracting the time
        gih_values.append(float(clean_data[4])) # Extracting gih_values 

plt.figure(figsize=(10,10)) # Figure size of the GUI 

plt.plot(time, gih_values, marker = 'o')

plt.xlabel("Time: Hours")

plt.ylabel("Solar Irradiance: w/m^2")

plt.title("Ann Arbor Solar Irradiance Data 2024 One Day Idle Condition (Clear Skies)")

plt.grid(True)

plt.show()

print(read)





