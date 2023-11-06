
#Author: Adeyemo Joel
#Description:  Design a personal todo list app that can not be tracked by  google or even apple and easy to use
 # App inspiration is  gotten from Apple's Calendar, Google Task anad Any.do
#File:Application.py
#Date:8/23/2022

__version__='1.1.0'

#Front_end Dependencies
import calendar
from tkinter import END, INSERT, PhotoImage
import customtkinter
from PIL import  Image,ImageTk
import PIL.Image
import tkinter as tk
import queue,datetime
from tkinter import messagebox

#Back-end Dependencies
import os
from typing import Optional, Tuple
import re
import pandas as pd
from icecream import ic
import json

#user Defined Dependencies
from Task_frame import *


PATH = os.path.dirname(os.path.realpath(__file__))
image_path= os.path.join(PATH,"Icons")

class App(customtkinter.CTk):
    HEIGHT= 900
    WIDTH= 1200
    Left_frame_width=50
    def __init__(self, *args, fg_color="default_theme", **kwargs):
        super().__init__() 
        
        # Customize the Layout
        self.title("To do List App")
        self.geometry(f'{App.WIDTH}x{App.HEIGHT}')
        self.protocol("WM_DELETE_WINDOW",self.on_closing)
        
        # Load images
        self.enter_icon= self.load_image(light_path=image_path+'/Send-30.png',image_size=(30,30))                  # [1] in links.txt
        self.calendar_icon=self.load_image(light_path=image_path+"/calendar-30.png",image_size=(30,30))            # [2] in links.txt
        self.details_icon=self.load_image(light_path=image_path+"/details-30.png",image_size=(30,30))              # [3] in links.txt
        self.star_icon=self.load_image(light_path=image_path+"/star-30.png",image_size=(30,30))                    # [4] in links.txt
        
        # Making sure that the toplevel window isnt duplicated
        self.toplevel_window=None
        self.tasks=[]
                            
        # Create a queue
        self.que=queue.Queue()
        
        #Design the App GUI 
        self.create_app()
    #-------------------------------------------------------------------------
    def on_closing(self,events=0):
        '''When the Window is closed'''
        print("destroyed")
        self.destroy()
    #----------------------------------------------------------------------------
    def change_apperance_mode(self,selected):
        ''' # Change the apperance of the  App ie either Dark mode or light mode'''
        customtkinter.set_appearance_mode(selected)
    #-----------------------------------------------------------------------------
    def load_image(self,light_path:Optional[str] = None,dark_path:Optional[str] = None, image_size: Tuple[int, int]=(0,0)):
        light_image = Image.open(light_path) if light_path else None
        dark_image = Image.open(dark_path) if dark_path else None
        return customtkinter.CTkImage(light_image=light_image,dark_image=dark_image,size=image_size)
    #----------------------------------------------------------------------------
    def add_to_commandbox(self):
        ''' # Add what Ever is in the queue to the command box'''
        inside= []            # List that holds the current values
        lz_que=queue.Queue()   # Create a new Queue
        
        # Put the current task into a new queue
        for i_x in self.que.queue:
            lz_que.put(i_x)
        
        #Print the Queue  on the Combo box
        for i_y in range(0,len(lz_que.queue)):
            inside.append(lz_que.get()) 
                                
        self.commandbox.delete("0",END)                                                                                                                                                                                                                                                                
        #Add to the Command box
        for x in range(0,len(inside)):
            instr=f'{x}:{inside[x]}'+'\n'
            self.commandbox.insert(x,instr)
            #self.commandbox.tag_add("here","1.0",END)
        return
    #--------------------------------------------------------------------------------------    
    def savebtn_clicked(self,choice):
        
        # Get the various elements such as Name, additional details and 
        text_entered=self.task_entry.get() 
        detail_text_entered=self.adddetails_entry.get()
        self.date_time_entered_rl=''
        if self.toplevel_window !=None:
            datetime_entered =self.toplevel_window.donebtn_clicked(text_entered)
            self.date_time_entered_rl= datetime_entered['current_date']+','+datetime_entered['current_time']
        
        self.adddetails_entry.grid_remove() # Close the box
        self.scrollable_checkbox_frame.add_item_frame(text_entered,additional_details=detail_text_entered, time_date_details=self.date_time_entered_rl)
        self.add_task_lst(text_entered,detail_text_entered,self.date_time_entered_rl)
        self.task_entry.delete("0",'end')
        self.adddetails_entry.delete(0,END)
    #---------------------------------------------------------------------------------------- 
    def add_task_lst(self,task_name,more_details,datetime_reminder):
        ''' Function at the task with its reminder,date, and any other to a list'''
        task={
            'task_name': f'{task_name}',
            'Extra Details': f'{more_details}',
            'Date/time':f'{datetime_reminder}'
        }
        self.tasks.append(task)
        self.save_and_exist()
    #---------------------------------------------------------------------------------------- 
    def save_and_exist(self):
        with open(PATH+'/files/saved_entry.json', 'w') as file:
            json.dump(self.tasks, file, indent=4)
    #---------------------------------------------------------------------------------------- 
    def detailbtnclicked(self):
        ''' Add more details to the current task'''
        self.adddetails_entry.grid()  #Unlock the entry box grid
        self.adddetails_entry.bind("<Return>",self.savebtn_clicked)
    #---------------------------------------------------------------------------------------- 
    def detailbtnentered(self):
        detail_text_entered=self.adddetails_entry.get()
        self.adddetails_entry.grid_remove() # Close the box
        self.adddetails_entry.delete(0,END)
    #----------------------------------------------------------------------------------------     
    def calendarbtn_clicked(self):
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window= CalendarFrame(self) #Create the calendar frame  #create window if its None or destroyed
        else:
            self.toplevel_window.focus()
    #----------------------------------------------------------------------------------------  
    def starbtn_clicked(self):
        pass
    #----------------------------------------------------------------------------------------    
    def create_toplevel(self):
        #Create the Frame
        self.superframe=customtkinter.CTkFrame(self.new_root,corner_radius=0)
        self.superframe.grid(column=0,row=0,sticky='nsew')
        
        # Configure the frame
        #configure grid layout (1x11) 1 column 11 rows
        self.superframe.grid_rowconfigure(0,minsize=10)   # empty row with minsize as spacing
        self.superframe.grid_rowconfigure(5,weight=1)
        self.superframe.grid_rowconfigure(8,minsize=20)
        self.superframe.grid_rowconfigure(11,minsize=10)
        
        # self.trainglebtn=customtkinter.CTkButton(self.superframe,fg_color="gray40",corner_radius=10,text="",width=20,image=self.threedot_icon)
        # self.trainglebtn.grid(column=0,row=0,pady=10,padx=10,sticky='w')
        
        # # Add a Calendar button 
        # self.calendarbtn=customtkinter.CTkButton(self.Entry_overlay,fg_color="gray40",corner_radius=10,text="",width=40,image= self.calendar_icon,command=self.calendarbtn_clicked)
        # self.calendarbtn.grid(column=1,row=0,pady=10,padx=10,sticky='w')
    #----------------------------------------------------------------------------------------  
    def Calendar_btn_clicked(self):
        datetime=calendar.calendar(2022)
        print(datetime)
    #----------------------------------------------------------------------------------------     
    def checkbox_frame_event(self,choice):
        print(f"checkbox frame modified: {self.scrollable_checkbox_frame.get_checked_items()}")
        self.scrollable_checkbox_frame.remove_item2(choice)
    #-----------------------------------------------------------------------------------------   
    def create_app(self):
        #Implement Two frame system
        # Configure grid layout [2x1] ie 2 columns [0,1] and  1 row[0]
        self.grid_columnconfigure(1,weight=1)
        self.grid_rowconfigure(0,weight=1)
        
        #===========Creating the Two Frames==============================
        self.left_frame=customtkinter.CTkFrame(self,corner_radius=0,width=App.Left_frame_width)
        self.left_frame.grid(column=0,row=0,sticky='nsew')
        
        self.right_frame=customtkinter.CTkFrame(self)
        self.right_frame.grid(column=1,row=0,sticky='nsew',padx=20,pady=20)
        
        #============Working on the Left Frame=============================
        
        #configure grid layout (1x11) 1 column 11 rows
        self.left_frame.grid_rowconfigure(0,minsize=10)   # empty row with minsize as spacing
        self.left_frame.grid_rowconfigure(5,weight=1)
        self.left_frame.grid_rowconfigure(8,minsize=20)
        self.left_frame.grid_rowconfigure(11,minsize=10)
        
        
        #Add Profile Button
        self.profilebutton=customtkinter.CTkButton(self.left_frame,width=App.Left_frame_width,fg_color="gray40",corner_radius=10,text="")
        self.profilebutton.grid(column=0,row=1,pady=10,padx=10,sticky='w')
        
        # Add option Menu to change the Apperance  of the system
        self.optionmenu=customtkinter.CTkOptionMenu(self.left_frame,values=['Light','Dark','System'],width=App.Left_frame_width,command=self.change_apperance_mode)
        self.optionmenu.grid(column=0,row=10,pady=10,sticky='w')
       
       
        #============Working on the Right Frame====================================
       
        # Create two Frames one for the calendar and the other for the to do list Entry
        self.right_frame.grid_columnconfigure((0,1),weight=1)
        self.right_frame.grid_rowconfigure(1,weight=1)
        
        #===========Creating the Frames==============================
        self.task_frame=customtkinter.CTkFrame(self.right_frame,width=250)
        self.task_frame.grid(column=0,row=1,sticky='nsew',padx=20,pady=20)
       
        self.calendar_frame=customtkinter.CTkFrame(self.right_frame,width=250)
        self.calendar_frame.grid(column=1,row=1,sticky='nsew',padx=20,pady=20)
        
        #============Working on the task Frame====================================
        
        # # 3 column by 7 rows
        # self.task_frame.grid_columnconfigure((0,1,2),weight=1)
        # self.task_frame.grid_rowconfigure((0,1,2,3,4,5),weight=1)
        
        # # Create a frame for the Entry box, and overlays
        # self.Entry_overlay=customtkinter.CTkFrame(self.task_frame,corner_radius=4)
        # self.Entry_overlay.grid(column=0,row=7,columnspan=3,sticky='nsew')
        
        # # Create a frame for the Entry box, and overlays
        # self.commandbox_frame=customtkinter.CTkFrame(self.task_frame,corner_radius=2)
        # self.commandbox_frame.grid(column=0,row=2,columnspan=3,rowspan=4,sticky='nsew',pady=10,padx=10)
        
        
        self.task_frame.grid_columnconfigure(0,weight=1)
        self.task_frame.grid_rowconfigure((2,3),weight=1)
        
        self.commandbox_frame =customtkinter.CTkFrame(self.task_frame,corner_radius=4)
        self.commandbox_frame.grid(column=0,row=2,rowspan=2,padx=(10,10),pady=(10,10),sticky='nsew')
        
        self.Entry_overlay =customtkinter.CTkFrame(self.task_frame,corner_radius=4)
        self.Entry_overlay.grid(column=0,row=5,padx=(10,10),pady=(10,10),sticky='nsew')
        
        #---------------Working on Entry_overlay -----------------------------------------
        # 2 columns 2  rows
        self.Entry_overlay.grid_columnconfigure(0,weight=1)
        self.commandbox_frame.grid_columnconfigure(0,weight=1)
        
        # Call the Task Frame that has all the value
        self.Task_frame= Task_frame_builder(self.Entry_overlay,self.commandbox_frame)
        self.Task_frame.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="nswe")
        
        #--------------------Working on the commandbox_frame----------------------------------------------
        # self.commandbox_frame.grid_columnconfigure(0,weight=1)
        # self.commandbox_frame.grid_rowconfigure(0,weight=1)
        
        # self.scrollable_checkbox_frame = ScrollableCheckBoxFrame(master=self.commandbox_frame, title='Task to do',command=self.checkbox_frame_event,btn_command=self.calendarbtn_clicked)
        # self.scrollable_checkbox_frame.grid(row=0, column=0,padx=5, pady=(0,0), sticky="nsew")
        # self.scrollable_checkbox_frame.add_item_frame("new item")
        
        # self.commandbox= tk.Listbox(self.commandbox_frame,width=25)
        # self.commandbox.pack(fill='both',expand=1)
        
        #============Working on the Calendar Frame ====================================
        
        # 3 column by 7 rows
        self.calendar_frame.grid_columnconfigure((0,1,2),weight=1)
        self.calendar_frame.grid_rowconfigure((0,1,2,3,4,5),weight=1)   
        
        # Create a frame for the Entry box, and overlays
        self.caltophalf_frame=customtkinter.CTkFrame(self.calendar_frame,corner_radius=0)
        self.caltophalf_frame.grid(column=0,row=2,columnspan=3,rowspan=4,sticky='nsew',pady=10,padx=10)
        
        # Create a frame for the Entry box, and overlays
        self.calbothalf_frame=customtkinter.CTkFrame(self.calendar_frame,corner_radius=0)
        self.calbothalf_frame.grid(column=0,row=7,columnspan=3,sticky='nsew')
        
        self.moveButton_frame=customtkinter.CTkFrame(self.calendar_frame,corner_radius=0)
        self.moveButton_frame.grid(column=3,row=1,sticky='e')
        
       
        # Working on Tophalf Frame
        self.tab_view = MyTabview(master=self.caltophalf_frame)
        self.tab_view.pack(fill="both",expand=1,pady=10)
        #self.tab_view.grid(row=0, column=0, padx=20, pady=20)
        
        # Working on MoveButton Frame
        self.moveButton_frame.grid_columnconfigure((0,1,2),weight=1)
        self.moveButton_frame.grid_rowconfigure((0),weight=1)
        
        self.move_left=customtkinter.CTkButton(self.moveButton_frame,border_color="grey",width=20,text="<")
        self.move_left.grid(column=0,row=0,sticky='nsew')
        
        self.move_center=customtkinter.CTkButton(self.moveButton_frame,border_color="grey",width=40,text="Today")
        self.move_center.grid(column=1,row=0,sticky='nsew')
        
        self.move_right=customtkinter.CTkButton(self.moveButton_frame,border_color="grey",width=20,text=">")
        self.move_left.grid(column=2,row=0,sticky='nsew')
    
        
        self.Calendar_btn_clicked()
        
            
class MyTabview(customtkinter.CTkTabview):
    def __init__(self,master,**kwargs):
        super().__init__(master,**kwargs)
        self.create_tabs()
        
    def add_tab(self,tab_name):
        self.add(tab_name)
    
    def create_tabs(self):
        # Add All the possible tabs
        self.add("Day")
        self.add("Week")
        self.add("Month")
        self.add("Year")
        
        # self.tab("Tab 1").grid_columnconfigure(0, weight=1)  # configure grid of individual tabs
        # self.tab("Tab 2").grid_columnconfigure(0, weight=1)
        # self.tab("Tab 3").grid_columnconfigure(0, weight=1)
        
        
  
       
       
       
       
        
        
        
    


