#Author: Adeyemo Joel
#Date :  10/31/2023 
#File: Task_frame.py
#Description: 



# Dependencies
import customtkinter
from typing import Optional, Tuple, Union
from PIL import  Image,ImageTk
import os,datetime,json
from icecream import ic
import pandas as pd
import calendar
from tkinter import END, INSERT, PhotoImage



PATH = os.path.dirname(os.path.realpath(__file__))
image_path= os.path.join(PATH,"Icons")

class Task_frame_builder(customtkinter.CTkFrame):
    ''' This class build the task frame with it different buttons such as the
      Task Entry box, Date/ Time box, Reminder box and additional details box
      Commandbox_frame is the frame the scrollable frame hangs unto'''
    
    def __init__(self,master,commandbox_frame):
        super().__init__(master)
        
        self.calendar_icon=self.load_image(light_path=image_path+"/calendarlight-24.png",image_size=(20,20)) #calendicon 10x10
        self.details_icon=self.load_image(light_path=image_path+"/detailslight-24.png",image_size=(20,20))   #detailsicon 10x10
        self.reminder_icon=self.load_image(light_path=image_path+"/reminderlight-24.png",image_size=(20,20)) #remindericon 10x10
        self.repeat_icon=self.load_image(light_path=image_path+"/repeatlight-24.png",image_size=(20,20))     #repeaticon 10x10
        self.star_icon=self.load_image(light_path=image_path+"/starlight-24.png",image_size=(20,20))         #staricon 10x10
        #saveicon 10x10
        
        #Attributes
        self.commandbox_frame=commandbox_frame
        self.toplevel_window=None
        self.starbtnflag= False
        self.adddetails_txt= ''
        self.tasks=[]   # holds all the current tasks into a list
        
        self.commandbox_frame.grid_columnconfigure(0,weight=1)
        self.commandbox_frame.grid_rowconfigure(0,weight=1)
        self.scrollable_checkbox_frame = ScrollableCheckBoxFrame(master=self.commandbox_frame, title='Task to do',command=self.checkbox_event_clicked)
        self.scrollable_checkbox_frame.grid(row=0, column=0,padx=5, pady=(0,0), sticky="nsew")
        
        self.create_widget()
        
    def load_image(self,light_path:Optional[str] = None,dark_path:Optional[str] = None, image_size: Tuple[int, int]=(0,0)):
        light_image = Image.open(light_path) if light_path else None
        dark_image = Image.open(dark_path) if dark_path else None
        return customtkinter.CTkImage(light_image=light_image,dark_image=dark_image,size=image_size)
       
    def create_widget(self):
        
        #2x1 frames
        self.grid_columnconfigure(0,weight=1)
        
        # For entry box and add details
        self.main_frame=customtkinter.CTkFrame(self,corner_radius=2)
        self.main_frame.grid(column=0,row=0,sticky='nsew',padx=(10,10),pady=(10,10))
        
        # For Date time and reminder
        self.aux_frame=customtkinter.CTkFrame(self,corner_radius=2,fg_color='grey30')
        self.aux_frame.grid(column=0,row=1,sticky='nsew',padx=(10,10),pady=(10,10))
        
        # Working on the main_frame
        #self.main_frame.grid_rowconfigure(0,weight=0)
        self.main_frame.grid_columnconfigure(0,weight=1)
        
        msg='Enter a task'
        self.task_entry=customtkinter.CTkEntry(self.main_frame,placeholder_text=msg,corner_radius=5)
        self.task_entry.grid(column=0,row=0,sticky='nsew',padx=10)
        self.task_entry.bind("<Return>",self.savebtnclicked)
        
        self.adddetails_entry=customtkinter.CTkEntry(self.main_frame,placeholder_text='Enter additional details',corner_radius=5,width=30,height=15)
        self.adddetails_entry.grid(column=0,row=1,sticky='nsew',padx=10)
        self.adddetails_entry.grid_remove()
        
        # Working on the aux_frame
        self.aux_frame.grid_columnconfigure((5),weight=1)
        self.aux_frame.grid_columnconfigure((1,2),weight=0)
        self.aux_frame.grid_rowconfigure(0,weight=1)
        
        # Add Calendar button - would have the calendar, reminder, date/time and repeat
        self.calendarbtn=customtkinter.CTkButton(self.aux_frame,fg_color="transparent",corner_radius=4,text="",width=20,height=20,image=self.calendar_icon,command=self.calendarbtnclicked)
        self.calendarbtn.grid(column=0,row=0,pady=5,padx=5,sticky='w')
        
        # Add a three rectangle button
        self.detailsbtn=customtkinter.CTkButton(self.aux_frame,fg_color="transparent",corner_radius=4,text="",width=20,height=20,image=self.details_icon,command=self.adddetailsclicked)
        self.detailsbtn.grid(column=1,row=0,pady=5,padx=5,sticky='w')
        
        # Add a star button 
        self.starbtn=customtkinter.CTkButton(self.aux_frame,fg_color="transparent",corner_radius=4,text="",width=20,height=20,image=self.star_icon,command=self.starbtnclicked)
        self.starbtn.grid(column=3,row=0,pady=5,padx=5,sticky='w')
        
        # Add the Save/Enter Button
        self.savebtn=customtkinter.CTkButton(self.aux_frame,fg_color="transparent",corner_radius=4,text="Add",width=20,height=20,command=self.savebtnclicked)
        self.savebtn.grid(column=5,row=0,pady=10,padx=10,sticky='e')
    
    def savebtnclicked(self,choice):
        ''' The method is responsible for either when the savebtn is clicked or entered in the taskentry box
           The method collects all the the data ie date/time,additional details and starbtn '''
        
        self.adddetails_entry.grid_remove()          # Close the add details entry box
        Task_name=self.task_entry.get()              # Get the task name
        details_txt= self.adddetails_entry.get()     # Get the additional details data
        star_flag= self.starbtnflag                   # Get the star value details
        date_time_entered_rl,reminder = '',''
        
        # Get the calendar data
        if self.toplevel_window !=None:
            datetime_entered =self.toplevel_window.donebtn_clicked()
            date_time_entered_rl= datetime_entered['current_date']+','+datetime_entered['current_time']
            reminder= datetime_entered['Reminder']
    
        new_Tasks=self.add_Task(Task_name,details_txt,date_time_entered_rl,reminder,star_flag)  #Create new Task
        self.add_Task_lst(new_Tasks)             # Add task to list
        ic(self.tasks)
        self.scrollable_checkbox_frame.add_item_frame(new_Tasks)
        self.task_entry.delete('0','end')        #Clear the entry box
        self.adddetails_entry.delete('0','end')  #Clear the add details entry box
    
    def calendarbtnclicked(self):
        ''' The method is responsible for showing a toplevel window with a calendar, time,reminder and repeat'''
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window= CalendarFrame(self) #Create the calendar frame  #create window if its None or destroyed
        else:
            self.toplevel_window.focus()
    
    def adddetailsclicked(self):
        ''' The method is responsible for showing the adddetails box, collecting the details and closing the box'''
        self.adddetails_entry.grid()  #Unlock the entry box grid
        self.adddetails_txt= self.adddetails_entry.get()
    
    def starbtnclicked(self):
        ''' The method changes the color button of the star and then makes the starbutton true'''
        self.starbtnflag=True
    
    def add_Task(self,task_name,more_details,datetime,reminder,starflag,Extra: Optional[str]=None):
        ''' Function at the task with its reminder,date, and any other to a list'''
        task={
            'Task_name': f'{task_name}',
            'Task_Details': f'{more_details}',
            'Date/time':f'{datetime}',
            'Reminder' :f'{reminder}',
            'Star_flag': f'{starflag}'
        }
        return task
    
    def add_Task_lst(self,Task):
        ''' Add the tasks to a compounding list'''
        self.tasks.append(Task)
    
    def remove_Task_lst(self,task_name):
        pass
    
    def add_to_json(self):
        with open(PATH+'/files/saved_entry.json', 'w') as file:
            json.dump(self.tasks, file, indent=4)
    
    def checkbox_event_clicked(self,choice):
        ''' This method deals with when the checkbox in the command frame is clicked. if the checkbox is clicked,
        change remove the command box and remove it from the task list'''
        
        print(f"checkbox frame modified: {self.scrollable_checkbox_frame.get_checked_items()}")
        self.scrollable_checkbox_frame.remove_item_frame(choice)# remove from the scroable frame
        self.remove_Task_lst(choice)# Remove from the task list
            
#-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+ -+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-
class Task_TopLevel(customtkinter.CTkToplevel):
    ''' TopLevel that other class can inherit from to build each of the values'''
    def __init__(self,master,title,width:int|None=None,height:int|None=None,):
        super().__init__(master)
        
        self.title=title
        self.width=width
        self.heigt=height
        self.geometry(f'{self.width}x{self.height}')
        self.protocol("WM_DELETE_WINDOW",self.on_closing)
        
        self.title = customtkinter.CTkLabel(self, text=self.title, fg_color="gray30", corner_radius=6)
        self.title.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="ew")
    
    def on_closing(self):
        self.destroy()
#-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+ -+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-


class CalendarFrame(customtkinter.CTkToplevel):
    '''  The idea for the calendar frame is the  ability to do the following
        - Set time using entry box
        - 
    '''
    WIDTH=300
    HEIGHT=500
    def __init__(self,master,*args, **kwarg):
        super().__init__(master,*args, **kwarg)
        
        self.title("Set Date and Time")
        self.geometry(f'{CalendarFrame.WIDTH}x{CalendarFrame.HEIGHT}')
        self.protocol("WM_DELETE_WINDOW",self.on_closing)
        
        
        self.month_names = {
            1: "Jan",2: "Feb",3: "Mar",
            4: "Apr",5: "May",6: "Jun",
            7: "Jul",8: "Aug",9: "Sep",
            10: "Oct",11: "Nov",12: "Dec"
        }
        
        self.df= pd.DataFrame()
        self.remind_icon= self.load_image(light_path=image_path+'/reminder-24.png',image_size=(15,15))
        current_date= datetime.datetime.now()
        self.curr_day=   current_date.day
        self.curr_month= current_date.month
        self.curr_year=  current_date.year
        self.curr_month_formatted= self.month_names.get(self.curr_month,"invalid")
        self.clicked_date= f'{self.curr_month_formatted} {self.curr_day}, {self.curr_year}'  # The space is very important to the format
        self.curr_time='12 AM'
        self.End_date=''
        self.End_time=''
        self.Reminder=''
        
        # For the buttons
        self.btns=[]
        self.btn_rows=[]  # Each row has an array of cols 
        self.used_btn=[]
    
        #using icecream to print
        ic(type(self.curr_month))
        ic(type(self.curr_year))
        ic(self.curr_month_formatted)
        ic(current_date)
         
        
        self.create_win_elements()
    
    def on_closing(self):
        self.destroy()
    
    def load_image(self,light_path:Optional[str] = None,dark_path:Optional[str] = None, image_size: Tuple[int, int]=(0,0)):
        light_image = Image.open(light_path) if light_path else None
        dark_image = Image.open(dark_path) if dark_path else None
        return customtkinter.CTkImage(light_image=light_image,dark_image=dark_image,size=image_size)

    def create_win_elements(self):
        '''  Idea:
           - Have entry box at the top
           - Have the calendar monthly view down
           - toggle button for end date and timee
           - clear btn
           - Remind drop down menu
        '''
        
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1) 
    
        #------------------------Date Change  Frame----------------------------
        self.entrybox_frame=customtkinter.CTkFrame(self)  # to make transparent
        self.entrybox_frame.grid(column=0,row=1,padx=(20,20),pady=(10,10),sticky='ew')
        
        
        self.Date_entry= customtkinter.CTkEntry(self.entrybox_frame,corner_radius=4,width=CalendarFrame.WIDTH/2)
        self.Date_entry.grid(column=0,row=0,padx=(10,0))
        self.time_entry= customtkinter.CTkEntry(self.entrybox_frame,corner_radius=4,width=CalendarFrame.WIDTH/3)
        self.time_entry.grid(column=1,row=0,padx=(0,10))
        self.enddate_entry= customtkinter.CTkEntry(self.entrybox_frame,corner_radius=4,width=CalendarFrame.WIDTH/3)
        self.enddate_entry.grid(column=1,row=0,padx=(15,10))
        self.enddate_entry.grid_remove()
        
        
        self.Date_entry2= customtkinter.CTkEntry(self.entrybox_frame,corner_radius=4,width=CalendarFrame.WIDTH/2)
        self.Date_entry2.grid(column=0,row=1,padx=(10,0),pady=(5,0))
        self.time_entry2= customtkinter.CTkEntry(self.entrybox_frame,corner_radius=4,width=CalendarFrame.WIDTH/3)
        self.time_entry2.grid(column=1,row=1,padx=(0,10),pady=(5,0))
        
        self.Date_entry2.grid_remove()
        self.time_entry2.grid_remove()
        
        
        self.status_label = customtkinter.CTkLabel(self.entrybox_frame, text="", fg_color="green")
        self.status_label.grid(column=2, row=0, sticky='w')
        
        self.Date_entry.bind("<Return>",self.Date_entry_clicked)
        self.time_entry.bind("<Return>",self.Time_entry_clicked)
        # self.Date_entry.set_status_label()
        
        #------------------------Calendar Frame----------------------------
        self.calable_frame=customtkinter.CTkFrame(self,height=27)  # to make transparent
        self.calable_frame.grid(column=0,row=2,padx=(20,20),pady=(10,10),sticky='ew')
        
        self.calable_frame.grid_columnconfigure((1,2),weight=0)
        self.calable_frame.grid_columnconfigure(0,weight=1)
        
        self.month_label=customtkinter.CTkLabel(self.calable_frame,text="Jan 2077")
        self.month_label.grid(column=0,row=0, padx=20, sticky="w")
        
        self.left_button = customtkinter.CTkButton(self.calable_frame, text="<", width=26, height=26,hover_color="grey70",bg_color="transparent",command=self.leftbtn_clicked)
        self.left_button.grid(column=1,row=0, padx=(3, 0),sticky='w')
        self.right_button = customtkinter.CTkButton(self.calable_frame, text=">", width=26, height=26,hover_color="grey70",bg_color="transparent",command=self.rightbtn_clicked)
        self.right_button.grid(column=2,row=0, padx=(3, 0),sticky='w')
        
        #------------------------Calendar Table  Frame----------------------------
        self.calendartable_frame=customtkinter.CTkFrame(self)  # to make transparent
        self.calendartable_frame.grid(column=0,row=3,rowspan=3,padx=(20,20),pady=(10,10),sticky='ew')
        
        # create the table based on the current year and month
        self.create_calendar_btns(self.curr_year,self.curr_month)
        
        #------------------------Remind Frame----------------------------
        self.remind_frame=customtkinter.CTkFrame(self,height=27)  # to make transparent
        self.remind_frame.grid(column=0,row=6,padx=(20,20),pady=(10,10),sticky='ew')
        
        self.remind_frame.grid_columnconfigure((0,1),weight=0)
        self.remind_frame.grid_columnconfigure(2,weight=1)
        
        self.remindicon_label=customtkinter.CTkLabel(self.remind_frame,text='',bg_color='transparent',width=15,height=15,image=self.remind_icon)
        self.remindicon_label.grid(column=0,row=0, padx=(0,10), sticky="w")
        self.remind_label=customtkinter.CTkLabel(self.remind_frame,text="Remind")
        self.remind_label.grid(column=1,row=0, padx=(0,10), sticky="w")
        
        options=['None','1 day before(9am)','2 day before(9am)','1 week before(9am)']
        self.optionmenu=customtkinter.CTkOptionMenu(self.remind_frame,values=options, width=CalendarFrame.WIDTH/8,bg_color='transparent')
        self.optionmenu.grid(column=3,row=0,pady=10,sticky='e')
        
        
        #------------------------Enddate  time  Frame----------------------------
        self.endatetime_frame=customtkinter.CTkFrame(self,height=27)  # to make transparent
        self.endatetime_frame.grid(column=0,row=7,padx=(20,20),pady=(10,10),sticky='ew')
        
        self.endatetime_frame.grid_columnconfigure(0,weight=0)
        self.endatetime_frame.grid_columnconfigure((1,2),weight=1)
        self.endatetime_frame.grid_rowconfigure((0,1),weight=1)
        
        self.enddate_label=customtkinter.CTkLabel(self.endatetime_frame,text="End date")
        self.enddate_label.grid(column=0,row=0, padx=(0,10), sticky="w")
        
        switch_var = customtkinter.StringVar(value='off')
        self.enddate_switch= customtkinter.CTkSwitch(self.endatetime_frame,variable=switch_var,onvalue='on',offvalue='off',text="",width=2,command=self.enddate_switch_event)
        self.enddate_switch.grid(column=3,row=0, padx=(0,10), sticky="e")
        self.enddate_switch_event()
        
        self.includetime_label=customtkinter.CTkLabel(self.endatetime_frame,text="Include time")
        self.includetime_label.grid(column=0,row=1, padx=(0,10), sticky="w")
        
        switch_var2= customtkinter.StringVar(value='off')
        self.time_switch= customtkinter.CTkSwitch(self.endatetime_frame,variable=switch_var2,onvalue='on',offvalue='off',text="",width=2,command=self.time_switch_event)
        self.time_switch.grid(column=3,row=1, padx=(0,10), sticky="e")
        self.time_switch_event()
        
        #------------------------Clear Frame----------------------------
        self.clear_frame=customtkinter.CTkFrame(self,height=27)  # to make transparent
        self.clear_frame.grid(column=0,row=8,padx=(20,20),pady=(10,10),sticky='ew')
        
        self.clear_frame.grid_columnconfigure((0,1),weight=0)
        self.clear_frame.grid_columnconfigure((2,3),weight=1)
        self.clear_frame.grid_rowconfigure(0,weight=1)
        
        self.cancel_btn=customtkinter.CTkButton(self.clear_frame,text="Cancel",bg_color="transparent")
        self.cancel_btn.grid(column=2,row=0, padx=(0,10), sticky="w")
        
        self.done_btn=customtkinter.CTkButton(self.clear_frame,text="Done",bg_color="transparent",command=self.donebtn_clicked)
        self.done_btn.grid(column=3,row=0, padx=(0,10), sticky="w")
    
    def Date_entry_clicked(self,choice):
        ''' It is very space sensitive so becareful when entrying the value'''
        self.on_validate_date_format(self.Date_entry.get())    #validate the string
        results=self.get_match_elements(self.Date_entry.get()) #get the elements ie month and Year
        
        # plot the calendar table 
        print(type(results["Year"]),results["Month"])
        self.create_calendar_btns(int(results["Year"]),int(results["Month"]))
    
    def Time_entry_clicked(self,choice):
        ic('Time enter clicked ')
        ic(self.time_entry.get())
        valid =self.on_validate_time_format(self.time_entry.get()) # validate the string entered
        if valid:
            ic('pass')#Add to database for the particular day
            self.curr_time=self.time_entry.get()
        else:
            ic('failed')
            pass
    
    def time_switch_event(self):
        if(self.time_switch.get()=='off'):
            self.time_entry.delete(0,END)   # clear the data in the entry box
            self.time_entry.configure(state='disabled') #disable the time entry box
            self.Date_entry2.grid_remove()
            self.time_entry2.grid_remove()
        else:
            if(self.enddate_switch.get()=='on'):  #If both time and end date is on
                self.Date_entry2.grid()
                self.time_entry2.grid()
                self.time_entry2.delete(0,END)     # clear the data in the entry box
                self.time_entry2.insert(0,"12 AM") # print the 12am in the entry box
                self.Date_entry2.delete(0,END)   # Clear the data in the box
                self.Date_entry2.insert(0, f'{self.curr_month_formatted} {self.curr_day}, {self.curr_year}')
            else:
                self.time_entry.configure(state='normal')   #enable the time entry box
                self.time_entry.delete(0,END)     # clear the data in the entry box
                self.time_entry.insert(0,"12 AM") # print the 12am in the entry box
    
    def enddate_switch_event(self):
        ''' This callback function occurs when the end date switch is turned on
        First it creates a different entry box, if off disable and make the box dissappers, and add to end date list'''
        
        # self.enddate_entry= customtkinter.CTkEntry(self.entrybox_frame,corner_radius=4,width=CalendarFrame.WIDTH/4)
        # self.enddate_entry.grid(column=1,row=0,padx=(15,10))
        
        if(self.enddate_switch.get()=='off'):
            self.enddate_entry.grid_remove()
            self.Date_entry2.grid_remove()
            self.time_entry2.grid_remove()
            self.enddate_entry.delete(0,END)   # clear the data in the entry box
            self.enddate_entry.configure(state='disabled')  #disable the enddate entry box
            
        else:
            self.enddate_entry.grid()
            self.enddate_entry.configure(state='normal')   #enable the time entry box
            self.enddate_entry.delete(0,END)   # Clear the data in the box
            self.enddate_entry.insert(0, f'{self.curr_month_formatted} {self.curr_day}, {self.curr_year}')
            #self.enddate_entry.grid(column=1,row=0,padx=(15,10))
                    
    def get_match_elements(self,input_text):
        date_pattern= r'^(?P<month>Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) (?P<day>\d{1,2}), (?P<year>\d{4})$'
        match=re.match(date_pattern,str(input_text))
        month_map={"Jan":1,"Feb":2,
                   "Mar":3,"Apr":4,
                   "May":5,"Jun":6,
                   "Jul":7,"Aug":8,
                   "Sep":9,"Oct":10,
                   "Nov":11,"Dec":12}
        res={ 'Month': f'{month_map[match.group("month")]}',
               'Day' : f'{match.group("day")}',
               'Year':f'{match.group("year")}'
        }
        return res
    
    def validate_date_format(self,input_text):
        date_pattern= r'^\b(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) (\d{1,2}), (\d{4})$'
        print(input_text)
        return bool(re.match(date_pattern,str(input_text)))
    
    def on_validate_date_format(self, new_text):
        if self.validate_date_format(new_text):
            if self.status_label:
                self.status_label.configure(text="Valid date format", fg_color="green")
            return True
        else:
            if self.status_label:
                self.status_label.configure(text="Invalid date format", fg_color="red")
                self.Date_entry.configure(placeholder_text='Not right format Jan 4, 2077',fg_color='red')
            return False   
    
    def validate_time_format(self,input_time):
        time_pattern=r"^(\d{1,2}(:\d{2})?)(\s?)([apAp][mM])$"
        return bool(re.match(time_pattern,str(input_time)))
    
    def on_validate_time_format(self,new_txt):
        if self.validate_time_format(new_txt):
            if self.status_label:
                self.status_label.configure(text="Valid date format", fg_color="green")
            return True
        else:
            if self.status_label:
                self.status_label.configure(text="Invalid date format", fg_color="red")
                self.Date_entry.configure(placeholder_text='Can be 12am or 12 am or 12:30 am',fg_color='red')
            return False      
    
    def leftbtn_clicked(self):
        '''Moves the calendar backwards to the next month'''
        self.curr_month= self.curr_month-1
        if self.curr_month != 0:  #if when haven't reached december
            self.create_calendar_btns(self.curr_year,self.curr_month)    #move  backwards
        else:
            self.curr_year= self.curr_year-1
            self.curr_month=12
            self.create_calendar_btns(self.curr_year,self.curr_month)   #change the year
    
    def rightbtn_clicked(self):
        '''Moves the calendar forward to the next month'''
        self.curr_month = self.curr_month+1
        if self.curr_month !=13:  #if when haven't reached december
            ic(self.curr_month)
            ic(self.curr_year)
            self.create_calendar_btns(self.curr_year,self.curr_month)    #move forward
        else:
            self.curr_year= self.curr_year+1
            self.curr_month=1
            self.create_calendar_btns(self.curr_year,self.curr_month)   #change the year
    
    def change_year_month_label(self,year,month):
        #change the Label on the next row
        self.curr_year,self.curr_month=year,month
        self.curr_month_formatted= self.month_names[self.curr_month]
        self.month_label.configure(text=f'{self.curr_month_formatted} {self.curr_year}')    #change the Label on the next row
        return 
        
    def create_calendar_btns(self,year,month):
        self.change_year_month_label(year,month)  #Format the Label on the next row
        cal=calendar.monthcalendar(year, month)
        n_rows=len(cal)
        n_cols=len(cal[0])
        #btns=[]
        self.btns.clear()
        
        for row in range(n_rows):
            btn_rows=[]  # Each row has an array of cols 
            for col in range(n_cols):
                day=cal[row][col]
                if day==0:
                    label=''
                else:
                    label= str(day)
                button =customtkinter.CTkButton(self.calendartable_frame,text=label,width=15,fg_color="transparent",hover_color="blue",command=lambda txt=label,row= row,col=col: self.day_btn_clicked(txt,row,col))
                btn_rows.append(button)
                button.grid(column=col,row=row,padx=2,pady=2)
            self.btns.append(btn_rows) 
    
    def day_btn_clicked(self,day:str,row,col):
        # Get the date, year and month and print on the
        if self.used_btn:
           self.used_btn[-1].configure(fg_color='transparent') # if available
        ic(day)
        ic(row,col)
        self.btns[row][col].configure(fg_color='blue')
        self.used_btn.append(self.btns[row][col])
        
        #Add the date - month and Year together
        self.curr_day= day
        self.clicked_date= f'{self.curr_month_formatted} {self.curr_day}, {self.curr_year}'
        self.Date_entry.delete(0,END)
        self.Date_entry.insert(0,f'{self.clicked_date}')
    
    def donebtn_clicked(self):
        ''' The task name is entered from the other class to help when saving'''
        ic('Done btn Clicked')
        self.destroy()
        data={
            "current_date":f'{self.clicked_date}',
            "current_day":f'{self.curr_day}',
            "current_month":f'{self.curr_month}',
            "current_year":f'{self.curr_year}',
            "current_time":f'{self.curr_time}',
            "End_date": f'{self.End_date}',
            "End_time":f'{self.End_time}',
            "Reminder":f'{self.Reminder}'
        }
        #self.df.append(data)
        return data
#-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+ -+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-

class ScrollableCheckBoxFrame(customtkinter.CTkScrollableFrame):
    
    def __init__(self, master,title,command=None,btn_command=None, **kwargs):     
        """ The scrollable frame collects all the input data,stores it and stores the list
        """
        super().__init__(master, **kwargs,label_text=title)
        
        self.grid_columnconfigure(0, weight=1)
        
        self.command = command
        self.btn_command=btn_command
        self.item_frame_list={}
        self.checkbox_list = []
        self.checkbox_done=[]
    
    def add_item(self,item):
        checkbox=customtkinter.CTkCheckBox(self,text=item)
        if self.command is not None:
            checkbox.configure(command=lambda: self.command(item))
        checkbox.grid(row=len(self.checkbox_list), column=0, pady=(0, 10),sticky='w')
        self.checkbox_list.append(checkbox)
    
    def add_item_frame(self,item_name,additional_details=" ",time_date_details=" "):
        ''' Adds a checkbox, label and a button on frame to be addedd to the checkboxFrame'''
        item_frame=customtkinter.CTkFrame(self,height=50)
        item_frame.grid(row=len(self.checkbox_list),column=0,pady=(0,0),sticky='nsew')
        
        #self.item_frame.grid_rowconfigure((0,1,2),weight=1)
        item_frame.grid_columnconfigure(0,weight=1)
        
        # Add the checkbox
        item_checkbox=customtkinter.CTkCheckBox(item_frame,text=item_name)
        if self.command is not None:
            item_checkbox.configure(command=lambda: self.command(item_name))
        item_checkbox.grid(row=0,column=0,pady=(0, 5),sticky='w')
        self.checkbox_list.append(item_checkbox)#append to the checkbox list
        
        #Add the additional detail
        add_details_label=customtkinter.CTkLabel(item_frame,text=additional_details,bg_color='transparent')
        if additional_details is None:
           add_details_label.configure(state='disabled') # make the state of the label 
        add_details_label.grid(row=1,column=0,padx=(30,0),pady=(0, 5),sticky='w')
        
        #Add the button for the date and time
        datetime_btn=customtkinter.CTkButton(item_frame,width=30,bg_color='transparent',text= "Add date/time",fg_color="transparent")
        if time_date_details =='':
            datetime_btn.configure(state='disabled')
        else:
           datetime_btn.configure(command=lambda: self.btn_command(item_name),text=f'{time_date_details}')
        datetime_btn.grid(row=2,column=0,padx=(30,0),pady=(0,5),sticky='w')
        
        self.item_frame_list[f'{item_checkbox.cget("text")}']=item_frame
        
        return
    
    def add_item_frame(self,new_task):
        ''' Add a task Type to the Frame
        - Needed: Task Name with checkbox,Another line for the details,edit btns'''
        
        item_frame=customtkinter.CTkFrame(self,height=30)
        item_frame.grid(row=len(self.checkbox_list),column=0,pady=(0,0),sticky='nsew')
        
        item_frame.grid_columnconfigure(0,weight=1)
        
        # Add the checkbox
        item_checkbox=customtkinter.CTkCheckBox(item_frame,text=new_task['Task_name'])
        if self.command is not None:
            item_checkbox.configure(command=lambda: self.command(new_task['Task_name']))  # should just change it to new_task***
        item_checkbox.grid(row=0,column=0,pady=(0, 5),sticky='w')
        self.checkbox_list.append(item_checkbox)       #append to the checkbox list
        
        #Add the additional detail
        add_details_label=customtkinter.CTkLabel(item_frame,text=new_task['Task_Details'], bg_color='transparent')
        if new_task['Task_Details'] is None:
           add_details_label.configure(state='disabled') # make the state of the label 
        add_details_label.grid(row=1,column=0,padx=(30,0),pady=(0, 5),sticky='w')
        
        #Add the button for the date and time
        datetime_label= customtkinter.CTkLabel(item_frame,width=25,fg_color='transparent')
        reminder_label= customtkinter.CTkLabel(item_frame,width=25,fg_color='transparent')
        
        if new_task['Date/time'] == '':
            datetime_label.configure(text='')
        else:
            datetime_label.configure(text=new_task['Date/time'])
            
        if new_task['Reminder']== '':
           reminder_label.configure(text='')
        else:
            reminder_label.configure(text=new_task['Reminder'])
            
        datetime_label.grid(row=2,column=0,padx=(30,0),pady=(0,5),sticky='w')
        reminder_label.grid(row=2,column=1,padx=(30,0),pady=(0,5),sticky='w')
        
        self.item_frame_list[f'{item_checkbox.cget("text")}']= item_frame
    
    def remove_item(self, item):
        for checkbox in self.checkbox_list:
            if item == checkbox.cget("text"):
                checkbox.destroy()
                self.checkbox_list.remove(checkbox)
                self.checkbox_done.append(checkbox)
                return
    
    def remove_item_frame(self, item):
        ''' Item is the task_name'''
        for checkbox in self.checkbox_list:
            if item == checkbox.cget("text"):
                if item in self.item_frame_list:
                    item_frame= self.item_frame_list[f'{item}']
                    checkbox.destroy()
                    item_frame.destroy()
                value = self.item_frame_list.pop(f'{checkbox}', None)  # None is the default value
                self.checkbox_list.remove(checkbox)
                self.checkbox_done.append(checkbox)
                return
    
    def get_checked_items(self):
        checkedboxs=[]
        return [checkbox.cget("text") for checkbox in self.checkbox_list if checkbox.get() == 1]
#-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+ -+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-           
       
       