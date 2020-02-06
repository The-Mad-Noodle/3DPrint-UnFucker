'''
-----------------------------------------------------------------------------------------
   _____ ____     ____       _       __     __  __      ______           __
  |__  // __ \   / __ \_____(_)___  / /_   / / / /___  / ____/_  _______/ /_____  _____
   /_ </ / / /  / /_/ / ___/ / __ \/ __/  / / / / __ \/ /_  / / / / ___/ //_/ _ \/ ___/
 ___/ / /_/ /  / ____/ /  / / / / / /_   / /_/ / / / / __/ / /_/ / /__/ ,< /  __/ /
/____/_____/  /_/   /_/  /_/_/ /_/\__/   \____/_/ /_/_/    \__,_/\___/_/|_|\___/_/
                                                        by The Mad Noodle v.0.0.5
-----------------------------------------------------------------------------------------
The Failed 3D print recovery gcode processor.
Find the line number of the point where your 3D print failed
and the UnFucker will modify the gcode to start at the correct point

By The Mad Noodle
02/05/2020
v0.0.5
'''

import os
from tkinter import *
from tkinter.ttk import *
from tkinter import filedialog
from tkinter import messagebox as mb
import configparser


# == Configuration Setup ==============================================================

configFile = 'config.ini'
config = configparser.ConfigParser()
config.read(configFile)

start_z_move = config.get('settings', 'start_z_move')
recovered_suffix = config.get('settings', 'recovered_file_suffix')
default_open_dir = config.get('settings', 'default_open_dir')

# == Functions ========================================================================
def fix_gcode():

    try:
        recovery_filename = source_text.get()
        line_number = int(line_field.get())
        Z_height = float(z_field.get())
        print_temp = temp_field.get()

        Z_height_offset = float(Z_height) + float(start_z_move)


        if recovery_filename[-6:] != '.gcode':
            mb.showerror("Wrong File Format", "Incorrect file format!\n"
                                              "Please select a .gcode file and try again.")
            recovery_filename = ''
            source_text.delete(0, END)
            source_text.insert(0, '')

        i = 0
        x = 0
        f = open(recovery_filename, "r")
        destination_name = recovery_filename[:-6]
        destination_file = destination_name + '_' + recovered_suffix + '.gcode'
        copy = open(destination_file, "wt")

        line = f.readline()

        for line in f:
            if x == (line_number - 2):
                try:
                    last_E = line.split('E', 1)[1]
                except:
                    mb.showerror("error", "This is not a usable line number!\n"
                                 "Add or subtract a few from your current number and try again.")
            x = x + 1

        inserted_gcode = ["; " + recovery_filename + " failed at line " + str(line_number) + "\n", "; gCode Defuct with Print Unfucker v.0.0.1 by The Mad Noodle\n\n"
             "G90\n", "M82\n", "G28 X0 Y0\n\n", "M201 X500 Y500; Set X and Y acceleration values\n", "M204 S500; Set default acceleration\n\n",
             "M104 S" + str(print_temp) + " T0\n", "M109 S" + str(print_temp) + " T0\n\n", "M117 God Speed and Good Luck\n\n",
             "T0\n", "G92 E" + str(last_E) + "\n", "G92 Z" + str(Z_height_offset) + "\n\n\n", ]

        copy.writelines(inserted_gcode)
        f.seek(0)

        for line in f:
            if i >= (line_number - 2):
                copy.write(str(line))

            if i == (line_number) - 2:
                copy.write("G1 Z" + str(Z_height) + "\n")

            i = i + 1
        f.close()
        copy.close()

        if mb.askyesno('Done', 'Your print is now UnFucked!\nWould you like to review your gcode?'):
            os.startfile(destination_file)

        else:
            print('done')
    except:
        mb.showerror("error", "This is not a usable line number!\n"
                              "Add or subtract a few from your current number and try again.")

def open_source_file():
    global recovery_filename
    window.source_filename = filedialog.askopenfilename(initialdir=default_open_dir, title="Select Source file",
                                               filetypes=(("gCode files", "*.gcode"), ("all files", "*.*")))
    source_text.delete(0, END)
    source_text.insert(0, '')
    source_text.insert(END, window.source_filename)



# == GUI Setup ==================================================================
window = Tk()

window.title("3D Print UnFucker v0.0.5")
#window.geometry('270x100')
window.iconbitmap('img/unf.ico')

# -- Logo
logo_img = PhotoImage(file='img/logo.png')
title_lbl = Label(window, image=logo_img, font='courier')
title_lbl.grid(columnspan=3, row=0, padx=5, pady=5)

source_btn = Button(window, text="Open Gcode", command=open_source_file)
source_btn.grid(column=0, row=1, padx=5, pady=5)

source_text = Entry(window)
source_text.grid(column=1, row=1, padx=5, pady=5)

line_lbl = Label(window, text='Line Number:')
line_lbl.grid(column=0, row=2, sticky=E, padx=5, pady=5)
line_field = Entry(window)
line_field.grid(column=1, row=2, sticky=W, padx=5, pady=5)

z_lbl = Label(window, text='Z-Height:')
z_lbl.grid(column=0, row=3, sticky=E, padx=5, pady=5)
z_field = Entry(window)
z_field.grid(column=1, row=3, sticky=W, padx=5, pady=5)

temp_lbl = Label(window, text='Temperature:')
temp_lbl.grid(column=0, row=4, sticky=E, padx=5, pady=5)
temp_field = Entry(window)
temp_field.grid(column=1, row=4, sticky=W, padx=5, pady=5)

button_img = PhotoImage(file='img/button_label.png')
unfuck_btn = Button(window, image=button_img, command=fix_gcode)
unfuck_btn.grid(column=1, columnspan=2, row=5, sticky=E, padx=5, pady=5)

window.mainloop()

