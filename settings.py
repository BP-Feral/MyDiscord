from tkinter import *

root = Tk()

root.geometry('300x240')
root.title('settings')
root.resizable(False, False)

def get_data():
    f = open("config.ini", "r")
    global lines
    lines = f.readlines()
    f.close()

def reset():
    f = open("config.ini", "w")
    
    lines=["[SERVER]\n",
    "host_address=localhost\n",
    "host_port=17578\n",
    "\n",
    "[CLIENT]\n",
    "connect_address=localhost\n",
    "connect_port=17578\n",
    "client_status=online\n",
    "image_default=default.png\n",
    "\n",
    "[INFO]\n",
    "client_status: online / idle / busy / away \n",
    "image_default: the name and extension of the file.\n",
    "               must be placed in folder avatar/\n"]

    f.writelines(lines)
    f.close()

    global host_on_address, host_on_port
    host_on_address = "localhost"
    host_on_port = "17578"
def update_file():
    f = open("config.ini", "w")
    f.writelines(lines)
    f.close()

def set_address():
    global lines
    host_on_address = host_address_entry.get()
    lines[1] = f"host_address={host_on_address}\n"
    update_file()

def set_port():
    global lines
    host_on_port = host_port_entry.get()
    lines[2] = f"host_port={host_on_port}\n"
    update_file()
    
def set_address_2():
    global lines
    connect_to_address = connect_address_entry.get()
    lines[5] = f"connect_address={connect_to_address}\n"
    update_file()

def set_port_2():
    global lines
    connect_to_port = connect_port_entry.get()
    lines[6] = f"connect_port={connect_to_port}\n"
    update_file()

def set_status():
    global lines
    status_to_use = status_to_use_entry.get()
    lines[7] = f"client_status={status_to_use}\n"
    update_file()

def set_avatar():
    global lines
    avatar_to_use = image_default_entry.get()
    lines[8] = f"image_default={avatar_to_use}\n"
    update_file()


get_data()

SERVER_LABEL = Label(root, text="\t[SERVER]")
SERVER_LABEL.place(x=5, y=5)

host_address_label = Label(root, text="Host Address: ")
host_address_label.place(x=5, y=25)
host_address_entry = Entry(root)
host_address_entry.place(x=85, y=25)
host_address_button = Button(root, text="Set", command=set_address)
host_address_button.place(x=200, y=25)

host_port_label = Label(root, text="Port Address: ")
host_port_label.place(x=5, y=50)
host_port_entry = Entry(root, width=6)
host_port_entry.place(x=85, y=50)
host_port_button = Button(root, text="Set", command=set_port)
host_port_button.place(x=200, y=50)

CLIENT_LABEL = Label(root, text="\t[CLIENT]")
CLIENT_LABEL.place(x=5, y=85)

connect_address_label = Label(root, text="Connection Address: ")
connect_address_label.place(x=5, y=105)
connect_address_entry = Entry(root)
connect_address_entry.place(x=120, y=105)
connect_address_button = Button(root, text="Set", command=set_address_2)
connect_address_button.place(x=250, y=105)

connect_port_label = Label(root, text="   Connection Port: ")
connect_port_label.place(x=5, y=125)
connect_port_entry = Entry(root)
connect_port_entry.place(x=120, y=125)
connect_port_button = Button(root, text="Set", command=set_port_2)
connect_port_button.place(x=250, y=125)

status_to_use_label = Label(root, text="       Client Status: ")
status_to_use_label.place(x=5, y=145)
status_to_use_entry = Entry(root)
status_to_use_entry.place(x=120, y=145)
status_to_use_button = Button(root, text="Set", command=set_status)
status_to_use_button.place(x=250, y=145)

image_default_label = Label(root, text="Client Image: avatar/")
image_default_label.place(x=5, y=165)
image_default_entry = Entry(root)
image_default_entry.place(x=120, y=165)
image_default_button = Button(root, text="Set", command=set_avatar)
image_default_button.place(x=250, y=165)

reset_client = Button(root, text="Reset Settings", command=reset)
reset_client.place(x=5, y=195)

root.mainloop()