import tkinter as tk
from tkinter import messagebox
import threading
import os
import re
    
class Timer:
    def __init__(self, width, height):
        self.valid_time = True;
        self.all_time = 0;
        self.timer = None;
        
        #width and height main window
        self.width = width
        self.height = height
        
        self.create_canvas()
        
        
    def create_canvas(self):
        self.root = tk.Tk()

        #setting main window
        self.root.title("Time is 00:00:00")
        self.root.geometry('{}x{}'.format(self.width, self.height))
        self.root.resizable(width=False, height=False)
        
        #top title
        self.top_title = tk.Label(self.root, text="Timer", font="Arial 17")
        self.top_title.pack()
        
        #label image
        img = tk.PhotoImage(file='timer1.png')
        self.lb_image = tk.Label(self.root, image=img)
        self.lb_image.pack()

        #white space
        self.separator = tk.Frame(self.root, height=10)
        self.separator.pack()

        #frame for time (hour:minute:second)
        self.frame = tk.Frame(self.root)
        self.frame.pack()

        #hours
        self.var_hours = tk.StringVar()
        self.var_hours.set("00")
        self.hours = tk.Entry(
                            self.frame, 
                            font="Arial 20", 
                            width=2, 
                            textvariable=self.var_hours
                            )
        self.hours.bind(
                        "<KeyRelease>", 
                        lambda event: self.entry_valide(
                                            event, 
                                            self.var_hours
                                            )
                        )
        self.hours.grid(row=0, column=0, padx=3)
        self.lb = tk.Label(self.frame, text=":", font="Arial 20")
        self.lb.grid(row=0, column=1)

        #minutes
        self.var_minutes = tk.StringVar()
        self.var_minutes.set("00")
        self.minutes = tk.Entry(
                                self.frame, 
                                font="Arial 20", 
                                width=2,
                                textvariable=self.var_minutes
                                )
        self.minutes.bind(
                        "<KeyRelease>", 
                        lambda event: self.entry_valide(
                                        event, 
                                        self.var_minutes
                                        )
                        )
        self.minutes.grid(row=0, column=2, padx=3)
        self.lb = tk.Label(self.frame, text=":", font="Arial 20")
        self.lb.grid(row=0, column=3)

        #seconds
        self.var_seconds = tk.StringVar()
        self.var_seconds.set("00")
        self.seconds = tk.Entry(
                                self.frame, 
                                font="Arial 20", 
                                width=2,
                                textvariable=self.var_seconds
                                )
        self.seconds.bind(
                        "<KeyRelease>", 
                        lambda event: self.entry_valide(
                                        event, self.var_seconds
                                        )
                        )
        self.seconds.grid(row=0, column=4, padx=3)

        #white space
        self.separator = tk.Frame(self.root, height=10)
        self.separator.pack()

        self.button = tk.Button(
                            self.root, 
                            text="Start", 
                            font="Arial 15", 
                            width=15, 
                            bg="#90EE90",
                            activebackground="#07db67",
                            cursor="hand1",
                            command=self.button_command,                 
                            )
        self.button.pack()
        
        #run main loop
        self.root.mainloop()
        
    def entry_valide(self, event, text_var):
        '''
            Function for validate enter time value
        '''
        value = event.widget.get()
        default_bd_color = self.root.cget('highlightbackground')
        default_active_bd_color = self.root.cget('highlightcolor')
        
        #replace all no digit value
        value = re.sub(r'[^\d]+', '', value)
        text_var.set(value)
        
        if(len(value) > 2):
            text_var.set(value[:2])
        
        try:
            value = int(value)
            event.widget.config(
                        highlightbackground=default_bd_color,
                        highlightcolor=default_active_bd_color
                        )
            self.valid_time = True;
        except Exception as err:    
            event.widget.config(
                                highlightbackground='red', 
                                highlightcolor='red')
            self.valid_time = False;
        
        
    def count_user_time(self):
        '''
            Function for counting entered time in seconds.
            Return time in seconds.
        '''
        hours = int(self.var_hours.get())
        minutes = int(self.var_minutes.get())
        seconds = int(self.var_seconds.get())
        self.all_time = hours*60*60+minutes*60+seconds
        return self.all_time
        
    def clear_screen_timer(self):
        '''
            Function for setting default screen.
        '''
        self.var_hours.set("00")
        self.var_minutes.set("00")
        self.var_seconds.set("00")
        
        self.root.title("Time is 00:00:00")
            
        self.button["text"] = "Start"
        self.button.config(bg="#90EE90", activebackground="#07db67")
        
    def set_new_time(self):
        '''
            Function for displaing new time.
        '''
        hours = int(self.all_time/3600)
        minutes = int((self.all_time%3600)/60)
        seconds = int(((self.all_time%3600)%60))
        
        hours = str(hours) if (hours >= 10) else'0'+str(hours)
        minutes = str(minutes) if (minutes >= 10) else'0'+str(minutes)
        seconds = str(seconds) if (seconds >= 10) else '0'+str(seconds)
            
        self.var_hours.set(hours)
        self.var_minutes.set(minutes)
        self.var_seconds.set(seconds)
        
        self.root.title(
                    "Time is {}:{}:{}".format(hours, minutes, seconds)
                    )
        
    def handler_timer_event(self):
        '''
            Function for handler timer event.
        '''
        #substract 1 second from the set time
        self.all_time -= 1;
        if(self.all_time == 0):
            #if time is over, clear screen, show notify and play sound
            self.clear_screen_timer()
            current_path = os.path.dirname(os.path.abspath(__file__))
            
            #notify
            os.system(
            'notify-send -i {}/timer1.png \
            "Timer app" "Time is over"'.format(current_path)
            )
            #play sound ('aplay' - only for .wav file)
            os.system('aplay {}/sound.wav'.format(current_path))
            return None
            
        self.set_new_time()
        
        #create new Timer
        self.timer = threading.Timer(1.0, self.handler_timer_event)
        self.timer.start()
        
        
    def button_command(self):
        '''
            Function for handler button click.
        '''
        if(self.button["text"] == "Start"):
            if(self.valid_time):
                value = self.count_user_time()
                #Start timer if set time is not 0
                if(value == 0):
                    messagebox.showinfo(
                            "No correct value", 
                            "Please, enter correct time!"
                            )
                else:
                    self.button.focus()
                    self.set_new_time()
                    #Start timer 1s
                    self.timer = threading.Timer(
                                            1.0, 
                                            self.handler_timer_event
                                            )
                    self.timer.start()
                    self.button["text"] = "Stop/Clear"
                    self.button.config(
                                bg="#FF0000", 
                                activebackground="#d51b01"
                                )
        else:
            if(self.timer):
                self.timer.cancel()
            self.clear_screen_timer()

#create main app
app = Timer(250, 250)
