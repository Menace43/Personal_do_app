
# import tkinter as tk
# import calendar

# class Calendar:
#     def __init__(self, parent):
#         self.parent = parent
#         self.cal = calendar.Calendar()
#         self.year = 2023
#         self.month = 4

#         self.create_widgets()

#     def create_widgets(self):
#         # Create the grid of labels for the calendar
#         days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
#         for i, day in enumerate(days):
#             label = tk.Label(self.parent, text=day)
#             label.grid(row=0, column=i)

#         for week_num, week in enumerate(self.cal.monthdatescalendar(self.year, self.month)):
#             for day_num, day in enumerate(week):
#                 if day.month == self.month:
#                     label = tk.Label(self.parent, text=day.day)
#                     label.grid(row=week_num+1, column=day_num)

#         # Create buttons to navigate between months and years
#         prev_month_button = tk.Button(self.parent, text='<<', command=self.prev_month)
#         prev_month_button.grid(row=6, column=0)

#         next_month_button = tk.Button(self.parent, text='>>', command=self.next_month)
#         next_month_button.grid(row=6, column=6)

#     def prev_month(self):
#         if self.month == 1:
#             self.month = 12
#             self.year -= 1
#         else:
#             self.month -= 1

#         self.update_calendar()

#     def next_month(self):
#         if self.month == 12:
#             self.month = 1
#             self.year += 1
#         else:
#             self.month += 1

#         self.update_calendar()

#     def update_calendar(self):
#         for widget in self.parent.winfo_children():
#             widget.destroy()

#         self.create_widgets()

# # Create the root window and the Calendar widget
# root = tk.Tk()
# calendar_widget = Calendar(root)

# # Run the GUI loop
# root.mainloop()


# import tkinter as tk
# import calendar

# class CalendarGUI:
#     def __init__(self, master):
#         self.master = master
#         self.master.title("Calendar")

#         # Create a calendar instance
#         self.cal = calendar.Calendar()

#         # Create a frame to hold the buttons
#         self.button_frame = tk.Frame(self.master)
#         self.button_frame.pack()

#         # Create a button for each day in the calendar
#         for day in self.cal.itermonthdays2(2023, 4):
#             if day[0] != 0:
#                 day_button = tk.Button(self.button_frame, text=str(day[0]))
#                 day_button.grid(row=day[0] // 7, column=day[0] % 7)

# root = tk.Tk()
# app = CalendarGUI(root)
# root.mainloop()



import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
import random

root = tk.Tk()
root.title("Continuous Plotting")

fig, ax = plt.subplots()
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

x_data = []
y_data = []

line, = ax.plot(x_data, y_data)

def update_plot():
    global x_data, y_data
    x_data.append(len(x_data))
    y_data.append(random.randint(0, 10))
    line.set_data(x_data, y_data)
    ax.relim()
    ax.autoscale_view()
    canvas.draw()

    root.after(1000, update_plot)

update_plot()

root.mainloop()