import pathlib
import pygubu
import tkinter as tk
import tkinter.ttk as ttk

PROJECT_PATH = pathlib.Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "gui.ui"


class GuiApp:
    def __init__(self, master=None):
        # build ui
        self.toplevel = tk.Tk() if master is None else tk.Toplevel(master)
        self.mainframe = tk.Frame(self.toplevel)
        self.controlFrame = tk.Frame(self.mainframe, container='false')
        self.bt_plan = tk.Button(self.controlFrame)
        self.bt_plan.configure(text='Plan')
        self.bt_plan.grid(column='0', padx='5', row='0', sticky='nw')
        self.bt_plan.bind('<ButtonRelease-1>', self.plan_callback, add='')
        self.bt_clean = tk.Button(self.controlFrame)
        self.bt_clean.configure(text='Clean')
        self.bt_clean.grid(column='1', row='0', sticky='nw')
        self.bt_clean.bind('<ButtonRelease-1>', self.clean_callback, add='')
        self.sc_roll = tk.Scale(self.controlFrame)
        self.var_roll = tk.DoubleVar(value='')
        self.sc_roll.configure(from_='0', label='Roll (°)', length='180', orient='horizontal')
        self.sc_roll.configure(resolution='0.5', state='normal', tickinterval='90', to='360')
        self.sc_roll.configure(variable=self.var_roll)
        self.sc_roll.grid(column='0', row='1', sticky='nw')
        self.sc_pitch = tk.Scale(self.controlFrame)
        self.var_pitch = tk.DoubleVar(value='')
        self.sc_pitch.configure(from_='0', label='Pitch (°)', length='180', orient='horizontal')
        self.sc_pitch.configure(resolution='0.5', state='normal', tickinterval='90', to='360')
        self.sc_pitch.configure(variable=self.var_pitch)
        self.sc_pitch.grid(column='1', row='1', sticky='nw')
        self.sc_yaw = tk.Scale(self.controlFrame)
        self.var_yaw = tk.DoubleVar(value='')
        self.sc_yaw.configure(from_='0', label='Yaw (°)', length='180', orient='horizontal')
        self.sc_yaw.configure(resolution='0.5', state='normal', tickinterval='90', to='360')
        self.sc_yaw.configure(variable=self.var_yaw)
        self.sc_yaw.grid(column='2', row='1', sticky='nw')
        self.sc_lenght = tk.Scale(self.controlFrame)
        self.var_lenght = tk.DoubleVar(value='')
        self.sc_lenght.configure(from_='0', label='Lenght', length='360', orient='horizontal')
        self.sc_lenght.configure(resolution='0.1', showvalue='true', state='normal', tickinterval='0.1')
        self.sc_lenght.configure(to='1', variable=self.var_lenght)
        self.sc_lenght.grid(column='0', columnspan='2', row='2', sticky='nw')
        self.et_lenght_multiplier = tk.Entry(self.controlFrame)
        self.var_lenght_multiplier = tk.DoubleVar(value=1.0)
        self.et_lenght_multiplier.configure(state='normal', textvariable=self.var_lenght_multiplier, validate='key', width='6')
        _text_ = '''1.0'''
        self.et_lenght_multiplier.delete('0', 'end')
        self.et_lenght_multiplier.insert('0', _text_)
        self.et_lenght_multiplier.grid(column='2', pady='20', row='2', sticky='nw')
        _validatecmd = (self.et_lenght_multiplier.register(self.lenght_multiplier_validate), '%P')
        self.et_lenght_multiplier.configure(validatecommand=_validatecmd)
        self.lb_lenght_multiplier = tk.Label(self.controlFrame)
        self.lb_lenght_multiplier.configure(font='{Arial} 8 {}', state='normal', text='Lenght Multipl.')
        self.lb_lenght_multiplier.grid(column='2', row='2', sticky='nw')
        self.lb_status = tk.Label(self.controlFrame)
        self.lb_status.configure(text='Status:')
        self.lb_status.grid(column='1', row='0', sticky='e')
        self.et_status = tk.Entry(self.controlFrame)
        self.var_status_msg = tk.StringVar(value='')
        self.et_status.configure(state='readonly', textvariable=self.var_status_msg)
        self.et_status.grid(column='2', row='0')
        self.bt_draw_plane = tk.Button(self.controlFrame)
        self.bt_draw_plane.configure(text='Draw')
        self.bt_draw_plane.grid(column='0', padx='65', row='0', sticky='n')
        self.bt_draw_plane.bind('<ButtonRelease-1>', self.draw_plane_callback, add='')
        self.sc_interpol = tk.Scale(self.controlFrame)
        self.var_interpol = tk.DoubleVar(value='')
        self.sc_interpol.configure(from_='0', label='Points Interpolation Fraction (%)', length='360', orient='horizontal')
        self.sc_interpol.configure(resolution='1', tickinterval='10', to='100', variable=self.var_interpol)
        self.sc_interpol.grid(column='0', columnspan='2', row='3', sticky='nw')
        self.sc_interpol.bind('<ButtonRelease-1>', self.interpolation_fraction_callback, add='')
        self.lb_npoints = tk.Label(self.controlFrame)
        self.lb_npoints.configure(state='normal', text='Number of Points')
        self.lb_npoints.grid(column='2', pady='15', row='3', sticky='nw')
        self.et_npoints = tk.Entry(self.controlFrame)
        self.var_npoints = tk.IntVar(value='')
        self.et_npoints.configure(state='readonly', textvariable=self.var_npoints)
        self.et_npoints.grid(column='2', pady='40', row='3', sticky='w')
        self.lb_canvas_lenght = tk.Label(self.controlFrame)
        self.lb_canvas_lenght.configure(font='{Arial} 8 {}', state='normal', text='Canvas Lenght')
        self.lb_canvas_lenght.grid(column='2', columnspan='1', pady='20', row='2', sticky='sw')
        self.et_canvas_lenght = tk.Entry(self.controlFrame)
        self.var_canvas_lenght = tk.IntVar(value=4)
        self.et_canvas_lenght.configure(state='normal', textvariable=self.var_canvas_lenght, validate='key', width='6')
        _text_ = '''4'''
        self.et_canvas_lenght.delete('0', 'end')
        self.et_canvas_lenght.insert('0', _text_)
        self.et_canvas_lenght.grid(column='2', pady='0', row='2', sticky='sw')
        _validatecmd = (self.et_canvas_lenght.register(self.canvas_lenght_validate), '%P')
        self.et_canvas_lenght.configure(validatecommand=_validatecmd)
        self.et_eef_step = tk.Entry(self.controlFrame)
        self.var_eef_step = tk.DoubleVar(value=0.1)
        self.et_eef_step.configure(state='normal', textvariable=self.var_eef_step, validate='key', width='6')
        _text_ = '''0.1'''
        self.et_eef_step.delete('0', 'end')
        self.et_eef_step.insert('0', _text_)
        self.et_eef_step.grid(column='2', padx='30', pady='20', row='2', sticky='ne')
        _validatecmd = (self.et_eef_step.register(self.lenght_multiplier_validate), '%P')
        self.et_eef_step.configure(validatecommand=_validatecmd)
        self.lb_eef_step = tk.Label(self.controlFrame)
        self.lb_eef_step.configure(font='{Arial} 8 {}', justify='left', state='normal', text='eef_step')
        self.lb_eef_step.grid(column='2', padx='40', row='2', sticky='ne')
        self.et_jump_thresh = tk.Entry(self.controlFrame)
        self.var_jump_thresh = tk.DoubleVar(value=0.0)
        self.et_jump_thresh.configure(state='normal', textvariable=self.var_jump_thresh, validate='key', width='6')
        _text_ = '''0.0'''
        self.et_jump_thresh.delete('0', 'end')
        self.et_jump_thresh.insert('0', _text_)
        self.et_jump_thresh.grid(column='2', padx='30', row='2', sticky='se')
        _validatecmd = (self.et_jump_thresh.register(self.lenght_multiplier_validate), '%P')
        self.et_jump_thresh.configure(validatecommand=_validatecmd)
        self.lb_jump_thresh = tk.Label(self.controlFrame)
        self.lb_jump_thresh.configure(font='{Arial} 8 {}', justify='left', state='normal', text='jump_thresh.')
        self.lb_jump_thresh.grid(column='2', columnspan='1', padx='20', pady='22', row='2', sticky='se')
        self.controlFrame.pack(side='bottom')
        self.controlFrame.grid_anchor('s')
        self.frame4 = tk.Frame(self.mainframe)
        self.canvas = tk.Canvas(self.frame4)
        self.canvas.configure(background='#ffffff', borderwidth='1', cursor='pencil', height='400')
        self.canvas.configure(highlightbackground='#000000', width='550')
        self.canvas.pack(pady='10', side='top')
        self.canvas.bind('<B1-Motion>', self.canvas_motion_callback, add='')
        self.canvas.bind('<Button-1>', self.canvas_pressed_callback, add='')
        self.canvas.bind('<ButtonRelease-1>', self.canvas_released_callback, add='')
        self.frame4.pack(side='top')
        self.mainframe.pack(side='top')
        self.toplevel.configure(height='500', width='400')
        self.toplevel.resizable(False, False)
        self.toplevel.title('Robot Path')

        # Main widget
        self.mainwindow = self.toplevel
    
    def run(self):
        self.mainwindow.mainloop()

    def plan_callback(self, event=None):
        pass

    def clean_callback(self, event=None):
        pass

    def lenght_multiplier_validate(self, P):
        pass

    def draw_plane_callback(self, event=None):
        pass

    def interpolation_fraction_callback(self, event=None):
        pass

    def canvas_lenght_validate(self, P):
        pass

    def canvas_motion_callback(self, event=None):
        pass

    def canvas_pressed_callback(self, event=None):
        pass

    def canvas_released_callback(self, event=None):
        pass


if __name__ == '__main__':
    app = GuiApp()
    app.run()


