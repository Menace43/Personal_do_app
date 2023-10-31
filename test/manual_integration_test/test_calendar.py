

import re
from icecream import ic

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

if __name__ =="__main__":
    Tests=Classic_Tests()
    #print(Tests.validate_time_format("12:00 AM"))
    ic(Tests.clicked_on())