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
from tkinter import messagebox
from tkinter import filedialog
from tkinter.ttk import Combobox
import tkinter.font as tkfont
import requests


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


def load_csv(file):
    with open(file) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=",")
        for row in readCSV:
            print(row)
            print(row[0])
            print(
                row[0], row[1], row[2],
            )


def load_files(selected_software_year):
    if len(files_list) > 0:
        files_list.clear()
    fd = {}
    with open(selected_software_year, "r") as csvfile:
        read_dict = csv.DictReader(csvfile)
        for fn in read_dict:
            print(fn)
            files_list.append(fn)
            fd[fn['#FriendlyName']] = fn


def update_year(event):
    if not year_list.get() == "":
        year_selected = year_list.get()
        print(f"Year selected: {year_selected}")
        load_files(year_selected)
        files_listbox.delete(0, END)
        idx=0
        for file in files_list:
            files_listbox.insert(END, file['#FriendlyName'])
            files_index[file['#FriendlyName']] = idx
            idx = idx + 1


def get_directory():
    selected_write_folder = StringVar()
    selected_write_folder = filedialog.askdirectory()
    print(f"Write Folder: {selected_write_folder}")
    if len(selected_write_folder) > 0:
        dir = os.listdir(selected_write_folder)
        if not os.path.exists(selected_write_folder):
            print(f"Cannot file directory {selected_write_folder}")
            return()
        if len(dir) > 0:
            print("Error: Download Directory not empty!")
            return()
        if not os.access(selected_write_folder, os.W_OK):
            print("Error: Download Directory not writable!")
            return()
        selected_download_folder.set(selected_write_folder)


def start_download():
    print("Start Download")
    dest_folder = dl_folder_value.get()
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)  # create folder if it does not exist
    print(f"  ... download folder = {dest_folder}")

    files = []
    cname = files_listbox.curselection()
    for i in cname:
        op = files_listbox.get(i)
        files.append(op)
    for val in files:
        print(val)


def download(url: str, dest_folder: str):
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)  # create folder if it does not exist

    # be careful with file names
    filename = url.split('/')[-1].replace(" ", "_")
    file_path = os.path.join(dest_folder, filename)

    r = requests.get(url, stream=True)
    if r.ok:
        print("saving to", os.path.abspath(file_path))
        with open(file_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024 * 8):
                if chunk:
                    f.write(chunk)
                    f.flush()
                    os.fsync(f.fileno())
    else:  # HTTP status code 4XX/5XX
        print("Download failed: status code {}\n{}".format(r.status_code, r.text))


# start main...

parse_args(sys.argv[1:])

# find list of available software download lists
# this list should ultimately come from an internet
# download from the original github account.
software_years = []
files_list = []
files_index = {}
for file in os.listdir("."):
    if "FRCSoftware" in file:
        print(f"    software file: {file}")
        software_years.append(file)

if len(software_years) == 0:
    print("No software years found")
    exit
elif len(software_years) == 1:
    print(f"Only 1 year defined: {software_years[0]}")
selected_software_year = software_years[-1]
print(f"Selecting Default Year {selected_software_year}")

load_files(selected_software_year)

# top level window stuff...
root = Tk()
root.title("py-csa-loader")
#root.geometry("{}x{}".format(450, 450))
#fontStyle = tkfont.Font(family="Lucida Grande", size=18)

top_frame = Frame()

# downloadable files list
files_frame = Frame(master=top_frame, relief=RAISED, borderwidth=1)
files_listbox = Listbox(master=files_frame, selectmode="multiple")
files_listbox.pack(side=LEFT, fill=BOTH)
scrollbar = Scrollbar(master=files_frame)
scrollbar.pack(side=RIGHT, fill=BOTH)
if files_list:
    for file in files_list:
        files_listbox.insert(END, file['#FriendlyName'])
files_listbox.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=files_listbox.yview)
files_frame.pack(side=LEFT)

controls_frame = Frame(master=top_frame)

# select competition year
selected_year = StringVar()
year_frame = Frame(master=controls_frame)
year_label = Label(master=year_frame, text="Select Competition Year ")
year_label.pack(side=LEFT)
year_list = Combobox(master=year_frame, textvariable=selected_year)
year_list['values'] = software_years
year_list.current(len(software_years)-1)
year_list.pack(side=RIGHT, padx=5)
year_list.bind('<<ComboboxSelected>>', update_year)
year_frame.pack(side=TOP, pady=10, fill=X)

# Select the Download Folder
selected_download_folder = StringVar()
dl_frame = Frame(master=controls_frame)
dl_folder_label = Label(master=dl_frame, text="Download Folder ")
dl_folder_label.pack(side=LEFT)
dl_folder_value = Entry(master=dl_frame, textvariable=selected_download_folder)
dl_folder_value.pack(side=LEFT, padx=2)
dl_browse_button = Button(
    master=dl_frame, text="Browse", command=get_directory)
dl_browse_button.pack(side=LEFT, padx=7)
dl_frame.pack(side=TOP)

db_frame = Frame(master=controls_frame)
download_button = Button(
    master=db_frame, text="Download", command=start_download)
download_button.pack(side=BOTTOM, pady=20, fill=X, expand=True)
db_frame.pack(side=BOTTOM, fill=X, expand=True)

controls_frame.pack(side=TOP)

#status_label = Label(progress_frame, text="Idle")

top_frame.pack(side=TOP)

# -- bottom frame progress bar and status label
bot_frame = Frame(root)
#progress = Progressbar(master=bot_frame, length=200)
# progress.pack(side=LEFT)
status_msg = Label(master=bot_frame, text="Idle")
status_msg.pack(side=LEFT)
# progress['value'] = 0
bot_frame.pack(side=BOTTOM, fill=X)

# start the main gui loop
root.mainloop()
