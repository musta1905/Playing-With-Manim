from manimlib import *
from scipy.integrate import odeint
from scipy.integrate import solve_ivp

def lorenz_system(t, state, sigma=10, rho=28, beta=8 / 3):
    x, y, z = state
    dxdt = sigma * (y - x)
    dydt = x * (rho - z) - y
    dzdt = x * y - beta * z
    return [dxdt, dydt, dzdt]

def ode_solution_points(function, state0, time, dt=0.01):
    solution = solve_ivp(
        lorenz_system,
        t_span=(0, time),
        y0=state0,
        t_eval=np.arange(0, time, dt)
    )
    return solution.y.T

class LorenzAttractor(InteractiveScene):
    def construct(self):
        axes = ThreeDAxes(
            x_range=(-50, 50, 5),
            y_range=(-50, 50, 5),
            z_range=(-0, 50, 5),
            width=16,
            height=16,
            depth=8
        )

        axes.set_width(FRAME_WIDTH)
        axes.center()

        self.frame.reorient(43, 76, 1, IN, 10)
        self.add(axes)
        epsilon = 0.001
        evolution_time = 30
        states = [
            [10, 10, 10 + n*epsilon]
                  for n in range(10)]
        colors = color_gradient([BLUE, YELLOW], len(states))
        

        curves = VGroup()
        for state, color in zip(states, colors):
            points = ode_solution_points(lorenz_system, state, evolution_time)
            curve = VMobject().set_points_as_corners(axes.c2p(*points.T))
            curve.set_stroke(color, 2)
            curves.add(curve)
            
        dots = Group(GlowDot(color=color, radius = 0.5) for color in colors)
        
        globals().update(locals())
        def update_dots(dots):
            for dot, curve in zip(dots, curves):
                dot.move_to(curve.get_end())
        
        dots.add_updater(update_dots)
        tails = VGroup(
            TracingTail(dot, time_traced= 3).match_color(dot)
            for dot in dots
        )

        self.add(dots)
        self.add(tails)
        curves.set_opacity(0)
        self.play(*(
            ShowCreation(curve, rate_func= linear)
            for curve in curves
            ),
            self.frame.animate.reorient(270, 72, 0, IN, 10), 
            run_time=evolution_time
        )
