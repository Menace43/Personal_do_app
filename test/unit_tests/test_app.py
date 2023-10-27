
import customtkinter
import unittest
#import Application as AppClass
import sys

sys.path.insert(0, '/Users/joel/Projects/sideprojects/Personal_Todo_App/')
import Application as AppClass

class test_App(unittest.TestCase):
    def setUp(self):
        self.root=AppClass.App()
        
    def clean(self):
        self.root.quit()
        self.root.destroy()
        
    def main(self):
        self.execute_tasks()
        self.root.mainloop()
    
    def execute_tasks(self):
        print('\n Test App() started')
        
        start_time=0
        self.root.after(start_time,self.test_title)
        start_time += 300
        self.root.after(start_time, self.clean)

    def test_title(self):
        print('\n Testing Title',end='')
        
        title= self.root.title()
        expected="To do List App"
        #assert title==expected
        self.assertEqual(title, expected, "Title does not match")
        print("successful")
        
        
        


if __name__ == "__main__":
    unittest.main()
    