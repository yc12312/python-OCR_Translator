#!/usr/bin/env python
# coding: utf-8

# In[7]:


#ver 1.0
import tkinter
import tkinter.ttk
import win32gui
from pyscreenshot import grab
try:
    from PIL import Image
except ImportError:
    import Image
    
import pytesseract
from googletrans import Translator

import time

import threading
from queue import Queue

import os

import multiprocessing


#Globals
img = None
x1 = 0
x2 = 0
y1 = 0
y2 = 0

transFromlang = 'en'
transTolang = 'ko'

cap_lang = 'eng'

original_result = 'None'
tr_results = 'None'
org_lb = None
tr_lb = None

now_result = None
past_result = None

t1 = None
t2 = None

cb = None

#OCR
def ocr(q):
    while True:
        #Get Cordinate
        global x1,x2,y1,y2
        x1 = cb.winfo_rootx()
        x2 = x1 + cb.winfo_width()
        y1 = cb.winfo_rooty()
        y2 = y1 + cb.winfo_height()
    
        #Create Screenshot
        global img
        img = grab(bbox=(x1,y1,x2,y2))
    
        global now_result
        global past_result
        
        global tr_results
        now_result = pytesseract.image_to_string(img , lang = cap_lang)
        now_result = now_result.replace('\n', ' ')
        if(past_result != now_result): 
            past_result = now_result
            
            evt = threading.Event()
            q.put((now_result,evt))
            
            tr_results = 'waitng for tanslation!\n'
            configure_text(tr_lb,tr_results)
            evt.wait() 
      
         
#Translation
def trans(q):
    #making translator
    translator = Translator()
    
    global original_result
    global tr_results
    
    while True:
        data,evt = q.get()
    
        try:
            original_result = data + '\n'
            temp = translator.translate(data, src= transFromlang, dest=transTolang)
            tr_results = temp.text + '\n'
            
        except:
            original_result = 'Data is none\n'
            tr_results = 'Data is none\n'
            pass
        
        configure_text(org_lb,original_result)
        configure_text(tr_lb,tr_results)
        
        evt.set()
        q.task_done()

def threadStart():
    global t1,t2
    
    q = Queue()
    t1 = threading.Thread(target=ocr,args=(q,))
    t2 = threading.Thread(target=trans,args=(q,))
    t1.start()
    t2.start()
    q.join()
    
def threadStop(thread):
    global past_result
    past_result = None
    
    thread._is_running = False

def configure_text(target, data):
    target.configure(text = data)

def configure_font(eventObject):
    
    data = eventObject.widget.get()
        
    org_lb.configure(font = ("Helvetica", data))
    tr_lb.configure(font = ("Helvetica", data))
    
def configure_lang(eventObject) : 
    global cap_lang, transFromlang, transTolang, t1,t2
    
    data = eventObject.widget.get()
    
    target = str(eventObject.widget)
   
    if target == '.!toplevel.!frame.!combobox' :
        cap_lang = data
    elif target == '.!toplevel.!frame.!combobox2':
        transFromlang = data
    else:
        transTolang = data
    
    #threadStop(t1)
    #threadStop(t2)
    #threadStart()
    


def printBoard(self):

    printBoard = tkinter.Toplevel()
    printBoard.wm_geometry("660x400+200+200")
    printBoard.title('printBoard')
    printBoard.resizable(False,True)
    
    #frames
    option_frame = tkinter.Frame(printBoard, relief="solid", bd=1)
    option_frame.pack(side='top', fill='both')
    
    top_frame = tkinter.Frame(printBoard, relief="solid", bd=1)
    top_frame.pack(side='top', fill='both', expand = 'true')
    
    bottom_frame = tkinter.Frame(printBoard, relief="solid", bd=1)
    bottom_frame.pack(side='bottom', fill='both', expand = 'true')
    
    global cb0,cb1,cb2,cb3
    #combobox
    cap_lang_val = ('chi_sim','eng','kor','jpn')
    cbx = tkinter.ttk.Combobox(option_frame,values = cap_lang_val)
    #cbx.pack(side = 'left')
    cbx.set('Image')
    cbx.grid(row = 0, column = 0, sticky = 'W')
    
    lang_val = ('zh-cn ','en','ko','ja')
    cbx1 = tkinter.ttk.Combobox(option_frame,values = lang_val)
    #cbx1.pack(side = 'left')
    cbx1.set('From')
    cbx1.grid(row = 0, column = 1, sticky = 'W')
    
    lang_val = ('zh-cn ','en','ko','ja')
    cbx2 = tkinter.ttk.Combobox(option_frame,values = lang_val)
    #cbx2.pack(side = 'top')
    cbx2.set('To')
    cbx2.grid(row = 0, column = 2, sticky = 'W')
    
    lang_val = (10,12,14,16,18,20)
    cbx3 = tkinter.ttk.Combobox(option_frame,values = lang_val)
    #cbx3.pack(side = 'top')
    cbx3.set('font size')
    cbx3.grid(row = 0, column = 3, sticky = 'W')
    
    cbx.bind("<<ComboboxSelected>>", configure_lang)
    cbx1.bind("<<ComboboxSelected>>", configure_lang)
    cbx2.bind("<<ComboboxSelected>>", configure_lang)
    cbx3.bind("<<ComboboxSelected>>", configure_font)

    #labels
    
    global org_lb,tr_lb
    orgLabel = tkinter.Label(top_frame, text = original_result , font=("Helvetica", 10),wraplength = 650)
    #orgLabel.pack(side = 'bottom')
    org_lb = orgLabel
    orgLabel.grid(row = 0, column = 0, sticky = 'W')
    
    transLabel = tkinter.Label(bottom_frame, text= tr_results , font=("Helvetica", 10), wraplength = 650)
    #transLabel.pack(side='top')
    tr_lb = transLabel
    transLabel.grid(row = 0, column = 0, sticky = 'W')
    
class captureBoard(tkinter.Tk):
    def __init__(self):
        tkinter.Tk.__init__(self)

def main():
    global cb
    cb= captureBoard() 
    cb.title('captureBoard')
    cb.geometry("320x200+100+100")
    cb.resizable(True, True)
    cb.wm_attributes('-alpha', 0.3)

    printBoard(captureBoard)
    threadStart()
    cb.mainloop()
    
if __name__ == '__main__':
    
    multiprocessing.freeze_support()

    main()


# In[ ]:




