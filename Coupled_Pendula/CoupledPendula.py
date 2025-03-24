from manimlib import *
from scipy.integrate import solve_ivp

def coupled_system(t, state, g=9.81, L=1.0, m=1.0, k=0.5):
    x1, v1, x2, v2 = state

    dx1_dt = v1
    dv1_dt = - (g / L) * x1 - (k / m) * (x1 - x2)

    dx2_dt = v2
    dv2_dt = - (g / L) * x2 - (k / m) * (x2 - x1)

    return [dx1_dt, dv1_dt, dx2_dt, dv2_dt]

dt = 0.01
def solve_coupled_pendula(func, state0, time, dt1 = dt):
    solution = solve_ivp(
        coupled_system,
        t_span=(0, time),
        y0=state0,
        t_eval=np.arange(0, time, dt1),
    )
    return solution.y.T 


class CoupledPendula(InteractiveScene):
    def construct(self):
        label_x = Tex(R''' Time ''')
        label_y = Tex(R''' Displacement ''')
        pen_1 = Tex(R'''- Pendulum_1''')
        pen_2 = Tex(R'''- Pendulum_2''')
        sq_yel = Square(side_length = 0.2, fill_opacity=1, color= YELLOW)
        sq_red = Square(side_length= 0.2, fill_opacity=1, color= RED)
        axes = Axes(
            x_range = (0, 60, 5),
            y_range = (-20, 20, 5),
            width = 20,
            height = 10,
            axis_config = {"color": BLUE, },
        )
        axes.add_coordinate_labels(
            font_size = 40,
            num_decimal_places = 0,
        )
        axes.center()
        label_x.next_to(axes)
        label_y.next_to(axes)

        label_x.next_to(np.array([5, -1, 0]))
        label_y.next_to(np.array([-6.5, 3.5, 0]))
        sq_yel.next_to(np.array([3.6, 3, 0]))
        sq_red.next_to(np.array([3.6, 2.5, 0]))
        pen_1.next_to(np.array([4, 3, 0]))
        pen_2.next_to(np.array([4, 2.5, 0]))
        axes.set_width(FRAME_WIDTH)
        

        self.add(axes, label_x, label_y, sq_red, sq_yel, pen_1, pen_2)
              

        time = 60
        state = [10, 0, 0, 0]       # x1, v1, x2, v2
        points = solve_coupled_pendula(coupled_system, state, time)
        y_cord1 = []
        y_cord2 = []
        for arr in range(len(points)):
            y_val1 = points[arr][0]
            y_val2= points[arr][2]
            y_cord1.append(y_val1)
            y_cord2.append(y_val2)

        y_final1=np.array(y_cord1)
        y_final2=np.array(y_cord2)
        curve1 = VMobject().set_points_as_corners(axes.c2p(np.arange(0, time, dt),y_final1))
        curve2 = VMobject().set_points_as_corners(axes.c2p(np.arange(0, time, dt),y_final2))
        curve1.set_stroke(YELLOW, 3)
        curve2.set_stroke(RED, 3)

        dots = Group(GlowDot(color = YELLOW, radius = 0.25),GlowDot(color = RED, radius = 0.25))
        
        globals().update(locals())
        def update_dots(dots):
            for dot, curve in zip(dots, [curve1, curve2]): 
                dot.move_to(curve.get_end())
        
        dots.add_updater(update_dots)
        self.add(dots)
        self.play(ShowCreation(curve1),
                  ShowCreation(curve2),  
                  run_time = time)
