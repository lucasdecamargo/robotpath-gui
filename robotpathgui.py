from curses.ascii import isdigit
from posixpath import split
from guiapp import GuiApp
from math import (pi, radians)
from numpy import linspace

class RobotPathGui(GuiApp):
    def __init__(self):
        super().__init__()

        self.var_lenght.set(0.0)
        self.var_interpol.set(100)
        self.var_canvas_lenght.set(1)

        self.points_x = []
        self.points_y = []
        self._plan_cb = None
        self._draw_plane_cb = None
        self._plane_change_cb = None

        self.sc_roll.bind('<ButtonRelease-1>', self.plane_change_callback, add='')
        self.sc_pitch.bind('<ButtonRelease-1>', self.plane_change_callback, add='')
        self.sc_yaw.bind('<ButtonRelease-1>', self.plane_change_callback, add='')
        self.sc_lenght.bind('<ButtonRelease-1>', self.plane_change_callback, add='')
        self.et_lenght_multiplier.bind('<ButtonRelease-1>', self.plane_change_callback, add='')

    def set_plan_callback(self, func):
        self._plan_cb = func
    
    def set_draw_plane_callback(self, func):
        self._draw_plane_cb = func

    def set_plane_change_callback(self, func):
        self._plane_change_cb = func

    def plane_change_callback(self, event=None):
        if self._plane_change_cb is not None:
            self._plane_change_cb()

    def get_points(self):
        assert len(self.points_x) == len(self.points_y), "Point arrays x and y are of different size"
        
        idx = [int(n) for n in linspace(0,len(self.points_x)-1,len(self.points_x)*self.var_interpol.get()/100.0)]
        return ([(self.points_x[i] - self.canvas.winfo_width()/2.0)/self.canvas.winfo_width() * self.var_canvas_lenght.get()  for i in idx],
                [(self.points_y[i] - self.canvas.winfo_height()/2.0)/self.canvas.winfo_height() * self.var_canvas_lenght.get()  for i in idx])


    def get_plane_parameters(self):
        param = {}
        param["roll"] = radians(self.var_roll.get())
        param["pitch"] = radians(self.var_pitch.get())
        param["yaw"] = radians(self.var_yaw.get())
        param["lenght"] = self.var_lenght.get()*self.var_lenght_multiplier.get()
        return param

    def status_msg(self, msg):
        self.var_status_msg.set(msg)

    def plan_callback(self, event=None):
        if self._plan_cb is not None:
            self._plan_cb()

    def draw_plane_callback(self, event=None):
        if self._draw_plane_cb is not None:
            self._draw_plane_cb()

    def lenght_multiplier_validate(self, P):
        try:
            if ' ' in P:
                return False
            if P=='':
                return False
            float(P)
            return True
        except Exception:
            return False

    def canvas_lenght_validate(self, P):
        try:
            if ' ' in P or '.' in P:
                return False
            if P=='':
                return False
            int(P)
            return True
        except Exception:
            return False

    def clean_callback(self, event=None):
        self.points_x.clear()
        self.points_y.clear()
        self.canvas.delete('all')

    def canvas_motion_callback(self, event=None):
        global lasx, lasy
        if lasx==event.x or lasy==event.y:
        	return
        self.points_x.append(event.x)
        self.points_y.append(event.y)
        self.canvas.create_line((lasx, lasy, event.x, event.y), fill='red', width=2)
        lasx, lasy = event.x, event.y

    def canvas_pressed_callback(self, event=None):
        global lasx, lasy
        self.points_x.append(event.x)
        self.points_y.append(event.y)
        lasx, lasy = event.x, event.y
    
    def canvas_released_callback(self, event=None):
        self.var_npoints.set(self.var_interpol.get()/100 * len(self.points_x))

    def interpolation_fraction_callback(self, event=None):
        self.var_npoints.set(self.var_interpol.get()/100 * len(self.points_x))

if __name__ == '__main__':
    app = RobotPathGui()
    app.run()
    
