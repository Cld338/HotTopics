from tkinter import *
import tkinter as tk
import os
import time
from xmlrpc.client import boolean
from selenium import webdriver
from selenium.webdriver.common.by import By
import sys
import tkinter.messagebox as msgbox
import socket
from PIL import Image, ImageTk
import chromedriver_autoinstaller
directory = os.path.dirname(os.path.realpath(__file__)).replace("\\","/")
webdriver_options = webdriver.ChromeOptions()
webdriver_options.add_argument('headless')

chromedriver_autoinstaller.install()
driver = webdriver.Chrome(options=webdriver_options )
driver.implicitly_wait(3)


root = Tk()
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.attributes("-topmost", True)
root.config(bg = '#add123') #창 투명
# root.resizable(False)
root.wm_attributes('-transparentcolor','#add123')
img_size = 75
root.geometry(f"{img_size}x{img_size}+1180+280") #크기/x,y좌표
root.resizable(False,False) #너비,높이 변경 불가
root.overrideredirect(1) #상태 표시줄 제거

icon_path = f"{directory}/floating.png"
icon_img = ImageTk.PhotoImage(Image.open(icon_path).resize((50,50)))

icon_label = Button(root, image=icon_img, bg = '#add123', activebackground = '#add123', bd=0,)
icon_label.pack()
moved = boolean()
driver.get("https://signal.bz/")


def get_ranking():
    ipaddress=socket.gethostbyname(socket.gethostname())
    if ipaddress=="127.0.0.1":
        print("You are not connected to the internet!")
        return "인터넷에 연결되지\n않았습니다."
    else:
        # driver.implicitly_wait(3)
        
        driver.implicitly_wait(10)
        txt=""
        idx=1
        for k in driver.find_elements(By.CSS_SELECTOR,"#app > div > main > div > section > div > section > section > div > div > div > div > a > span.rank-text"):
            txt+=f"{(str(idx)+'.'+k.text)}"
            idx+=1
            if idx != 11:
                txt += "\n"
        # txt += "\b"
        return txt

def createNewWindow():
    global newWindow
    root_x,root_y = root.winfo_pointerxy()
    newWindow = Tk()
    newWindow.attributes("-topmost", True)
    newWindow.title("Hot Keywords🔥")
    newWindow.geometry(f"150x200+{root_x-100}+{root_y}") #크기/x,y좌표
    newWindow.attributes('-toolwindow', True) # 윈도우창 접기 버튼 없애기
    newWindow.protocol("WM_DELETE_WINDOW", reveal_icon)
    newWindow.protocol("WM_DELETE_WINDOW", reveal_icon)
    root.withdraw()
    rank_label = Label(newWindow, text=get_ranking())
    rank_label.pack()
    # insertBtn = Button(newWindow, text="↻", width=80)
    # insertBtn.pack(side=BOTTOM)


    if newWindow.winfo_x() < 35:
        newWindow.after(1,newWindow.geometry(f"150x200+{root_x-100}+{root_y}"))


def reveal_icon():
    global newWindow
    rank_x,rank_y = root.winfo_pointerxy()
    root.geometry(f"+{rank_x-100}+{rank_y-37}") 
    root.deiconify()
    newWindow.destroy()

def move_window(event):
    global moved
    moved = True
    x,y = root.winfo_pointerxy()
    root.geometry(f"{img_size}x{img_size}+{x-30}+{y-30}") #크기/x,y좌표
    print(root.winfo_x())


def clicked(event):
    global moved
    if moved == False:
        createNewWindow()
    moved = False

def close(event):
    response = msgbox.askyesno(title=None,message= "프로그램을 종료하시겠습니까?")
    if response == 1:
        root.destroy()
        sys.exit(0)
    elif response == 0:
        pass


root.bind('<B1-Motion>',move_window)
if moved==False: # Mouse left button pressed move
    root.bind('<ButtonRelease-1>',clicked)

root.bind('<Button-3>',close)

root.mainloop()