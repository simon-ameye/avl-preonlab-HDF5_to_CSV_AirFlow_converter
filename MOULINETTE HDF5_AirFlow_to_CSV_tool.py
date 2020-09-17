import h5py as h5
import numpy as np
import glob

#User parameters
auto = 1 #0 if you want to manually select keys and files locations. 1 if you want the code to be automatic.
position_keywords = ["Geometry", "geometry"] #in case of auto run, keywords are used to select velocity and geometry keys based on their names
velocity_keywords = ["Velocity", "velocity"]

#Code
def file_location(auto):
    if auto == 0:
        #File location
        print('Please select the HDF5 file using the dialog window')
        root = tk.Tk();
        root.withdraw();
        return filedialog.askopenfilename()
    else:
        return glob.glob('*.h5')[0]

def key_selection(auto, all_child_keys, position_keywords, velocity_keywords):
    print('Here are the available keys in your file :')
    for i in range(0,len(all_child_keys)):
        print(i, ": ", all_child_keys[i])
    if auto == 0:
        selected_keys = []
        selected_keys.append(all_child_keys[int(input('Enter the number for coordinates key :'))])
        selected_keys.append(all_child_keys[int(input('Enter the number for velocities key :'))])
    else:
        selected_keys = []
        for key in all_child_keys:
            if any(word in key for word in position_keywords):
                selected_keys.append(key)
        for key in all_child_keys:
            if any(word in key for word in velocity_keywords):
                selected_keys.append(key)
    print('Here are the selected keys :')
    for key in selected_keys:
        print(key)
    return selected_keys

def file_destination(auto):
    if auto == 0:
        root = tk.Tk();
        root.withdraw();
        print('Select now the path for file saving')
        file_path =  filedialog.asksaveasfilename(initialdir = "file_path",title = "Select file",filetypes = (("CSV files","*.CSV"),("all files","*.*"))) + ".csv"
    else :
        file_path =  glob.glob('*.h5')[0]
    if not file_path.endswith(('.csv','.xls','.txt','.dat')):
        file_path += '.csv'
    return(file_path)

print('This tool will allow you to open HDF5 files and to create XYZUVW file for PreonLab')
if auto == 0:
    import tkinter as tk
    from tkinter import filedialog

file = h5.File(file_location(auto), 'a')
all_child_keys = []
file.visit(all_child_keys.append)
selected_keys = key_selection(auto, all_child_keys, position_keywords, velocity_keywords)
if np.size(selected_keys) != 2:
    print("ERROR : Number of selected keys is not 2 ! Please check key words used to select keys in your H5 file")

#Concatenate coordinates and speed
try : 
    result = np.concatenate((file[selected_keys[0]],file[selected_keys[1]]),axis=1)
except : 
    print("ERROR : Position and velocity keys won't concatenant ! Please check their size or that their names are expected")

file_path =  file_destination(auto)
print('Writing CSV file... This can take up to 1 hour')
NAMES = np.array(['X','Y','Z','U','V','W']);
np.savetxt(file_path, np.vstack((NAMES, result)), delimiter="," , fmt="%s")
print('Done')
