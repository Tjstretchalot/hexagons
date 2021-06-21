from manim import *
import math

BASIS = np.array([
    [0, math.cos(30 * DEGREES)],
    [1, math.sin(30 * DEGREES)]
])
INV_BASIS = np.linalg.inv(BASIS)
NEON_GREEN = '#39ff14'

class TransformedHexagonMath(Scene):
    def construct(self):
        self.radius = 4 / math.sqrt(3)

        outer_hexagon = self.create_transformed_hexagon()
        lines_and_grid_mobjs = self.add_dashed_lines_and_grid(outer_hexagon)
        self.calculate_t_from_s_1(outer_hexagon)
        self.calculate_t_from_s_2(outer_hexagon)
        self.calculate_t_from_s_3(outer_hexagon)
        self.wait()
        self.play(*[FadeOut(mobj) for mobj in lines_and_grid_mobjs])
        self.wait()

    def create_transformed_hexagon(self):
        hex = TransformedHexagon(ORIGIN, self.radius, dots=True, labels=True)
        self.add(*hex.children())
        return hex

    def add_dashed_lines_and_grid(self, outer_hexagon):
        alpha = ValueTracker(0)

        def create_line_and_updater(start, end):
            line = DashedLine(start, end)
            num_dashes = line.calculate_num_dashes()

            def line_updater(x):
                a = alpha.get_value()
                visible_dashes = int(a * num_dashes)
                last_dash_alpha = a * num_dashes - visible_dashes

                for idx, child in enumerate(x.submobjects):
                    if idx < visible_dashes:
                        child.set_opacity(1)
                    elif idx == visible_dashes:
                        child.set_opacity(last_dash_alpha)
                    else:
                        child.set_opacity(0)

                return x

            line.add_updater(line_updater)
            return (line, line_updater)

        lines_and_updaters = (
            create_line_and_updater(outer_hexagon.vertices[0], outer_hexagon.vertices[4]),
            create_line_and_updater(outer_hexagon.vertices[1], outer_hexagon.vertices[3])
        )
        for (line, _) in lines_and_updaters:
            self.add(line)

        self.play(alpha.animate.set_value(1))

        lines = []
        for line, updater in lines_and_updaters:
            line.remove_updater(updater)
            lines.append(line)

        s_axis = DoubleArrow([outer_hexagon.vertices[-1][0], 0, 0], [outer_hexagon.vertices[2][0], 0, 0], buff=0)
        pos_s_tex = MathTex(r'\vec{s}').next_to(s_axis, RIGHT)
        neg_s_tex = MathTex(r'-\vec{s}').next_to(s_axis, LEFT)

        s_axis_start = s_axis.start.copy()
        s_axis_end = s_axis.end.copy()
        s_axis_center = s_axis.get_center()
        s_axis_center_start_delta = s_axis_start - s_axis_center
        s_axis_center_end_delta = s_axis_end - s_axis_center
        alpha.set_value(0)
        def s_axis_updater(x):
            a = alpha.get_value()
            if a == 0:
                return x.become(DoubleArrow(s_axis_start, s_axis_end, buff=0).scale(0).fade(1))

            return x.become(DoubleArrow(s_axis_center + s_axis_center_start_delta * a, s_axis_center + s_axis_center_end_delta * a, buff=0))

        s_axis.add_updater(s_axis_updater)
        self.add(s_axis.scale(0))
        self.play(alpha.animate.set_value(1))
        s_axis.remove_updater(s_axis_updater)
        self.play(GrowFromCenter(pos_s_tex), GrowFromCenter(neg_s_tex))

        return [*lines, s_axis, pos_s_tex, neg_s_tex]

    def calculate_t_from_s_1(self, outer_hexagon):
        qL = math.sqrt(3) * self.radius

        def pre_bottom_tex():
            # make some space
            self.play(Transform(outer_hexagon.texs[4], outer_hexagon.texs[4].copy().next_to(outer_hexagon.dots[4], DOWN)))


        self._calculate_t_from_s(
            np.array([(-2/3) * qL, (1/3) * qL]), np.array([(-1/3) * qL, (-1/3) * qL]),
            np.array([(-2/3) * qL, (1/3) * qL]), np.array([(-1/3) * qL, (2/3) * qL]),
            [(-7/12) * qL, (-5/12) * qL, (-1/2) * qL],
            None,
            [
                [
                    r'\frac{1}{3}qL + \left(\frac{s - \left(-\frac{2}{3}qL\right)}{\left(-\frac{1}{3}qL\right) - \left(-\frac{2}{3}qL\right)}\right)\left(\frac{2}{3}qL - \frac{1}{3}qL\right)',
                    0.3,
                    6
                ],
                [
                    r'\frac{1}{3}qL + \left(\frac{s + \frac{2}{3}qL}{\frac{1}{3}qL}\right)\left(\frac{1}{3}qL\right)',
                    0.5,
                    4
                ],
                [
                    r'\frac{1}{3}qL + s + \frac{2}{3}qL',
                    0.5,
                    1
                ],
                [
                    r'qL + s',
                    1,
                    1
                ]
            ],
            pre_bottom_tex,
            [
                [
                    r'\frac{1}{3}qL + \left(\frac{s - \left(-\frac{2}{3}qL\right)}{\left(-\frac{1}{3}qL\right) - \left(-\frac{2}{3}qL\right)}\right)\left(-\frac{1}{3}qL - \frac{1}{3}qL\right)',
                    0.3,
                    1
                ],
                [
                    r'\frac{1}{3}qL + \left(\frac{s + \frac{2}{3}qL}{\frac{1}{3}qL}\right)\left(-2 \cdot \frac{1}{3}qL\right)',
                    0.5,
                    1
                ],
                [
                    r'\frac{1}{3}qL - 2s - \frac{4}{3}qL',
                    0.5,
                    1
                ],
                [
                    r'-qL - 2s',
                    1,
                    1
                ]
            ],
            None,
            [
                [
                    r'(qL + s) - (-qL - 2s)',
                    0.5,
                    4
                ],
                [
                    r'qL + s + qL + 2s',
                    0.5,
                    1
                ],
                [
                    r'2qL + 3s',
                    1,
                    2
                ],
            ]
        )

    def calculate_t_from_s_2(self, outer_hexagon):
        qL = math.sqrt(3) * self.radius

        def pre_bottom_tex():
            # make some space
            self.play(Transform(outer_hexagon.texs[4], outer_hexagon.texs[4].copy().next_to(outer_hexagon.dots[4], LEFT)))

        self._calculate_t_from_s(
            np.array([(-1/3) * qL, (-1/3) * qL]), np.array([(1/3) * qL, (-2/3) * qL]),
            np.array([(-1/3) * qL, (2/3) * qL]), np.array([(1/3) * qL, (1/3) * qL]),
            [(-1/4) * qL, (1/4) * qL, 0 * qL],
            None,
            [
                [
                    r'\frac{2}{3}qL + \left(\frac{s - \left(-\frac{1}{3}qL\right)}{\frac{1}{3}qL - \left(-\frac{1}{3}qL\right)}\right)\left(\frac{1}{3}qL - \frac{2}{3}qL\right)',
                    0.3,
                    1
                ],
                [
                    r'\frac{2}{3}qL + \left(\frac{s + \frac{1}{3}qL}{\frac{2}{3}qL}\right)\left(-\frac{1}{3}qL\right)',
                    0.5,
                    1
                ],
                [
                    r'\frac{2}{3}qL - \frac{1}{2}s - \frac{1}{6}qL',
                    0.5,
                    1
                ],
                [
                    r'\frac{1}{2}(qL - s)',
                    0.75,
                    1
                ]
            ],
            pre_bottom_tex,
            [
                [
                    r'-\frac{1}{3}qL + \left(\frac{s - \left(-\frac{1}{3}qL\right)}{\frac{1}{3}qL - \left(-\frac{1}{3}qL\right)}\right)\left(-\frac{2}{3}qL - \left(-\frac{1}{3}qL\right)\right)',
                    0.3,
                    1
                ],
                [
                    r'-\frac{1}{3}qL + \left(\frac{s + \frac{1}{3}qL}{\frac{2}{3}qL}\right)\left(-\frac{1}{3}qL\right)',
                    0.5,
                    0.1
                ],
                [
                    r'-\frac{1}{3}qL - \frac{1}{2}s - \frac{1}{6}qL',
                    0.5,
                    0.1
                ],
                [
                    r'-\frac{1}{2}(qL + s)',
                    1,
                    0.1
                ]
            ],
            None,
            [
                [
                    r'\frac{1}{2}(qL - s) - \left(-\frac{1}{2}(qL + s)\right)',
                    1,
                    3
                ],
                [
                    r'\frac{1}{2}(qL - s + qL + s)',
                    1,
                    2
                ],
                [
                    'qL',
                    1,
                    2
                ]
            ],
            a_dot_tex_dir=np.array([math.sqrt(2)/2, math.sqrt(2)/2, 0]),
            b_dot_tex_shift=[0, -0.3, 0],
            h_tex_shift=[0, -0.5, 0],
        )

    def calculate_t_from_s_3(self, outer_hexagon):
        qL = math.sqrt(3) * self.radius

        self.play(
            Transform(outer_hexagon.texs[1], outer_hexagon.texs[1].copy().next_to(outer_hexagon.dots[1], UP)),
            Transform(outer_hexagon.texs[2], outer_hexagon.texs[2].copy().next_to(outer_hexagon.dots[2], np.array([math.sqrt(2)/2, math.sqrt(2)/2, 0])))
        )

        self._calculate_t_from_s(
            np.array([(1/3) * qL, (-2/3) * qL]), np.array([(2/3) * qL, (-1/3) * qL]),
            np.array([(1/3) * qL, (1/3) * qL]), np.array([(2/3) * qL, (-1/3) * qL]),
            [(5/12) * qL, (7/12) * qL, (1/2) * qL],
            None,
            [
                [
                    r'\frac{1}{3}qL + \left(\frac{s - \frac{1}{3}qL}{\frac{2}{3}qL - \frac{1}{3}qL}\right)\left(-\frac{1}{3}qL - \frac{1}{3}qL\right)',
                    0.3,
                    0.1
                ],
                [
                    r'\frac{1}{3}qL + \left(\frac{s - \frac{1}{3}qL}{\frac{1}{3}qL}\right)\left(-\frac{2}{3}qL\right)',
                    0.5,
                    0.1
                ],
                [
                    r'\frac{1}{3}qL - 2s + \frac{2}{3}qL',
                    0.75,
                    0.1
                ],
                [
                    'qL - 2s',
                    1,
                    0.1
                ]
            ],
            None,
            [
                [
                    r'-\frac{2}{3}qL + \left(\frac{s - \frac{1}{3}qL}{\frac{2}{3}qL - \frac{1}{3}qL}\right)\left(-\frac{1}{3}qL - \left(-\frac{2}{3}qL\right)\right)',
                    0.3,
                    0.1
                ],
                [
                    r'-\frac{2}{3}qL + \left(\frac{s - \frac{1}{3}qL}{\frac{1}{3}qL}\right)\left(\frac{1}{3}qL\right)',
                    0.5,
                    0.1
                ],
                [
                    r'-\frac{2}{3}qL + s - \frac{1}{3}qL',
                    0.75,
                    0.1
                ],
                [
                    '-qL + s',
                    1,
                    0.1
                ]
            ],
            None,
            [
                [
                    r'(qL - 2s) - (-qL + s)',
                    0.5,
                    0.1
                ],
                [
                    r'2qL - 3s',
                    1,
                    2
                ]
            ],
            h_brace_dir=LEFT,
            a_dot_tex_dir=np.array([math.sqrt(2)/2, math.sqrt(2)/2, 0]),
            a_dot_tex_shift=np.array([0, 0.3, 0]),
            b_dot_tex_dir=np.array([math.sqrt(2)/2, -math.sqrt(2)/2, 0]),
        )

        self.play(
            Transform(outer_hexagon.texs[1], outer_hexagon.texs[1].copy().next_to(outer_hexagon.dots[1], RIGHT)),
            Transform(outer_hexagon.texs[2], outer_hexagon.texs[2].copy().next_to(outer_hexagon.dots[2], RIGHT))
        )

    def _calculate_t_from_s(
        self, bottom_start, bottom_end, top_start, top_end,
        animate_points, pre_top_tex, top_texs, pre_bottom_tex, bottom_texs,
        pre_height_texs, height_texs,
        a_dot_tex_dir = np.array([-1, 1, 0]),
        a_dot_tex_shift = ORIGIN,
        b_dot_tex_dir = np.array([-1, -1, 0]),
        b_dot_tex_shift = ORIGIN,
        h_brace_dir = RIGHT,
        h_tex_shift = ORIGIN
    ):
        top_texs = [
            [
                r'\text{above}(s) = \text{?}',
                0.75,
                2
            ]
        ] + top_texs + [
            [
                r'\left(s, ' + top_texs[-1][0] + r'\right)',
                1,
                3
            ]
        ]
        bottom_texs = [
            [
                r'\text{below}(s) = \text{?}',
                0.75,
                2
            ]
        ] + bottom_texs + [
            [
                r'\left(s, ' + bottom_texs[-1][0] + r'\right)',
                1,
                3
            ]
        ]
        height_texs = [
            [
                r'\text{height}(s) = \text{?}',
                0.75,
                2
            ]
        ] + height_texs

        qL = math.sqrt(3) * self.radius
        s_tracker = ValueTracker(animate_points[-1])

        def calculate_along(start, end, s):
            delta = end - start
            alpha = (s - start[0]) / delta[0]
            return (start + alpha * delta)[1]

        def calculate_bottom(s):
            return calculate_along(bottom_start, bottom_end, s)

        def calculate_top(s):
            return calculate_along(top_start, top_end, s)

        h_line = Line()
        def h_line_updater(x):
            s = s_tracker.get_value()
            bottom = calculate_bottom(s)
            top = calculate_top(s)

            return x.become(Line([s, bottom, 0], [s, top, 0]).set_color(NEON_GREEN))

        h_line_updater(h_line)

        h_brace = Brace(h_line)
        def h_brace_updater(x):
            return x.become(Brace(h_line_updater(Line()), h_brace_dir).set_color(NEON_GREEN))

        h_brace_updater(h_brace)

        h_tex = MathTex(r'\text{height}(s)').set_color(NEON_GREEN)
        def h_tex_updater(x):
            x_cp = x.copy()
            h_brace_updater(Brace(Line())).put_at_tip(x_cp)
            return x.become(x_cp.shift(h_tex_shift))

        h_tex_updater(h_tex)

        b_dot = Dot().set_color(NEON_GREEN)
        def b_dot_updater(x):
            s = s_tracker.get_value()
            bottom = calculate_bottom(s)
            return x.move_to([s, bottom, 0])

        b_dot_updater(b_dot)

        b_dot_tex = MathTex(r'(s, \text{below}(s))').set_color(NEON_GREEN)
        def b_dot_tex_updater(x):
            return x.next_to(b_dot_updater(Dot()), b_dot_tex_dir).shift(b_dot_tex_shift)

        b_dot_tex_updater(b_dot_tex)

        a_dot = Dot().set_color(NEON_GREEN)
        def a_dot_updater(x):
            s = s_tracker.get_value()
            top = calculate_top(s)
            return x.move_to([s, top, 0])
        a_dot_updater(a_dot)

        a_dot_tex = MathTex(r'(s, \text{above}(s))').set_color(NEON_GREEN)
        def a_dot_tex_updater(x):
            return x.next_to(a_dot_updater(Dot()), a_dot_tex_dir).shift(a_dot_tex_shift)

        a_dot_tex_updater(a_dot_tex)

        self.play(
            GrowFromCenter(h_line),
            GrowFromCenter(b_dot), GrowFromCenter(b_dot_tex),
            GrowFromCenter(a_dot), GrowFromCenter(a_dot_tex)
        )
        self.wait()
        self.play(GrowFromCenter(h_brace), GrowFromCenter(h_tex))
        self.wait()

        h_line.add_updater(h_line_updater)
        h_brace.add_updater(h_brace_updater)
        h_tex.add_updater(h_tex_updater)
        b_dot.add_updater(b_dot_updater)
        b_dot_tex.add_updater(b_dot_tex_updater)
        a_dot.add_updater(a_dot_updater)
        a_dot_tex.add_updater(a_dot_tex_updater)

        for val in animate_points:
            self.play(s_tracker.animate.set_value(val))

        self.wait()

        h_line.remove_updater(h_line_updater)
        h_brace.remove_updater(h_brace_updater)
        h_tex.remove_updater(h_tex_updater)
        b_dot.remove_updater(b_dot_updater)
        b_dot_tex.remove_updater(b_dot_tex_updater)

        if pre_top_tex is not None:
            pre_top_tex()

        for (new_tex, new_scale, wait_time) in top_texs:
            tmp_a_dot_tex = MathTex(new_tex).scale(new_scale).next_to(a_dot, a_dot_tex_dir).shift(a_dot_tex_shift).set_color(NEON_GREEN)
            self.play(FadeTransform(a_dot_tex, tmp_a_dot_tex))
            if wait_time > 0:
                self.wait(wait_time)
            a_dot_tex = tmp_a_dot_tex

        if pre_bottom_tex is not None:
            pre_bottom_tex()

        for (new_tex, new_scale, wait_time) in bottom_texs:
            tmp_b_dot_tex = MathTex(new_tex).scale(new_scale).next_to(b_dot, b_dot_tex_dir).shift(b_dot_tex_shift).set_color(NEON_GREEN)
            self.play(FadeTransform(b_dot_tex, tmp_b_dot_tex))
            if wait_time > 0:
                self.wait(wait_time)
            b_dot_tex = tmp_b_dot_tex

        if pre_height_texs is not None:
            pre_height_texs()

        for (new_tex, new_scale, wait_time) in height_texs:
            tmp_h_tex = MathTex(new_tex).scale(new_scale).set_color(NEON_GREEN)
            h_brace.put_at_tip(tmp_h_tex)
            self.play(FadeTransform(h_tex, tmp_h_tex.shift(h_tex_shift)))
            if wait_time > 0:
                self.wait(wait_time)
            h_tex = tmp_h_tex

        self.play(
            ShrinkToCenter(h_line), ShrinkToCenter(h_brace), ShrinkToCenter(h_tex),
            ShrinkToCenter(a_dot), ShrinkToCenter(a_dot_tex),
            ShrinkToCenter(b_dot), ShrinkToCenter(b_dot_tex)
        )


class TransformedHexagon:
    def __init__(self, center, radius, dots=False, labels=False):
        self.center = np.array(center)
        self.radius = float(radius)

        self.vertices = self.calc_vertices()
        self.lines = self.canonical_lines()

        if dots:
            self.dots = self.canonical_dots()
        else:
            self.dots = []

        if labels:
            self.texs = self.canonical_texs()
        else:
            self.texs = []

    def calc_vertices(self):
        center_xy = BASIS @ self.center[:2]

        res = []
        for angle in range(0, 360, 60):
            coord_xy = np.array((center_xy[0] + self.radius * math.cos(angle * DEGREES), center_xy[1] + self.radius * math.sin(angle * DEGREES)))
            coord_st = INV_BASIS @ coord_xy
            res.append(np.array([coord_st[0], coord_st[1], 0]))
        return res

    def children(self):
        return [*self.lines, *self.dots, *self.texs]

    def canonical_lines(self):
        return [
            Line(self.vertices[idx], self.vertices[(idx+1)%6])
            for idx in range(6)
        ]

    def canonical_dots(self):
        return [Dot(vert) for vert in self.vertices]

    def canonical_texs(self):
        reference_dot = Dot(ORIGIN)
        return [
            MathTex(tex).scale(0.75).next_to(reference_dot, dir).shift(vert)
            for (tex, dir, vert) in zip(
                [
                    r'\left(-\frac{1}{3}, \frac{2}{3}\right)qL',
                    r'\left(\frac{1}{3}, \frac{1}{3}\right)qL',
                    r'\left(\frac{2}{3}, -\frac{1}{3}\right)qL',
                    r'\left(\frac{1}{3}, -\frac{2}{3}\right)qL',
                    r'\left(-\frac{1}{3}, -\frac{1}{3}\right)qL',
                    r'\left(-\frac{2}{3}, \frac{1}{3}\right)qL'
                ],
                [UP, RIGHT, RIGHT, DOWN, LEFT, LEFT],
                self.vertices
            )
        ]
