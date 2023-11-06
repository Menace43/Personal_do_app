

import re
from icecream import ic
import customtkinter
import sys

sys.path.insert(0, '/Users/joel/Projects/sideprojects/Personal_Todo_App/')
from Task_frame import *

class Classic_Tests:
    
    def validate_date_format(self,input_text):
        date_pattern= r'^\b(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) (\d{1,2}), (\d{4})$'
        print(input_text)
        return bool(re.match(date_pattern,str(input_text)))
    
    def validate_time_format(self,input_time):
        time_pattern=r"^(\d{1,2}(:\d{2})?)(\s?)([apAp][mM])$"
        print(input_time)
        return bool(re.match(time_pattern,str(input_time)))
    
    def clicked_on(self):
        myvals=Send_value()
        res=myvals.send_value("present")
        return res

class Send_value():
    def send_value(self,new_res):
        res={
            "Value1":"1",
            "new_value":f'{new_res}'
        }
        return res

# if __name__ =="__main__":
#     Tests=Classic_Tests()
#     #print(Tests.validate_time_format("12:00 AM"))
#     ic(Tests.clicked_on())


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("my app")
        self.geometry("400x180")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.checkbox_frame = Task_frame_builder(self)
        self.checkbox_frame.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="nswe")


if __name__ =="__main__":
    app = App()
    app.mainloop()
