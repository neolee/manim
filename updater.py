from manimlib import * # type: ignore


class Updater(Scene):
    def construct(self):
        square = Square()
        square.set_fill(BLUE_E, 1)

        # on all frames, the constructor Brace(square, UP) will
        # be called, and the mobject brace will set its data to match
        # that of the newly constructed object
        brace = always_redraw(Brace, square, UP)

        label = TexText("Width = 0.00")
        number = label.make_number_changeable("0.00")

        # this ensures that the method deicmal.next_to(square)
        # is called on every frame
        label.always.next_to(brace, UP)
        # we could also write the following equivalent line
        # label.add_updater(lambda m: m.next_to(brace, UP))

        # if the argument itself might change, you can use f_always,
        # for which the arguments following the initial Mobject method
        # should be functions returning arguments to that method.

        # the following line ensures thst decimal.set_value(square.get_y())
        # is called every frame
        number.f_always.set_value(square.get_width)
        # we could also write the following equivalent line
        # number.add_updater(lambda m: m.set_value(square.get_width()))

        self.add(square, brace, label)

        # notice that the brace and label track with the square
        self.play(
            square.animate.scale(2),
            rate_func=there_and_back,
            run_time=2,
        )
        self.wait()
        self.play(
            square.animate.set_width(5, stretch=True),
            run_time=3,
        )
        self.wait()
        self.play(
            square.animate.set_width(2),
            run_time=3
        )
        self.wait()

        # in general, you can alway call Mobject.add_updater, and pass in
        # a function that you want to be called on every frame
        # The function should take in either one argument, the mobject,
        # or two arguments, the mobject and the amount of time since the last frame
        now = self.time
        w0 = square.get_width()
        square.add_updater(
            lambda m: m.set_width(w0 * math.sin(self.time - now) + w0)
        )
        self.wait(4 * PI)


class NumberManipulation(Scene):
    def construct(self):
        axes = Axes((-3, 3), (-3, 3), unit_size=1)
        axes.to_edge(DOWN)
        axes.add_coordinate_labels(font_size=16)
        circle = Circle(radius=2)
        circle.set_stroke(YELLOW, 3)
        circle.move_to(axes.get_origin())
        self.add(axes, circle)

        # when numbers show up in tex, they can be readily
        # replaced with DecimalMobjects so that methods like
        # get_value and set_value can be called on them, and
        # animations like ChangeDecimalToValue can be called
        # on them.
        tex = Tex("x^2 + y^2 = 4.00")
        tex.next_to(axes, UP, buff=0.5)
        value = tex.make_number_changeable("4.00")


        # This will tie the right hand side of our equation to
        # the square of the radius of the circle
        value.add_updater(lambda v: v.set_value(circle.get_radius()**2)) # type: ignore
        self.add(tex)

        text = Text("""
            You can manipulate numbers
            in Tex mobjects
        """, font_size=30)
        text.next_to(tex, RIGHT, buff=1.5)
        arrow = Arrow(text, tex)
        self.add(text, arrow)

        self.play(
            circle.animate.set_height(2.0),
            run_time=4,
            rate_func=there_and_back,
        )

        # by default, tex.make_number_changeable replaces the first occurance
        # of the number,but by passing replace_all=True it replaces all and
        # returns a group of the results
        exponents = tex.make_number_changeable("2", replace_all=True)
        self.play(
            LaggedStartMap(
                FlashAround, exponents,
                lag_ratio=0.2, buff=0.1, color=RED
            ),
            exponents.animate.set_color(RED)
        )

        def func(x, y):
            # switch from manim coords to axes coords
            xa, ya = axes.point_to_coords(np.array([x, y, 0])) # type: ignore
            return xa**4 + ya**4 - 4 # type: ignore

        new_curve = ImplicitFunction(func)
        new_curve.match_style(circle)
        circle.rotate(angle_of_vector(new_curve.get_start()))  # align
        value.clear_updaters()

        self.play(
            *(ChangeDecimalToValue(exp, 4) for exp in exponents), # type: ignore
            ReplacementTransform(circle.copy(), new_curve),
            circle.animate.set_stroke(width=1, opacity=0.5),
        )
