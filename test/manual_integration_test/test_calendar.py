

import re

class Classic_Tests:
    
    def validate_date_format(self,input_text):
        date_pattern= r'^\b(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) (\d{1,2}), (\d{4})$'
        print(input_text)
        return bool(re.match(date_pattern,str(input_text)))
    
    def validate_time_format(self,input_time):
        time_pattern=r"^(\d{1,2}(:\d{2})?)(\s?)([apAp][mM])$"
        print(input_time)
        return bool(re.match(time_pattern,str(input_time)))

if __name__ =="__main__":
    Tests=Classic_Tests()
    print(Tests.validate_time_format("12:30 AM"))