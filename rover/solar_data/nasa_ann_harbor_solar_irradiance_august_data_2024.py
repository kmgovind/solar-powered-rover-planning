import matplotlib.pyplot as plt
import numpy as np 

# Opening file using with, handles closing the file automatically 
with open('nasa_august_solar_CLEAR_SKY_IDLE.csv', 'r') as file: # Passing in the file to read and selecting read mode
    read = file.readlines()

# Data Arrangement 
# YEAR,MO,DY,HR,CLRSKY_SFC_SW_DWN

time = [] # Hours 
ghi_values = []  # Units w/m^2 

for line in read:
    clean_data = line.strip().split(',') # strip() removes the \n character at the end and split() seperate the items by using the commas as seperators 
    if len(clean_data) >= 5:
        time.append((clean_data[3])) # appending time values 
        ghi_values.append(float(clean_data[4])) # Appending index four containg the ghi_values 

plt.figure(figsize=(10,10))
plt.plot(time, ghi_values, marker = 'o')
plt.xlabel("Time: hours)")
plt.ylabel("Solar Irradiance: w/m^2")
plt.title(" Ann Arbor Solar August 2024 Solar Irradiance Data")
plt.grid(True)
plt.show()
print(read)