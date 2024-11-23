# module to create the user interface
from tkinter import *
import tkinter.font as tkFont
import threading
import socket
import time
import random

# module to collect display data
from win32api import GetMonitorInfo, MonitorFromPoint

# module to reclaim windows explorer activity
# yes, "reclaim" :)) because 'root.overrideredirect(True)' breaks explorer.exe
from ctypes import windll

settings = []

f = open("config.ini", "r")
settings = f.readlines()
f.close()

settings_connect_address = settings[5][16:-1]
settings_connect_host = settings[6][13:-1]
settings_status = settings[7][14:-1]
settings_image = settings[8][14:-1]

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((settings_connect_address, int(settings_connect_host)))

from PIL import Image
def add_status( status , image_name):
    if status == "online":
        frontImage = Image.open('data/online.png')
    elif status == "idle":
        frontImage = Image.open('data/idle.png')
    elif status == "busy":
        frontImage = Image.open('data/busy.png')
    elif status == "away":
        frontImage = Image.open('data/invisible.png')
    else:
        print("[WARNING] > Something went wrong with the status ! \n[WARNING] > Forced 'invisible' mode")
        frontImage = Image.open('data/away.png')
    

    try:
        background = Image.open(f'avatar/{image_name}')
    except:
        print("[WARNING] > Something went wrong with the avatar ! \n[WARNING] > Forced default avatar")
        background = Image.open('avatar/default.png')

    resized_image= background.resize((32,32), Image.ANTIALIAS)

    frontImage = frontImage.convert("RGBA")
    background = resized_image.convert("RGBA")
    

    width = (background.width - frontImage.width) // 2
    height = (background.height - frontImage.height) // 2
    background.paste(frontImage, (width, height), frontImage)
    background.save("data/border.png", format="png")

def circular_photo( status , image_name):
    import numpy as np
    from PIL import Image, ImageDraw

    # Open the input image as numpy array, convert to RGB
    img=Image.open(f"avatar/{image_name}").convert("RGB")
    npImage=np.array(img)
    h,w=img.size

    # Create same size alpha layer with circle
    alpha = Image.new('L', img.size,0)
    draw = ImageDraw.Draw(alpha)
    draw.pieslice([0,0,h,w],0,360,fill=255)

    # Convert alpha Image to numpy array
    npAlpha=np.array(alpha)

    # Add alpha layer to RGB
    npImage=np.dstack((npImage,npAlpha))

    # Save with alpha
    Image.fromarray(npImage).save('avatar/result.png')

    small = Image.open('avatar/result.png')
    small_image = small.resize((32,32))
    small_image.save('avatar/small_result.png')

class Discord:

    def __init__(self, master):

        self.font_Helvetica_9_bold = tkFont.Font(family="HelveticaR", size=9, weight="bold")
        self.font_Helvetica_9 = tkFont.Font(family="HelveticaR", size=9)
        
        self.font_Helvetica_10_bold = tkFont.Font(family="HelveticaR", size=11, weight="bold")
        self.font_Helvetica_10 = tkFont.Font(family="HelveticaR", size=11)
        
        self.GWL_EXSTYLE = -20
        self.WS_EX_APPWINDOW = 0x00040000
        self.WS_EX_TOOLWINDOW = 0x00000080
       
        self.DARK_GREY = "#202225"
        self.GREY = "#2f3136"
        self.LIGHT_GREY =  "#36393f"
        self.SLIGHT_GREY = "#292b2f"
        self.LIGHTER_GREY = "#b0b2b5"
        self.LIGHT_RED = "#ed4245"
        self.WHITE = "#ffffff"
        
        # DEBUGGING / BUILDING COLORS
        self.GREEN = "#70E442"
        self.BLUE = "#3D90DD"
        self.YELLOW = "#FAF62A"


        self.status = settings_status
        self.running = True


        monitor_info = GetMonitorInfo(MonitorFromPoint((0,0)))
        self.work_area = monitor_info.get("Work")
        self.win_height = int(self.work_area[3])
        self.win_width = int(self.work_area[2])
        print(self.win_width)
        
        self.windowed = 1
        self.z = 0
   
    def receive(self):
        while self.running:
            print (self.running)
            try:
                message = client.recv(1024).decode('ascii')
                if message == 'DISCONNECT':
                    print("Usernames starting with SSH are not allowed!\n Disconnected. Relaunch the client and try again!")
                    client.close()
                    break
                else:
                        print(message)
                                                
                        self.text_box.config(state=NORMAL)
                        self.text_box.insert('end', f"{message}")
                        self.text_box.config(state=DISABLED)
                        self.text_box.see(END)                      
            except:
                self.running = False
                print("An error occurred!")

                client.close()
                break


    def add_image(self):
        circular_photo(self.status, settings_image)
        self.circular = PhotoImage(file="avatar/small_result.png")
        self.text_box.image_create(CURRENT, image=self.circular)
        print("LINE 57, 68")
        return 'break'


    def send_message(self, e):
        global good_name, good_tag, latest
        data = self.entry_box.get('1.0', END)
        if data != '' or data != '\n':
            if latest != good_name:
                self.text_box.config(state=NORMAL)

                self.add_image()
                print(data)
                client.send(data.encode('ascii'))
                self.text_box.insert('end', f"\n{good_name}#{good_tag}\n")
                
                latest = good_name
                print ("latest name is", latest)
            else:
                self.text_box.config(state=NORMAL)
                client.send(data.encode('ascii'))
                #self.text_box.insert('end',f"{data}" )
                
            self.entry_box.delete('1.0', END)
            self.entry_box.mark_set(INSERT, '0.0')
            self.text_box.config(state=DISABLED)
            
            self.text_box.see(END)
            return 'break'

    def client_start(self, master):
        master.geometry(f"+{int(self.work_area[2]/2-512)}+{int(self.work_area[3]/2-256)}")
        master.overrideredirect(True)
        master.config(bg=self.LIGHT_GREY)
        self.status = settings_status

    def client_set_appwindow(self, master):
        hwnd = windll.user32.GetParent(master.winfo_id())
        style = windll.user32.GetWindowLongPtrW(hwnd, self.GWL_EXSTYLE)
        style = style & ~self.WS_EX_TOOLWINDOW
        style = style | self.WS_EX_APPWINDOW
        res = windll.user32.SetWindowLongPtrW(hwnd, self.GWL_EXSTYLE, style)
        # re-assert the new window style
        master.withdraw()
        master.after(10, master.deiconify)

    def get_pos(self, e):
        # obtain coords where the click is made
        self.xwin = e.x
        self.ywin = e.y

    def move_app(self, e):
        # move the app on screen
        root.geometry(f'+{e.x_root - self.xwin}+{e.y_root - self.ywin}')

    def quitter(self, e):
        # stop tkinter process
        self.running = False
        root.destroy()
        time.sleep(1)
        client.send('CONNECTION TERMINATED!'.encode('ascii'))
        client.close()

        print("[DEBUG] > {quitter} called !")
        

    def on_enter(self, e):
        # :hover: on "✕" button
        self.close_label.config(bg="#ed4245")
        
    def on_leave(self, e):
        # leave :hover: on "✕" button
        self.close_label.config(bg="#202225")

    def window_on_enter(self, e):
        # :hover: on "◻" button
        self.window_label.config(bg="#282b2e")
        
    def window_on_leave(self, e):
      # leave :hover: on "◻" button
        self.window_label.config(bg="#202225")

    def minimize_on_enter(self, e):
        # :hover: on "─" button
        self.minimize_label.config(bg="#282b2e")
    
    def minimize_on_leave(self, e):
        # leave :hover: on "─" button
        self.minimize_label.config(bg="#202225")
   
    def change_window_mode(self, e):
        # switch fullscreen/maximized
        self.windowed += 1
        if self.windowed % 2 == 0:
            print("DEBUG > maximized")

            self.window_label.config(text=" ❐ ")

            root.geometry("+0+0")
            root.geometry(f"{self.work_area[2]}x{self.work_area[3]}")

            self.frame_left_body.config(height=self.win_height)

            self.chat_box.config(bg=self.LIGHT_GREY, height=self.win_height-21, width=self.work_area[2]-240-73)

            self.frame_left_body.update()

            self.frame_height = self.frame_left_body.winfo_height()
            self.frame_user.place(x=0, y=self.work_area[3]-53-21)
            ### 53 = user frame height, 21 = title bar frame height

            self.frame_entry_box.config(width=self.work_area[2]-240-73)
            self.frame_entry_box.place(y=self.frame_height-66-21)
            ### 66 = entry box size, 21 = title bar frame height

            self.chat_title.config(width=self.work_area[2]-240-72)
            self.inner_chat_box.config(height=self.work_area[3]-66-48-21, width=self.work_area[2]-240-72-72)

        if self.windowed % 2 != 0:
            print("DEBUG > windowed")

            self.window_label.config(text=" ◻ ")

            root.geometry(f"+{int(self.work_area[2]/2-512)}+{int(self.work_area[3]/2-256)}")
            root.geometry("1024x512")

            self.frame_left_body.config(height=492)

            self.chat_box.config(bg=self.LIGHT_GREY, height=492, width=1024-240-72)   

            self.frame_left_body.update()

            self.frame_height = self.frame_left_body.winfo_height()
            self.frame_user.place(x=0, y=self.frame_height-53)

            self.frame_entry_box.config(width=1024-240-72)
            self.frame_entry_box.place(y=self.frame_height-66)

            self.chat_title.config(width=1024-240-72)

            self.inner_chat_box.config(height=498-66-48-7, width=1024-240-72-72)

    def minimize_mode(self, e):
        # switch minimized
        print("DEBUG > minimized")
        root.state('withdrawn')
        root.overrideredirect(False)
        root.state('iconic')
        self.z = 1

    def frameMapped(self, e):
        # get back window on screen
            root.overrideredirect(True)
            if self.z == 1:
                self.client_set_appwindow(root)
                self.z = 0

    def client_init_inteface(self, master):
        # create custom title bar
        self.title_bar = Frame(master, bg="#202225", relief="raised", bd=0)
        self.title_bar.pack(expand=0, fill=X)

        # bind the titlebar
        self.title_bar.bind("<B1-Motion>", self.move_app)
        self.title_bar.bind("<Button-1>", self.get_pos)

        # create title icon
        self.image_logo=PhotoImage(file='data/logo.png')
        self.title_label = Label(self.title_bar, image=self.image_logo, bg="#202225")
        self.title_label.pack(side=LEFT , pady=0)

        # create close button on titlebar
        self.close_label = Label(self.title_bar, text="  ✕ ", font="Arial 10", bg="#202225", fg="#99AAB5", relief="sunken", bd=0)
        self.close_label.pack(side=RIGHT, fill=Y)
        self.close_label.bind("<Button-1>", self.quitter)
        self.close_label.bind("<Enter>", self.on_enter)
        self.close_label.bind("<Leave>", self.on_leave)

        # create window mode button on titlebar
        self.window_label = Label(self.title_bar, text=" ◻ ", font="Arial 13", bg="#202225", fg="#99AAB5", relief="sunken", bd=0)
        self.window_label.pack(side=RIGHT, fill=Y)
        self.window_label.bind("<Button-1>", self.change_window_mode)
        self.window_label.bind("<Enter>", self.window_on_enter)
        self.window_label.bind("<Leave>", self.window_on_leave)

        # create minimized mode button on titlebar
        self.minimize_label = Label(self.title_bar, text=" ─ ", font="Arial 13", bg="#202225", fg="#99AAB5", relief="sunken", bd=0)
        self.minimize_label.pack(side=RIGHT, fill=Y)
        self.minimize_label.bind("<Button-1>", self.minimize_mode)
        self.minimize_label.bind("<Enter>", self.minimize_on_enter)
        self.minimize_label.bind("<Leave>", self.minimize_on_leave)

        master.bind("<Map>", self.frameMapped)

        self.frame_guild = Frame(master, bg=self.DARK_GREY, width=75) # GUILD LIST {FRAME = frame_guild}
        self.frame_guild.pack(side=LEFT, fill=Y)

        self.frame_left_body = Frame(master, bg=self.GREY, height=491, width=240) # DM LIST {FRAME = frame_left_body}
        self.frame_left_body.place(x=72, y=21)

        self.corner_image=PhotoImage(file='data/corner.png')
        self.corner = Frame(self.frame_left_body, width=10, height=10)
        self.corner.place(x=0, y=0)
        self.label_image = Label(self.corner, image=self.corner_image, borderwidth=0, compound="center", highlightthickness = 0)
        self.label_image.pack() 


        self.frame_left_body.update()
        self.frame_height = self.frame_left_body.winfo_height()

        ######### USER FRAME ##########
        self.frame_user = Frame(self.frame_left_body, bg=self.SLIGHT_GREY, height=53, width=240) # USER DETAILS {FRAME = frame_user}
        self.frame_user.place(x=0, y=self.frame_height-53)


        # avatar
        self.frame_picture = Frame(self.frame_user, height=32, width=32, bg=self.LIGHT_RED) # AVATAR {FRAME = frame_picture}
        self.frame_picture.place(x=8, y=10)
        
        
        add_status(self.status, settings_image)
        
        self.avatar_image = PhotoImage(file='data/border.png')
        self.avatar_box = Label(self.frame_picture, image=self.avatar_image, borderwidth=0, compound="center", highlightthickness = 0)
        self.avatar_box.pack()
        self.avatar_box.update()


        # user_tag
        self.frame_tag = Frame(self.frame_user, height=15, width=50, bg=self.LIGHT_RED) # USERNAME {FRAME = frame_username}
        self.frame_tag.place(x=50, y=25)
        self.label_tag = Label(self.frame_tag, text=f"{'#' + str(good_tag)}", bg=self.SLIGHT_GREY, fg=self.LIGHTER_GREY, font=self.font_Helvetica_9_bold)
        self.label_tag.pack()


        # username
        self.frame_username = Frame(self.frame_user, height=15, width=90, bg=self.LIGHT_RED) # USERNAME {FRAME = frame_username}
        self.frame_username.place(x=50, y=10)
        self.label_username = Label(self.frame_username, text=good_name, bg=self.SLIGHT_GREY, fg=self.WHITE, font=self.font_Helvetica_9_bold)
        self.label_username.pack()
        
        
        # microphone
        self.frame_bt_1 = Frame(self.frame_user, height=18, width=18)
        self.frame_bt_1.place(x=143, y=17)
        self.mic_image = PhotoImage(file='data/mic.png')
        self.mic_label = Label(self.frame_bt_1, image=self.mic_image, borderwidth=0, compound="center", highlightthickness = 0)
        self.mic_label.pack()

        # headphones
        self.frame_bt_2 = Frame(self.frame_user, height=18, width=18)
        self.frame_bt_2.place(x=176, y=17)
        self.headphone_image = PhotoImage(file='data/headphone.png')
        self.headphone_label = Label(self.frame_bt_2, image=self.headphone_image, borderwidth=0, compound="center", highlightthickness = 0)
        self.headphone_label.pack()

        # settings
        self.frame_bt_3 = Frame(self.frame_user, height=18, width=18)
        self.frame_bt_3.place(x=210, y=17)
        self.settings_image = PhotoImage(file='data/settings.png')
        self.settings_label = Label(self.frame_bt_3, image=self.settings_image, borderwidth=0, compound="center", highlightthickness = 0)
        self.settings_label.pack()

        # chat box
        self.chat_box = Frame(master, bg=self.LIGHT_GREY, height=492, width=1024-240-72) # DM LIST {FRAME = chat_box}
        self.chat_box.place(x=72+240, y=21)

        # chat_title
        self.chat_title = Frame(self.chat_box, bg=self.SLIGHT_GREY, height=48, width=1024-240-72)
        self.chat_title.place(x=0,y=0)
        
        # input field
        self.frame_entry_box = Frame(self.chat_box, bg=self.SLIGHT_GREY, height=66, width=1024-240-72)
        self.frame_entry_box.place(y=self.frame_height-66)

        # inner chat box
        self.inner_chat_box = Frame(self.chat_box, bg=self.LIGHT_GREY, height=498-66-48-7, width=1024-240-72-72)
        self.inner_chat_box.place(x=72, y=48)

        # text box
        self.text_box = Text(self.inner_chat_box,fg=self.WHITE,height=22, bg=self.LIGHT_GREY ,bd=0, font=self.font_Helvetica_10)
        self.text_box.pack(expand=True, fill=BOTH)
        self.text_box.config(state=DISABLED)

        self.entry_box = Text(self.frame_entry_box, fg=self.WHITE, width=100, height=2, bg=self.GREY, bd=0, font=self.font_Helvetica_10)
        self.entry_box.bind('<Return>', self.send_message)
        self.entry_box.place(x=0, y=0)

    def start_threads(self, master):
        self.receiving = threading.Thread(target=self.receive)
        self.receiving.daemon = True
        self.receiving.start()

       
class Login:
    def __init__(self, master): 
        self.font_tuple = ("SimSun-ExtB", 20, "bold")
        
        self.GWL_EXSTYLE = -20
        self.WS_EX_APPWINDOW = 0x00040000
        self.WS_EX_TOOLWINDOW = 0x00000080
       
        self.DARK_GREY = "#202225"
        self.GREY = "#2f3136"
        self.LIGHT_GREY =  "#36393f"
        self.SLIGHT_GREY = "#292b2f"
        self.LIGHT_RED = "#ed4245"

        monitor_info = GetMonitorInfo(MonitorFromPoint((0,0)))
        self.work_area = monitor_info.get("Work")
        self.win_height = int(self.work_area[3])

    def login_start(self, master):
        root.geometry(f"+{int(self.work_area[2]/2-250)}+{int(self.work_area[3]/2-200)}")
        root.overrideredirect(True) # remove title bar
        root.config(bg=self.LIGHT_GREY)

    def login_quitter(self, e):
        root.destroy()

    def move_login_app(self, e):
        root.geometry(f'+{e.x_root - self.xwin}+{e.y_root - self.ywin}')
        # :hover: on "✕" login_button
    
    def on_login_enter(self, e):
        self.login_close_label.config(bg="#ed4245")
        # leave :hover: on "✕" login_button

    def on_login_leave(self, e):
        self.login_close_label.config(bg="#202225")

    def login_set_appwindow(self, master):
        hwnd = windll.user32.GetParent(master.winfo_id())
        style = windll.user32.GetWindowLongPtrW(hwnd, self.GWL_EXSTYLE)
        style = style & ~self.WS_EX_TOOLWINDOW
        style = style | self.WS_EX_APPWINDOW
        res = windll.user32.SetWindowLongPtrW(hwnd, self.GWL_EXSTYLE, style)
        # re-assert the new window style
        master.withdraw()
        master.after(10, master.deiconify)

    def LimitSize(self, *args):
        value = self.nameValue.get()
        if len(value) > 20: self.nameValue.set(value[:20])

    def get_pos(self, e):
        self.xwin = e.x
        self.ywin = e.y

    def login_init_interface(self, master):
        self.login_title_bar = Frame(master, bg="#202225", relief="raised", bd=0)
        self.login_title_bar.pack(expand=0, fill=X)

        # bind the titlebar
        self.login_title_bar.bind("<B1-Motion>", self.move_login_app)
        self.login_title_bar.bind("<Button-1>", self.get_pos)

        # create title
        self.login_title_label = Label(self.login_title_bar,text="Discord", bg="#202225", fg="#99AAB5")
        self.login_title_label.pack(side=LEFT , pady=0)

        # create close button on titlebar
        self.login_close_label = Label(self.login_title_bar, text="  ✕ ", font="Arial 10", bg="#202225", fg="#99AAB5", relief="sunken", bd=0)
        self.login_close_label.pack(side=RIGHT, fill=Y)
        self.login_close_label.bind("<Button-1>", self.login_quitter)
        self.login_close_label.bind("<Enter>", self.on_login_enter)
        self.login_close_label.bind("<Leave>", self.on_login_leave)

        self.name_label = Label(master, text="   Choose a username", bg=self.LIGHT_GREY, fg="gray", font=self.font_tuple)
        self.name_label.place(x=80, y=30)

        self.nameValue = StringVar()
        self.nameValue.trace('w', self.LimitSize)

        self.login_entry = Entry(master, bg=self.GREY, font=self.font_tuple, fg="white", textvariable=self.nameValue)
        self.login_entry.place(x=105,y=70)
    
        self.login_button = Button(master, text="Join", font=self.font_tuple, bg=self.GREY, fg="white", activebackground=self.DARK_GREY, command=self.get_name)
        self.login_button.place(x=210, y=120)

        root.mainloop()
    
    def get_name(self):
        if self.login_entry.get() == "":
            self.name_label.config(fg=self.LIGHT_RED, text="  Please type a name!")
        elif self.login_entry.get()[:1] == " ":
            self.name_label.config(fg=self.LIGHT_RED, text="do not start with space!")
        else:
            global good_name
            global good_tag
            good_name = self.login_entry.get()
            client.send(good_name.encode('ascii'))
            choose = True
            while (choose):
                choose = False
                good_tag = random.randint(1000, 9999)
                if good_tag in used_tags:
                    good_tag = random.randint(1000, 9999)
                    choose = True

                
            root.destroy()
            time.sleep(1)
            Start_Discord()
            

def Start_Discord():
    global root

    root = Tk()
    root.withdraw()
    time.sleep(1)

    root.title('Discord')
    root.iconbitmap('data/app.ico')
    root.geometry("1024x512")
    root.deiconify()

    discord = Discord(root)
    discord.client_start(root)
    discord.client_set_appwindow(root)
    discord.client_init_inteface(root)
    discord.start_threads(root)

    root.mainloop()

def Login_Discord():
    print("[DEBUG] > STARTING UP {Login_Discord} !")
    global root
    root = Tk()
    root.withdraw()
    
    time.sleep(1)

    root.title('Discord')
    root.iconbitmap('data/app.ico')
    root.geometry("500x200")
    root.deiconify()

    discord = Login(root)
    discord.login_start(root)
    discord.login_set_appwindow(root)
    discord.login_init_interface(root)

    root.mainloop()

def Use_Login( bool ):
    if bool == True:
        Login_Discord()
    else:
        global good_name
        global good_tag
        good_name, good_tag = "Admin", "0000"
        Start_Discord()

if __name__ == '__main__':
    global latest
    latest = ''
    global discord
    global used_tags
    global status
    used_tags = []

                ### CONFIG ###

    # status: green: "online" yellow: "idle"
    # status:  red: "busy" grey: "invisible"
    status = "busy"

    # use login: True / False
    Use_Login(True)

                ### ###### ###

#_______________________________________________________________________________________________#/
# BUGS /// TO FIX
# 
# 1. Window cannot be moved from top left corner {TO BE FIXED}
# 2. Window appears to be black and small while using Alt + Tab if the window is minimized {BUG}
#
# 4. The application icon show pyscript image on taskbar {TO BE FIXED}
#
#
# 7. A white box appear when switching between login and client window {TO BE FIXED}
# 8. +1 px right margin bug in text box frame {TO BE FIXED}
# 9. Adjust entry box, and format layout {TO BE FIXED}
#

#_______________________________________________________________________________________________#/
# 3. The application icon show default feather on titlebar {!!! FIXED !!!}
#
# 5. Closing the application freeze for some seconds {!!! FIXED !!!}
# 6. Resizing the window doesn't move the user frame {!!! FIXED !!!}


#_______________________________________________________________________________________________#/
# TO DO
#
#  [ ] FIX RESIZE
#  [ ] FIX IMAGE
#  [ ] GENERATE SETTINGS
#  [ ] GENERATE RESET
#  [ ] CLEAR THE CODE
#
#  [X] Move the window from title bar
#  [X] Reseize frames depending on minimize/maximize
#  [ ] Implement the input boxes
#  [X] Create the server thread
#  [X] Configuring daemon to listen for send/receive data
#  [ ] Create and save accounts
#  [ ] Add and remove friends
#  [ ] Implement groups
#  [ ] Add File Transfer
#  [ ] Improve avatar customization
#  [ ] Add voice support
#  [ ] Change activity automatically
#  [ ] Compress the code, build functions
#_______________________________________________________________________________________________#/