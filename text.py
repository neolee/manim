from manimlib import * # type: ignore


class BasicText(Scene):
    def construct(self):
        # To run this scene properly, you should have "Consolas" font in your computer
        # for full usage, you can see https://github.com/3b1b/manim/pull/680
        text = Text("Here is a text", font="Consolas", font_size=90)
        difference = Text(
            """
            The most important difference between Text and TexText is that\n
            you can change the font more easily, but can't use the LaTeX grammar
            """,
            font="Arial", font_size=24,
            # t2c is a dict that you can choose color for different text
            t2c={"Text": BLUE, "TexText": BLUE, "LaTeX": ORANGE}
        )
        VGroup(text, difference).arrange(DOWN, buff=1)
        self.play(Write(text))
        self.play(FadeIn(difference, UP))
        self.wait(3)

        fonts = Text(
            "And you can also set the font according to different words",
            font="Arial",
            t2f={"font": "Consolas", "words": "Consolas"},
            t2c={"font": BLUE, "words": GREEN}
        )
        fonts.set_width(FRAME_WIDTH - 1)
        slant = Text(
            "And the same as slant and weight",
            font="Consolas",
            t2s={"slant": ITALIC},
            t2w={"weight": BOLD},
            t2c={"slant": ORANGE, "weight": RED}
        )
        VGroup(fonts, slant).arrange(DOWN, buff=0.8)
        self.play(FadeOut(text), FadeOut(difference, shift=DOWN))
        self.play(Write(fonts))
        self.wait()
        self.play(Write(slant))
        self.wait()


class Anagram(Scene):
    def construct(self):
        # source = Text("the morse code", height=1)
        # target = Text("here come dots", height=1)
        source = Text("two eleven", height=1)
        target = Text("one twelve", height=1)
        saved_source = source.copy()

        # TransformMatchingShapes will try to line up all pieces of a
        # source mobject with those of a target, regardless of the
        # what Mobject type they are
        self.play(Write(source))
        self.wait()
        kw = {"run_time": 3, "path_arc": PI/2}
        self.play(TransformMatchingShapes(source, target, **kw))
        self.wait()
        self.play(TransformMatchingShapes(target, saved_source, **kw))
        self.wait()


class TexTransform(Scene):
    def construct(self):
        # Tex to color map
        t2c = {
            "A": BLUE,
            "B": TEAL,
            "C": GREEN,
        }
        # Configuration to pass along to each Tex mobject
        kw = dict(font_size=72, t2c=t2c)
        lines = VGroup(
            Tex("A^2 + B^2 = C^2", **kw),
            Tex("A^2 = C^2 - B^2", **kw),
            Tex("A^2 = (C + B)(C - B)", **kw),
            Tex(R"A = \sqrt{(C + B)(C - B)}", **kw),
        )
        lines.arrange(DOWN, buff=LARGE_BUFF)

        self.add(lines[0])
        # The animation TransformMatchingStrings will line up parts
        # of the source and target which have matching substring strings.
        # Here, giving it a little path_arc makes each part rotate into
        # their final positions, which feels appropriate for the idea of
        # rearranging an equation
        self.play(
            TransformMatchingStrings(
                lines[0].copy(), lines[1],
                # matched_keys specifies which substring should
                # line up. If it's not specified, the animation
                # will align the longest matching substrings.
                # In this case, the substring "^2 = C^2" would
                # trip it up
                matched_keys=["A^2", "B^2", "C^2"],
                # When you want a substring from the source
                # to go to a non-equal substring from the target,
                # use the key map.
                key_map={"+": "-"},
                path_arc=90 * DEG,
            ),
        )
        self.wait()
        self.play(TransformMatchingStrings(
            lines[1].copy(), lines[2],
            matched_keys=["A^2"]
        ))
        self.wait()
        self.play(
            TransformMatchingStrings(
                lines[2].copy(), lines[3],
                key_map={"2": R"\sqrt"},
                path_arc=-30 * DEG,
            ),
        )
        self.wait(2)
        self.play(LaggedStartMap(FadeOut, lines, shift=2 * RIGHT)) # type: ignore


class TexIndexing(Scene):
    def construct(self):
        # You can index into Tex mobject (or other StringMobjects) by substrings
        equation = Tex(R"e^{\pi i} = -1", font_size=144)

        self.add(equation)
        self.play(FlashAround(equation["e"]))
        self.wait()
        self.play(Indicate(equation[R"\pi"]))
        self.wait()
        self.play(TransformFromCopy(
            equation[R"e^{\pi i}"].copy().set_opacity(0.5),
            equation["-1"],
            path_arc=-PI / 2,
            run_time=3
        ))
        self.play(FadeOut(equation))

        # Or regular expressions
        equation = Tex("A^2 + B^2 = C^2", font_size=144)

        self.play(Write(equation))
        for part in equation[re.compile(r"\w\^2")]:
            self.play(FlashAround(part))
        self.wait()
        self.play(FadeOut(equation))

        # Indexing by substrings like this may not work when
        # the order in which Latex draws symbols does not match
        # the order in which they show up in the string.
        # For example, here the infinity is drawn before the sigma
        # so we don't get the desired behavior.
        equation = Tex(R"\sum_{n = 1}^\infty \frac{1}{n^2} = \frac{\pi^2}{6}", font_size=72)
        self.play(FadeIn(equation))
        self.play(equation[R"\infty"].animate.set_color(RED))  # Doesn't hit the infinity
        self.wait()
        self.play(FadeOut(equation))

        # However you can always fix this by explicitly passing in
        # a string you might want to isolate later. Also, using
        # \over instead of \frac helps to avoid the issue for fractions
        equation = Tex(
            R"\sum_{n = 1}^\infty {1 \over n^2} = {\pi^2 \over 6}",
            # Explicitly mark "\infty" as a substring you might want to access
            isolate=[R"\infty"],
            font_size=72
        )
        self.play(FadeIn(equation))
        self.play(equation[R"\infty"].animate.set_color(RED))  # Got it!
        self.wait()
        self.play(FadeOut(equation))
