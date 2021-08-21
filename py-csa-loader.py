#!/usr/bin/env python3

"""
py-csa-loader

Forked from the original C# version of the tool:
http://github.com/JamieSinn/CSA-USB-Tool

Tool to download all files in a given FIRST season needed to support teams.

This tool downloads all the installers/packages for a given FRC season. 
CSA's commonly need these on hand in a USB to help teams update to the
latest version or to diagnose issues.

The original version of this application (which I think it awsome) was 
written in C# and some anti-virus/scanners will call out this as having 
a Trojan embedded in the application.  In order to work around this on some
platforms, I have re-written it in basic python with a tkinter gui.  I have 
tried to keep the same functionality as the original.

Looking at the original interface we will need:
1. Two main frames (top, bottom) full span, bottom is very short (1 line)
1.1. Bottom Frame has idle/busy indicator (label) and loading progress bar
1.2. Top is main window and is split into two frames left and right
1.2.1 Left frame has list widget for all files to be downloaded
1.2.2 Right frame with Year, Folder selection, and start download button

"""

import os
import sys
import argparse
import json
import pprint
import hashlib
import csv
from tkinter import *
from tkinter import filedialog
from tkinter.ttk import *
import tkinter.font as tkfont


def parse_args(arguments):
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    # parser.add_argument('infile', help="Input file", type=argparse.FileType('r'))
    parser.add_argument(
        "-o",
        "--outfile",
        help="Output file",
        default=sys.stdout,
        type=argparse.FileType("w"),
    )

    args = parser.parse_args(arguments)


def onButtonClicked(button_id):
    print("Button" + str(button_id) + " is clicked!")


def load_csv(file):
    with open(file) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=",")
        for row in readCSV:
            print(row)
            print(row[0])
            print(
                row[0], row[1], row[2],
            )



def main(arguments):
    parse_args(arguments)

    # find list of available software download lists
    # this list should ultimately come from an internet
    # download from the original github account.
    software_years = []
    files_list = []
    for file in os.listdir("."):
        if "FRCSoftware" in file:
            print(f"    software file: {file}")
            software_years.append(file)

    if len(software_years) == 0:
        print("No software years found")
        exit
    elif len(software_years) == 1:
        print(f"Only 1 year defined: {software_years[0]}")
    selected_software_year = software_years[0]

    files_list = []
    with open(selected_software_year, "r") as csvfile:
        read_dict = csv.DictReader(csvfile)
        for fn in read_dict:
            if fn["FriendlyName"][0] == "#":
                # this line is commented out
                del fn
            else:
                files_list.append(fn)
                print(f"File: {fn['FriendlyName']}")


    # top level window stuff...
    root = Tk()
    root.title("py-csa-loader")
    root.geometry("{}x{}".format(450, 450))
    fontStyle = tkfont.Font(family="Lucida Grande", size=18)

    files_frame = Frame(root)
    controls_frame = Frame(root)
    progress_frame = Frame(root)

    root.grid_rowconfigure(1, weight=1)
    root.grid_columnconfigure(0, weight=1)

    files_frame.grid(row=0, sticky="nw")
    controls_frame.grid(row=0, sticky="ne")
    progress_frame.grid(row=1, sticky="s")

    # downloadable files list
    file_label = Label(files_frame, text="Files:")
    files_listbox = Listbox(files_frame, selectmode = "BROWSE")
    idx = 1
    if files_list:
        for file in files_list:
            print(file)
            files_listbox.insert(idx, file['FriendlyName'])
            idx = idx + 1
    files_listbox.yview_scroll(5, UNITS)

    # select competition year
    year_label = Label(controls_frame, text="Select Competition Year ")
    year_list = Combobox(controls_frame)
    year_list['values'] = software_years
    year_list.current(0)

    # Select the Download Folder
    dl_folder_label = Label(controls_frame, text="Download Folder ")
    dl_folder_value = Label(controls_frame, text="")
    dl_browse_button = Button(controls_frame, text="Browse", command=get_directory(root, dl_folder_value))
    #root.withdraw()
    #folder_selected = filedialog.askdirectory()

    download_button = Button(controls_frame, text="Download", command=start_download())

    status_label = Label(progress_frame, text="Idle")

    file_label.grid(row=0, column=0)
    files_listbox.grid(row=1, column=0)
    
    year_label.grid(row=0, column=0)
    year_list.grid(row=0, column=1)
    
    dl_folder_label.grid(row=2, column=1)
    dl_folder_value.grid(row=2, column=2)
    dl_browse_button.grid(row=2, column=3)

    download_button.grid(row=3, column=2)

    status_label.grid(row=0, column=0)
    # -- bottom frame progress bar and status label
    # bot_frame = Frame(window)
    # progress = Progressbar(master=bot_frame, length = 200)
    # status_msg = Label(master=bot_frame, text = "Idle")
    # progress['value'] = 0
    # bot_frame.pack(side=BOTTOM, fill=X)
    # file_label.grid(column=0, row=0)

    # start the main gui loop
    root.mainloop()

def get_directory(root, dl_folder_value):
    #root.withdraw()
    folder_selected = filedialog.askdirectory()

    dl_folder_value.configure(text=folder_selected)

def start_download():
    print("Start Download")

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

