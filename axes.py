from manimlib import * # type: ignore


class Triangle(Scene):
    def construct(self):
        axes = Axes(
            x_range=(-5, 5, 1),  # x range and step
            y_range=(-5, 5, 1),  # y range and step
            axis_config={"include_numbers": False}  # hide on-axis tips
        )
        axes.add_coordinate_labels()  # add labels

        self.play(ShowCreation(axes))

        triangle = Polygon(
            axes.c2p(0, 1, 0),
            axes.c2p(-1, -1, 0),  # coordinates to screen position
            axes.c2p(1, -1, 0),
            color=BLUE,
            fill_opacity=0.5
        )

        self.play(FadeIn(triangle))

        # animating: `triangle.animate.scale` stretch the object on both dimensions
        self.play(triangle.animate.scale(2), run_time=2)
        self.play(triangle.animate.scale(0.5), run_time=2)

        # animating: `ApplyMethod(triangle.stretch, scale, dim)` let us assign a `dim`
        self.play(ApplyMethod(triangle.stretch, 2, 0), run_time=2)
        self.play(ApplyMethod(triangle.stretch, 2, 1), run_time=2)
        self.play(ApplyMethod(triangle.stretch, 0.5, 1), run_time=2)
        self.play(ApplyMethod(triangle.stretch, 0.5, 0), run_time=2)

        self.wait()


class Coordinate(Scene):
    def construct(self):
        axes = Axes(
            # x-axis ranges from -1 to 10, with a default step size of 1
            x_range=(-1, 10),
            # y-axis ranges from -2 to 2 with a step size of 0.5
            y_range=(-2, 2, 0.5),
            # axes will be stretched so as to match the specified
            # height and width
            height=6,
            width=10,
            # axes is made of two NumberLine mobjects
            # can specify their configuration with axis_config
            axis_config=dict(
                stroke_color=GREY_A,
                stroke_width=2,
                numbers_to_exclude=[0],
            ),
            # alternatively, we can specify configuration for just one
            # of them, like this:
            y_axis_config=dict(
                big_tick_numbers=[-2, 2],
            )
        )
        # keyword arguments of add_coordinate_labels can be used to
        # configure the DecimalNumber mobjects which it creates and
        # adds to the axes
        axes.add_coordinate_labels(
            font_size=20,
            num_decimal_places=1,
        )
        self.add(axes)

        # axes descends from the CoordinateSystem class, meaning
        # you can call call axes.coords_to_point, abbreviated to
        # axes.c2p, to associate a set of coordinates with a point,
        # like so:
        dot = Dot(color=RED)
        dot.move_to(axes.c2p(0, 0))
        self.play(FadeIn(dot, scale=0.5))
        self.play(dot.animate.move_to(axes.c2p(3, 2)))
        self.wait()
        self.play(dot.animate.move_to(axes.c2p(5, 0.5)))
        self.wait()

        # similarly, we can call axes.point_to_coords, or axes.p2c
        # print(axes.p2c(dot.get_center()))

        # we can draw lines from the axes to better mark the coordinates
        # of a given point
        # here, the always_redraw command means that on each new frame
        # the lines will be redrawn
        h_line = always_redraw(lambda: axes.get_h_line(dot.get_left()))
        v_line = always_redraw(lambda: axes.get_v_line(dot.get_bottom()))

        self.play(
            ShowCreation(h_line),
            ShowCreation(v_line),
        )
        self.play(dot.animate.move_to(axes.c2p(3, -2)))
        self.wait()
        self.play(dot.animate.move_to(axes.c2p(1, 1)))
        self.wait()

        # if we tie the dot to a particular set of coordinates, notice
        # that as we move the axes around it respects the coordinate
        # system defined by them
        f_always(dot.move_to, lambda: axes.c2p(1, 1))
        self.play(
            axes.animate.scale(0.75).to_corner(UL),
            run_time=2,
        )
        self.wait()
        self.play(FadeOut(VGroup(axes, dot, h_line, v_line))) # type: ignore

        # other coordinate systems you can play around with include
        # ThreeDAxes, NumberPlane, and ComplexPlane.


class FunctionGraph(Scene):
    def construct(self):
        axes = Axes((-3, 10), (-1, 8), height=6)
        axes.add_coordinate_labels()

        self.play(Write(axes, lag_ratio=0.01, run_time=1))

        # Axes.get_graph will return the graph of a function
        sin_graph = axes.get_graph(
            lambda x: 2 * math.sin(x),
            color=BLUE,
        )
        # by default, it draws it so as to somewhat smoothly interpolate
        # between sampled points (x, f(x)).  If the graph is meant to have
        # a corner, though, you can set use_smoothing to False
        relu_graph = axes.get_graph(
            lambda x: max(x, 0),
            use_smoothing=False,
            color=YELLOW,
        )
        # for discontinuous functions, you can specify the point of
        # discontinuity so that it does not try to draw over the gap
        step_graph = axes.get_graph(
            lambda x: 2.0 if x > 3 else 1.0,
            discontinuities=[3],
            color=GREEN,
        )

        # Axes.get_graph_label takes in either a string or a mobject.
        # If it's a string, it treats it as a LaTeX expression
        # by default it places the label next to the graph near the right side,
        # and has it match the color of the graph
        sin_label = axes.get_graph_label(sin_graph, "\\sin(x)")
        relu_label = axes.get_graph_label(relu_graph, Text("ReLU"))
        step_label = axes.get_graph_label(step_graph, Text("Step"), x=4)

        self.play(
            ShowCreation(sin_graph),
            FadeIn(sin_label, RIGHT),
        )
        self.wait(2)
        self.play(
            ReplacementTransform(sin_graph, relu_graph),
            FadeTransform(sin_label, relu_label),
        )
        self.wait()
        self.play(
            ReplacementTransform(relu_graph, step_graph),
            FadeTransform(relu_label, step_label),
        )
        self.wait()

        parabola = axes.get_graph(lambda x: 0.25 * x**2)
        parabola.set_stroke(BLUE)
        self.play(
            FadeOut(step_graph),
            FadeOut(step_label),
            ShowCreation(parabola)
        )
        self.wait()

        # we can use axes.input_to_graph_point, abbreviated
        # to axes.i2gp, to find a particular point on a graph
        dot = Dot(color=RED)
        dot.move_to(axes.i2gp(2, parabola)) # type: ignore
        self.play(FadeIn(dot, scale=0.5))

        # a value tracker lets us animate a parameter, usually
        # with the intent of having other mobjects update based
        # on the parameter
        x_tracker = ValueTracker(2)
        dot.add_updater(lambda d: d.move_to(axes.i2gp(x_tracker.get_value(), parabola))) # type: ignore

        self.play(x_tracker.animate.set_value(4), run_time=3)
        self.play(x_tracker.animate.set_value(-2), run_time=3)
        self.wait()
