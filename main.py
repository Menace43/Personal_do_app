
#Author: Adeyemo Joel
#Description:  Design a personal todo list app that can not be tracked by  google or even apple and easy to use
 # App inspiration is  gotten from Apple's Calendar, Google Task anad Any.do
#File: Main.py
#Date:8/23/2022

#Important Features
# --> Adding/Deleting Task
# --> Storing  Task in Json file
# --> Calendar Clicking on the 
# --> 


#Dependencies
import customtkinter


# User defined Dependencies
from Application import *




def main():
    
    #Create an Object for the GUI
    customtkinter.set_appearance_mode("Dark")      # Modes: "System ","Dark","Light"
    customtkinter.set_default_color_theme("blue")  # Themes:"Blue"(standard),"green","dark-blue"
    app=App()
    app.mainloop()

    
    
    

if __name__ =='__main__':
    main()
