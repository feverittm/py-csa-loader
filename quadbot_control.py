from tkinter import *
import tkinter.font as tkfont


def do_nothing():
    pass


def leg_buttons():
    lb_label = Label(master=legs_frame, text="Select Leg to Control:")
    lb_label.pack(side=TOP)
    lb_button = []
    for leg in range(4):
        lb_button.append(Radiobutton(master=legs_frame, text=str(leg),
                                     value=str(leg), variable=selected_leg))
        lb_button[leg].pack(side=LEFT, padx=15, fill=X)


def build_sliders():
    # need 3 slider to control the position of each of the leg joints
    sl_dict = {0: "coxa", 1: "femur", 2: "tibia"}
    slider_label = []
    slider = []
    for item in range(3):
        slider.append(Scale(master=slider_frame, from_=0, to=100, length=200,
                            variable=sl_dict[item]))
        slider_label.append(Label(master=slider_frame, text=sl_dict[item]))
        slider_label[item].pack(side=LEFT)
        slider[item].pack(side=LEFT, padx=10)


# need to create this as an array of 2x3 buttons and not just a linear list...
def build_controls():
    controls_list = {
            "sit/reset": "cmd_reset",
            "stand": "cmd_stand",
            "walk forward": "cmd_fwd",
            "walk back": "cmd_back",
            "walk left": "cmd_left",
            "walk right": "cmd_right",
            "lean left": "cmd_lean_left",
            "lean right": "cmd_lean_right",
            "rotate left": "cmd_rot_left",
            "rotate right": "cmd_rot_right"
            }
    width = 4
    font14 = tkfont.Font(family="Lucida Grande", size=14)
    ctl_label = Label(master=controls_frame, text="Controls", font=font14)
    ctl_label.pack()
    ctl_button = []
    ctl_sub_frame = []
    prev = -1

    for idx, ckey in enumerate(controls_list):
        row = int(idx/width)
        # print ("debug button rows. Row="+str(row)+", Column="+str(idx%width)+", Previous="+str(prev))
        if row != prev:
            if prev >= 0:
                print(" ... pack row")
                ctl_sub_frame[-1].pack(side=TOP, fill=X, expand=True)
            # print("...Create new row")
            ctl_sub_frame.append(Frame(master=controls_frame))
        ctl_button.append(Button(master=ctl_sub_frame[row], text=ckey, font=font14))
        ctl_button[-1].pack(side=LEFT, padx=5, fill=X)
        prev = row
    ctl_sub_frame[-1].pack(side=TOP, fill=X, expand=True)


def soft_buttons():
    font14 = tkfont.Font(family="Lucida Grande", size=14)
    sk_button = []
    for skey in range(5):
        text_string = "Soft Key " + str(skey)
        sk_button.append(Button(master=sk_frame, text=text_string,
                         command=lambda c=skey: onButtonClicked(c),
                         font=font14))
        sk_button[skey].pack()


def onButtonClicked(button_id):
    print("Button" + str(button_id) + " is clicked!")


def build_menubar():
    menubar = Menu(window, background="#ff8000", foreground='black',
                   activebackground='white')
    filemenu = Menu(menubar, tearoff=0)
    filemenu.add_command(label="New", command=do_nothing)
    filemenu.add_command(label="Open", command=do_nothing)
    filemenu.add_command(label="Save", command=do_nothing)
    filemenu.add_separator()
    filemenu.add_command(label="Exit", command=window.quit)
    menubar.add_cascade(label="File", menu=filemenu)

    helpmenu = Menu(menubar, tearoff=0)
    helpmenu.add_command(label="Help Index", command=do_nothing)
    helpmenu.add_command(label="About...", command=do_nothing)
    menubar.add_cascade(label="Help", menu=helpmenu)

    window.config(menu=menubar)

# ------ main ------


# top level window stuff...
window = Tk()
window.title("Quadbot Controls")
window.geometry("450x450")
build_menubar()

fontStyle = tkfont.Font(family="Lucida Grande", size=18)
print("Font Size: "+str(fontStyle.cget('size')))

selected_leg = StringVar(window, "0")

# UI has two vertical frame and two horizontal frame
# top / bottom frame
#         bottom has just the list of control buttons across the window
# top frame is split horizontal to hold the softkeys on the right
#    and another frame on the left
#       left frame is split in two vertically to hold the leg selection on top
#       and the sliders below.  
#
# The size of the slider should drive the size of the main window.
#
# -- top frame has 3 sections...
top_frame = Frame()

legs_frame = Frame(master=top_frame)
leg_buttons()
legs_frame.pack(side=TOP, fill=X)

slider_frame = Frame(master=top_frame)
build_sliders()
slider_frame.pack(side=LEFT, fill=X)

sk_frame = Frame(master=top_frame)
soft_buttons()
sk_frame.pack(side=RIGHT, fill=Y)

top_frame.pack(side=TOP, fill=X)

# -- bottom frame for the controls
bot_frame = Frame()

controls_frame = Frame(master=bot_frame)
build_controls()
controls_frame.pack(side=BOTTOM, expand=True, fill=X)

bot_frame.pack(side=BOTTOM, fill=X)

# -- start the main UI loop...

window.mainloop()
