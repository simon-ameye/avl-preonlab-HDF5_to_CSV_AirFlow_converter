import h5py as h5
import numpy as np
import tkinter as tk
from tkinter import filedialog
root = tk.Tk();
root.withdraw();

print('This tool will allow you to open HDF files and to create XYZUVW file for PreonLab')

#File location
print('Please select the HDF5 file using the dialog window')
file_path = filedialog.askopenfilename();
file = h5.File(file_path, 'a');

#HDF5 file explorator. Please use the explorator to
#- select the right nodes coordinates file
#- select the right velocity file

all_child_keys = []
file.visit(all_child_keys.append)
all_child_keys_num = range(0,len(all_child_keys))

print('Here are the available keys in your file :')
for i in range(0,len(all_child_keys)):
    print(i, ": ", all_child_keys[i])

coordinates_num = int(input('Enter the number for coordinates key :'))  
coordinates_name = all_child_keys[coordinates_num]
velocities_num = int(input('Enter the number for velocities key :'))  
velocities_name = all_child_keys[velocities_num]
#Coordinates and velocity files names
node_coord = file[coordinates_name]
velocity = file[velocities_name]

#Concatenate coordinates and speed
result = np.concatenate((node_coord,velocity),axis=1)

#The result file will be size_ratio times smaller
size_ratio = int(input('Do you want to reduce dataset size ? Enter 1 to keep all data. Larger value will divide dataset size by the value :'))

root = tk.Tk();
root.withdraw();
print('Select now the path for file saving')
file_path =  filedialog.asksaveasfilename(initialdir = "file_path",title = "Select file",filetypes = (("CSV files","*.CSV"),("all files","*.*")))

print('Writing CSV file... This can take up to 1 hour')
#   Writing the smaller result file """

result_size = np.size(result,0)
result_small = result[np.arange(0,result_size,size_ratio) ,  :]
NAMES = np.array(['X','Y','Z','U','V','W']);
result_small = np.vstack((NAMES,result_small))

np.savetxt(file_path, result_small, delimiter="," , fmt="%s")
print('Done')