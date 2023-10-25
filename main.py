from tkinter import ttk
import tkinter as tk

class PomodoroTimer:
    def __init__(self):
        # VALUES -----------------------------------------------------------------------------
        self.work_timer, self.quick_rest_timer, self.long_rest_timer = 0, 0 ,0
        self.clock, self.session = 0, 0
        self.paused = False

        # INITIATE GUI -----------------------------------------------------------------------
        self.root = tk.Tk()
        self.root.title('Pomodoro Timer')
        self.root.geometry('480x480+500+150')

        self.style = ttk.Style()
        self.style.configure('TSpinbox', foreground='red', background='white')

        # INITIALIZE AND RUN TIMER -----------------------------------------------------------
        self.timer()

        self.root.mainloop()
    
    def timer(self): # DEFINE POMODORO TIMER VALUES AND START --------------------------------
        self.init_frame = tk.Frame(self.root, width=480, height=480)
        self.init_frame.pack(fill='both', expand=True)
        self.init_frame.grid_rowconfigure((0,1,2), weight=2)
        self.init_frame.grid_columnconfigure((0,1,2), weight=1)

        self.instruct = tk.Label(self.init_frame, font=('Ubuntu', 20, 'bold'), text="Session Timer Set Up")
        self.instruct.place(relx=0.5, rely=0.1, anchor='n')

        # Get work session values
        self.setWorkTimer_label = tk.Label(self.init_frame, width=10, text="Work Session")
        self.setWorkTimer_label.grid(row=1, column=0, sticky='S')
        self.w_var = tk.IntVar(value=25)
        self.setWorkTimer_values = ttk.Spinbox(self.init_frame, from_=25, to=60, increment=5, textvariable=self.w_var, state='readonly')
        self.setWorkTimer_values.grid(row=2, column=0, padx=15, sticky='NE')
        
        # Get quick rest session values
        self.setQuickRest_label = tk.Label(self.init_frame, width=10, text="Break Session")
        self.setQuickRest_label.grid(row=1, column=1, sticky='S')
        self.qr_var = tk.IntVar(value=5)
        self.setQuickRest_values = ttk.Spinbox(self.init_frame, from_=5, to=15, increment=5, textvariable=self.qr_var, state='readonly')
        self.setQuickRest_values.grid(row=2, column=1, padx=15, sticky='N')
        
        # Get long relax session values
        self.setLongRest_label = tk.Label(self.init_frame, width=10, text="Relax Session")
        self.setLongRest_label.grid(row=1, column=2, sticky='S')
        self.lr_var = tk.IntVar(value=15)
        self.setLongRest_values = ttk.Spinbox(self.init_frame, from_=15, to=60, increment=5, textvariable=self.lr_var, state='readonly')
        self.setLongRest_values.grid(row=2, column=2, padx=15, sticky='NW')

        # Print program explanation
        self.info1_label = tk.Label(self.init_frame, pady=10, wraplength=410, font=('Ubuntu', 12), text="******************************************************************\n\nThe Pomodoro Technique is a time management method aimed towards improving concentration and work productivity. Get ready! The Pomodoro Timer will lead you through the following:")
        self.info1_label.grid(row=3, column=0, columnspan=3, sticky='N')
        self.info2_label = tk.Label(self.init_frame, wraplength=410, font=('Ubuntu', 12, 'bold'), text="(Work Session > Break Session) x3 > Work session > Relax Session!")
        self.info2_label.grid(row=4, column=0, columnspan=3, sticky='N')

        # Start program
        self.init_button = tk.Button(self.init_frame, width=10, height=2, text="Initialize Timer", command=self.run_timer)
        self.init_button.grid(row=5, column=1, pady=30)

    def run_timer(self): 
        # Set session values
        self.work_timer = int(self.setWorkTimer_values.get()) * 60
        self.quick_rest_timer = int(self.setQuickRest_values.get()) * 60
        self.long_rest_timer = int(self.setLongRest_values.get()) * 60

        for widget in self.init_frame.winfo_children():
            widget.destroy()
        self.init_frame.pack_forget()  

        self.timer_frame = tk.Frame(self.root, width=480, height=480)
        self.timer_frame.pack(fill='both', expand=True)      
        self.timer_frame.grid_rowconfigure((0,1), weight=1)
        self.timer_frame.grid_columnconfigure((0,2), weight=1)

        # ( session_status_label text to be set in session_handler() )
        self.session_status_label = tk.Label(self.timer_frame, font=('Ubuntu', 20, 'bold'), foreground='red')
        self.session_status_label.place(relx=0.5, rely=0.1, anchor='n')

        self.timer_label = tk.Label(self.timer_frame, font=('Ubuntu', 70), text="00:00")
        self.timer_label.place(relx=0.5, rely=0.3, anchor='n')

        # Start timer
        self.start_button = tk.Button(self.timer_frame, width=10, height=2, text="Start", command=self.start_timer)
        self.start_button.grid(row=1, column=0, sticky='E')

        # Pause timer
        self.pause_button = tk.Button(self.timer_frame, width=10, height=2, text="Pause", command=self.pause_timer)
        self.pause_button.grid(row=1, column=1)

        # Reset timer
        self.reset_button = tk.Button(self.timer_frame, width=10, height=2, text="Reset", command=self.reset_timer)
        self.reset_button.grid(row=1, column=2, sticky='W')

        self.progress_label = tk.Label(self.timer_frame, font=('Ubuntu', 14, 'bold'))
        self.progress_label.place(relx=0.5, rely=0.9, anchor='n')

    def session_handler(self):
        # 1) Work -> 2) Break -> 3) Work -> 4) Break -> 5) Work -> 6) Break -> 7) Work -> 8) Relax -> 9) Done
        if self.session > 8:
            self.session_status_label.config(text="Congrats! Productivity feels good, doesn't it?")
            self.pause_button.config(state=tk.DISABLED)
            self.paused = True
            self.root.after(5000, self.reset_timer)
        else:
            if self.session == 8:
                self.clock = self.long_rest_timer
                self.session_status_label.config(text="Relax! You've earned it.")
            elif self.session % 2 == 1:
                self.clock = self.work_timer
                self.session_status_label.config(text="Get to work!")
            elif self.session % 2 == 0:
                self.clock = self.quick_rest_timer
                self.session_status_label.config(text="Whew! Take a short break.")

            self.progress_label.config(text="{}/8 sessions completed".format(self.session))

    def start_timer(self):
        self.paused = False
        self.start_button.config(state=tk.DISABLED)
        self.pause_button.config(state=tk.NORMAL)
        self.reset_button.config(state=tk.DISABLED)
        self.countdown()

    def countdown(self):
        if self.clock < 0:
            self.session += 1
            self.session_handler()
        if not self.paused:
            minutes, seconds = divmod(self.clock, 60)
            self.timer_label.config(text="{:02d}:{:02d}".format(minutes, seconds))
            self.clock -= 1
            self.root.after(1000, self.countdown)    

    def pause_timer(self):
        self.paused = True
        self.start_button.config(state=tk.NORMAL)
        self.pause_button.config(state=tk.DISABLED)
        self.reset_button.config(state=tk.NORMAL)

    def reset_timer(self):
        self.reset = True
        self.root.destroy()
        PomodoroTimer()


PomodoroTimer()