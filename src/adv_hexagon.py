from manim import *
import math


class AdvancedHexagon(Scene):
    def construct(self):
        self.radius = 3

        outer_hexagon = self.add_outer_hexagon()
        (q_hex, q_brace, q_tex, q_tracker, r_tracker, updaters) = self.define_q()
        q_eqn_tex = self.eqn_radius_in_q()
        self.geometrical_radius_in_q(q_hex, q_tracker)
        self.play(q_tracker.animate.set_value(6))
        self.geometrical_radius_in_q(q_hex, q_tracker)
        self.define_basis(q_tracker)
        for mobj, upd in updaters:
            mobj.remove_updater(upd)
        q_hex.remove_updaters()
        self.play(ShrinkToCenter(q_brace), ShrinkToCenter(q_tex), ShrinkToCenter(q_eqn_tex))
        self.calculate_corners_in_basis(outer_hexagon)
        self.play(*[ShrinkToCenter(mobj) for mobj in q_hex.children()])
        self.transform_hexagon_in_basis(outer_hexagon, q_tracker)
        self.show_transformed_normals(outer_hexagon)
        self.show_transformed_contains(outer_hexagon)
        # self.transform_back(outer_hexagon)

    def add_outer_hexagon(self):
        res = Hexagon(ORIGIN, self.radius, dots=True, labels=True)
        self.add(*res.children())
        self.wait()
        return res

    def define_q(self):
        q = ValueTracker(4)
        radius_tracker = QToRadiusTracker(q, self.radius)
        hex = Hexagon(ORIGIN, radius_tracker.get_value())

        self.play(*[Create(mobj) for mobj in hex.children()])

        brace = Brace(hex.lines[1], direction=UP)
        tex = MathTex(r'\frac{1}{q}r').scale(0.75)
        brace.put_at_tip(tex)

        self.play(GrowFromCenter(brace), GrowFromCenter(tex))

        def brace_updater(x):
            return x.become(Brace(hex.lines[1], direction=UP))

        def tex_updater(x):
            cp_x = x.copy()
            brace.put_at_tip(cp_x)
            return x.become(cp_x)

        hex.add_updaters(radius_tracker)
        brace.add_updater(brace_updater)
        tex.add_updater(tex_updater)

        self.play(q.animate.set_value(3))
        self.play(q.animate.set_value(7))
        self.play(q.animate.set_value(5))
        self.wait()

        brace.remove_updater(brace_updater)

        self.play(Transform(brace, Brace(hex.lines[-2], direction=DOWN)))
        self.wait()

        def brace_updater(x):
            return x.become(Brace(hex.lines[-2], direction=DOWN))

        brace.add_updater(brace_updater)


        return (hex, brace, tex, q, radius_tracker, [(brace, brace_updater), (tex, tex_updater)])

    def eqn_radius_in_q(self):
        tex = MathTex(r'r = \frac{1}{q}r \cdot q').shift([0, 1.5, 0])
        self.play(GrowFromCenter(tex))
        self.wait(2)

        self.play(MoveAlongPath(tex, Line([0, 1.5, 0], [0, 3.2, 0])))
        self.play(ScaleInPlace(tex, 0.75))
        self.wait()
        return tex

    def geometrical_radius_in_q(self, c_hex, q_tracker):
        inner_radius = self.radius / q_tracker.get_value()
        inner_height = inner_radius * (math.sqrt(3) / 2)
        q = int(q_tracker.get_value())

        brace = Brace(c_hex.lines[2], direction=LEFT)
        brace_tex = MathTex(r'\frac{\sqrt{3}}{2}\frac{1}{q}r').scale(0.75)
        brace.put_at_tip(brace_tex)
        self.play(GrowFromCenter(brace), GrowFromCenter(brace_tex))
        self.wait(2)

        tmp_line = Line([-inner_radius, inner_height, 0], [-inner_radius, -inner_height, 0])
        tmp_brace = Brace(tmp_line, direction=LEFT)
        tmp_brace_tex = MathTex(r'\frac{\sqrt{3}}{2}\frac{1}{q}r\cdot 2').scale(0.75)
        tmp_brace.put_at_tip(tmp_brace_tex)
        self.play(Transform(brace, tmp_brace), FadeTransform(brace_tex, tmp_brace_tex))
        brace_tex = tmp_brace_tex
        self.wait(2)

        tmp_brace_tex = MathTex(r'\sqrt{3}\frac{1}{q}r').scale(0.75)
        brace.put_at_tip(tmp_brace_tex)
        self.play(FadeTransform(brace_tex, tmp_brace_tex))
        brace_tex = tmp_brace_tex

        y_shift_tracker = ValueTracker(0)
        def brace_updater(x):
            tmp_line = Line([-inner_radius, inner_height + y_shift_tracker.get_value(), 0], [-inner_radius, -inner_height + y_shift_tracker.get_value(), 0])
            return x.become(Brace(tmp_line, direction=LEFT))

        def brace_tex_updater(x):
            cp_x = x.copy()
            brace.put_at_tip(cp_x)
            return x.become(cp_x)

        brace.add_updater(brace_updater)
        brace_tex.add_updater(brace_tex_updater)

        height_hexes = []

        for i in range(int(q/2)):
            self.play(y_shift_tracker.animate.set_value(inner_height*2*i + inner_height))

            dot = Dot([0, inner_height * 2 * (i+1), 0])
            self.play(GrowFromCenter(dot))
            hex = Hexagon([0, inner_height * 2 * (i+1), 0], inner_radius)
            if (i+1) * 2 == q:
                hex.lines = [hex.lines[3], hex.lines[5]]
            self.play(*[Create(mobj) for mobj in hex.children()])
            self.play(ShrinkToCenter(dot))
            height_hexes.append(hex)

        brace.remove_updater(brace_updater)
        brace_tex.remove_updater(brace_tex_updater)
        self.play(ShrinkToCenter(brace), ShrinkToCenter(brace_tex))

        counter_texes = []
        for i in range(q):
            counter_tex = MathTex(str(int(i)+1)).scale(0.5).next_to([-inner_radius, inner_height * i + inner_height / 2, 0], LEFT)
            self.play(GrowFromCenter(counter_tex))
            counter_texes.append(counter_tex)

        show_q_tex = MathTex(f'q={q}').next_to([inner_radius, inner_height, 0], RIGHT)
        self.play(GrowFromCenter(show_q_tex))
        self.wait()

        anims = []
        for hhex in height_hexes:
            anims.extend([ShrinkToCenter(c) for c in hhex.children()])

        anims.extend([ShrinkToCenter(c) for c in counter_texes])
        anims.append(ShrinkToCenter(show_q_tex))
        self.play(*anims)
        self.wait()

    def define_basis(self, q_tracker):
        s = UP
        s_arrow = Arrow(ORIGIN, s, buff=0)
        s_tex = MathTex(r'\vec{s} = \langle 0, 1 \rangle').scale(0.75).next_to(s_arrow.get_end(), LEFT)

        self.play(Create(s_arrow), GrowFromCenter(s_tex))

        t = np.array([math.cos(30 * DEGREES), math.sin(30 * DEGREES), 0])
        t_arrow = Arrow(ORIGIN, t, buff=0)
        t_tex = MathTex(r'\vec{t} = \langle \cos(30^\circ), \sin(30^\circ) \rangle').scale(0.5).next_to(t_arrow.get_end(), RIGHT)

        self.play(Create(t_arrow), GrowFromCenter(t_tex))
        self.wait(2)

        tmp_t_tex = MathTex(r'\vec{t} = \left\langle \frac{\sqrt{3}}{2}, \frac{1}{2} \right\rangle').scale(0.5).next_to(t_arrow.get_end(), RIGHT)
        self.play(FadeTransform(t_tex, tmp_t_tex))
        t_tex = tmp_t_tex

        p = np.array([1.2, 1.5, 0])
        p_dot = Dot(p)
        p_tex = MathTex(r'\mathbf{p}').scale(0.75).next_to(p_dot, RIGHT)

        self.play(Create(p_dot), GrowFromCenter(p_tex))
        self.wait(2)

        self.play(ShrinkToCenter(t_tex), ShrinkToCenter(s_tex), ShrinkToCenter(p_tex))

        p_rebased = switch_basis(p, s, t)
        self.play(
            Transform(s_arrow, Arrow(ORIGIN, s * p_rebased[0], buff=0)),
            Transform(t_arrow, Arrow(ORIGIN, t * p_rebased[1], buff=0))
        )
        self.play(
            MoveAlongPath(s_arrow, Line(ORIGIN + s_arrow.get_center(), t * p_rebased[1] + s_arrow.get_center()))
        )

        self.wait(2)

        px_tracker = ValueTracker(p[0])
        py_tracker = ValueTracker(p[1])

        def p_dot_updater(x):
            p = np.array((px_tracker.get_value(), py_tracker.get_value(), 0))
            return x.become(Dot(p))

        def p_tex_updater(x):
            p = np.array((px_tracker.get_value(), py_tracker.get_value(), 0))
            return x.become(x.copy().next_to(Dot(p), RIGHT))

        def t_arrow_updater(x):
            p = np.array((px_tracker.get_value(), py_tracker.get_value(), 0))
            p_rebased = switch_basis(p, s, t)
            if p_rebased[1] == 0:
                return x.scale(0).set_opacity(0)
            return x.become(Arrow(ORIGIN, t * p_rebased[1], buff=0))

        def s_arrow_updater(x):
            p = np.array((px_tracker.get_value(), py_tracker.get_value(), 0))
            p_rebased = switch_basis(p, s, t)
            if p_rebased[0] == 0:
                return x.scale(0).set_opacity(0)
            return x.become(Arrow(t * p_rebased[1], p, buff=0))

        p_dot.add_updater(p_dot_updater)
        p_tex.add_updater(p_tex_updater)
        t_arrow.add_updater(t_arrow_updater)
        s_arrow.add_updater(s_arrow_updater)

        self.play(px_tracker.animate.set_value(-1.2), py_tracker.animate.set_value(1.7))
        self.wait(0.5)
        self.play(px_tracker.animate.set_value(-1.6), py_tracker.animate.set_value(-2))
        self.wait(0.5)
        self.play(px_tracker.animate.set_value(1.6), py_tracker.animate.set_value(-1.5))
        self.wait(0.5)
        self.play(px_tracker.animate.set_value(1.2), py_tracker.animate.set_value(1.5))
        self.wait()



        inner_radius = self.radius / q_tracker.get_value()
        inner_height = (math.sqrt(3) / 2) * inner_radius
        length = inner_height * 2

        s_term = r'\sqrt{3}\frac{1}{q}r\vec{s}'
        t_term = r'\sqrt{3}\frac{1}{q}r\vec{t}'
        for (i, j) in [
            (1, 0), (2, 0), (3, 0), (3, -1), (4, -1), (4, -2),
            (1, 0), (1, 1), (1, 2), (2, 2)
        ]:
            p = length * i * s + length * j * t

            tmp_p_tex = (
                MathTex(pretty_linear(pretty_linear('0', str(i), s_term), str(j), t_term))
                .scale(0.75).next_to(p_dot, RIGHT)
            )
            tmp_p_tex.add_updater(p_tex_updater)
            self.play(
                px_tracker.animate.set_value(p[0]),
                py_tracker.animate.set_value(p[1]),
                FadeTransform(p_tex, tmp_p_tex)
            )
            p_tex = tmp_p_tex
            self.wait()

        p_dot.remove_updater(p_dot_updater)
        p_tex.remove_updater(p_tex_updater)
        t_arrow.remove_updater(t_arrow_updater)
        s_arrow.remove_updater(s_arrow_updater)

        self.play(
            FadeOut(s_arrow), FadeOut(t_arrow),
            ShrinkToCenter(p_dot), ShrinkToCenter(p_tex)
        )
        self.wait()

    def calculate_corners_in_basis(self, outer_hexagon):
        s = UP
        s_arrow = Arrow(ORIGIN, s, buff=0)
        s_tex = MathTex(r'\vec{s} = \langle 0, 1 \rangle').scale(0.75).next_to(s_arrow.get_end(), LEFT)

        self.play(Create(s_arrow), GrowFromCenter(s_tex))

        t = np.array([math.cos(30 * DEGREES), math.sin(30 * DEGREES), 0])
        t_arrow = Arrow(ORIGIN, t, buff=0)
        t_tex = MathTex(r'\vec{t} = \langle \frac{\sqrt{3}}{2}, \frac{1}{2} \rangle').scale(0.5).next_to(t_arrow.get_end(), RIGHT)

        self.play(Create(t_arrow), GrowFromCenter(t_tex))
        self.wait(2)
        self.play(
            FadeOut(s_arrow), FadeOut(t_arrow),
            Transform(s_tex, s_tex.copy().move_to([-3.5, 1.7, 0])),
            Transform(t_tex, t_tex.copy().move_to([-3.75, 1.0, 0]))
        )
        self.wait()

        l_tex = MathTex(r'L = \sqrt{3}\frac{1}{q}r').move_to([-3.75, -1.5, 0])

        for idx, steps in enumerate([
            [
                r'(r, 0) = a\sqrt{3}\frac{1}{q}r\vec{s} + b\sqrt{3}\frac{1}{q}r\vec{t}',
                [
                    r'r = a\sqrt{3}\frac{1}{q}r\cdot 0 + b \sqrt{3}\frac{1}{q}r\cdot \frac{\sqrt{3}}{2}',
                    r'0 = a\sqrt{3}\frac{1}{q}r\cdot 1 + b \sqrt{3}\frac{1}{q}r\cdot \frac{1}{2}'
                ],
                [
                    r'r = b\frac{3}{2q}r',
                    r'0 = a\frac{\sqrt{3}}{q}r + b \frac{\sqrt{3}}{2q}r'
                ],
                [
                    r'1 = b\frac{3}{2q}',
                    r'0 = a + b \frac{\sqrt{3}}{2q}r \cdot \frac{q}{\sqrt{3}r}'
                ],
                [
                    r'b = \frac{2q}{3}',
                    r'a = -b \frac{1}{2}'
                ],
                [
                    r'b = \frac{2q}{3}',
                    r'a = -\frac{q}{3}'
                ],
                r'-\frac{q}{3} \sqrt{3}\frac{1}{q}r\vec{s} + \frac{2q}{3}\sqrt{3}\frac{1}{q}r\vec{t}',
                r'-\frac{q}{3} L\vec{s} + \frac{2q}{3} L\vec{t}'
            ],
            [
                r'\left(\frac{1}{2}r, \frac{\sqrt{3}}{2}r\right) = a\sqrt{3}\frac{1}{q}r\vec{s} + b\sqrt{3}\frac{1}{q}r\vec{t}',
                [
                    r'\frac{1}{2}r = a \sqrt{3}\frac{1}{q}r \cdot 0 + b\sqrt{3}\frac{1}{q}r \cdot \frac{\sqrt{3}}{2}',
                    r'\frac{\sqrt{3}}{2}r = a\sqrt{3}\frac{1}{q}r\cdot 1 + b\sqrt{3}\frac{1}{q}r\cdot \frac{1}{2}'
                ],
                [
                    r'\frac{1}{2}r = \frac{3b}{2q}r',
                    r'\frac{\sqrt{3}}{2}r = \frac{\sqrt{3}a}{q}r + \frac{\sqrt{3}b}{2q}r'
                ],
                [
                    r'1 = \frac{3b}{q}',
                    r'1 = \frac{2a}{q} + \frac{b}{q}'
                ],
                [
                    r'b = \frac{q}{3}',
                    r'q = 2a + b'
                ],
                [
                    r'b = \frac{q}{3}',
                    r'2a = q - \frac{q}{3}'
                ],
                [
                    r'b = \frac{q}{3}',
                    r'a = \frac{q}{3}'
                ],
                r'\frac{q}{3}L\vec{s} + \frac{q}{3}L\vec{t}'
            ],
            [
                r'\left(-\frac{1}{2}r, \frac{\sqrt{3}}{2}r) = a\sqrt{3}\frac{1}{q}r\vec{s} + b\sqrt{3}\frac{1}{q}r\vec{t}',
                [
                    r'-\frac{1}{2}r = a\sqrt{3}\frac{1}{q}r\cdot 0 + b\sqrt{3}\frac{1}{q}r \cdot \frac{\sqrt{3}}{2}',
                    r'\frac{\sqrt{3}}{2}r = a\sqrt{3}\frac{1}{q}r\cdot 1 + b\sqrt{3}\frac{1}{q}r\cdot \frac{1}{2}'
                ],
                [
                    r'-\frac{1}{2}r = \frac{3b}{2q}r',
                    r'\frac{\sqrt{3}}{2}r = \frac{\sqrt{3}a}{q}r + \frac{\sqrt{3}b}{2q}r'
                ],
                [
                    r'1 = -\frac{3b}{q}',
                    r'1 = \frac{2a}{q} + \frac{b}{q}'
                ],
                [
                    r'b = -\frac{q}{3}',
                    r'a = \frac{q}{2} - \frac{b}{2}'
                ],
                [
                    r'b = -\frac{q}{3}',
                    r'a = \frac{q}{2} + \frac{q}{6}'
                ],
                [
                    r'b = -\frac{q}{3}',
                    r'a = \frac{2q}{3}'
                ],
                r'\frac{2q}{3}L\vec{s} - \frac{q}{3}L\vec{t}'
            ],
            [
                r'(-r, 0) = a\sqrt{3}\frac{1}{q}r\vec{s} + b\sqrt{3}\frac{1}{q}r\vec{t}',
                [
                    r'-r = a\sqrt{3}\frac{1}{q}r\cdot 0 + b\sqrt{3}\frac{1}{q}r \cdot \frac{\sqrt{3}}{2}',
                    r'0 = a\sqrt{3}\frac{1}{q}r\cdot 1 + b\sqrt{3}\frac{1}{q}r\cdot \frac{1}{2}'
                ],
                [
                    r'-r = \frac{3b}{2q}r',
                    r'0 = \frac{\sqrt{3}a}{q}r + \frac{\sqrt{3}b}{2q}r'
                ],
                [
                    r'1 = -\frac{3b}{2q}',
                    r'0 = a + \frac{b}{2}'
                ],
                [
                    r'b = -\frac{2q}{3}',
                    r'a = -\frac{b}{2}'
                ],
                [
                    r'b = -\frac{2q}{3}',
                    r'a = \frac{q}{3}'
                ],
                r'\frac{q}{3}L\vec{s} - \frac{2q}{3}L\vec{t}'
            ],
            [
                r'\left(-\frac{1}{2}r, -\frac{\sqrt{3}}{2}r\right) = a\sqrt{3}\frac{1}{q}r\vec{s} + b\sqrt{3}\frac{1}{q}r\vec{t}',
                [
                    r'-\frac{1}{2}r = a\sqrt{3}\frac{1}{q}r\cdot 0 + b\sqrt{3}\frac{1}{q}r \cdot \frac{\sqrt{3}}{2}',
                    r'-\frac{\sqrt{3}}{2}r = a\sqrt{3}\frac{1}{q}r\cdot 1 + b\sqrt{3}\frac{1}{q}r\cdot \frac{1}{2}'
                ],
                [
                    r'-\frac{1}{2}r = \frac{3b}{2q}r',
                    r'-\frac{\sqrt{3}}{2}r = \frac{\sqrt{3}a}{q}r + \frac{\sqrt{3}b}{2q}r'
                ],
                [
                    r'1 = -\frac{3b}{q}',
                    r'1 = -\frac{2a}{q} - \frac{b}{q}'
                ],
                [
                    r'b = -\frac{q}{3}',
                    r'q = -2a - b'
                ],
                [
                    r'b = -\frac{q}{3}',
                    r'2a = -b - q'
                ],
                [
                    r'b = -\frac{q}{3}',
                    r'2a = \frac{q}{3} - q'
                ],
                [
                    r'b = -\frac{q}{3}',
                    r'a = -\frac{q}{3}'
                ],
                r'-\frac{q}{3}L\vec{s} - \frac{q}{3}L\vec{t}'
            ],
            [
                r'\left(\frac{1}{2}r, -\frac{\sqrt{3}}{2}r\right) = a\sqrt{3}\frac{1}{q}r\vec{s} + b\sqrt{3}\frac{1}{q}r\vec{t}',
                [
                    r'\frac{1}{2}r = a \sqrt{3}\frac{1}{q}r \cdot 0 + b\sqrt{3}\frac{1}{q}r \cdot \frac{\sqrt{3}}{2}',
                    r'-\frac{\sqrt{3}}{2}r = a\sqrt{3}\frac{1}{q}r\cdot 1 + b\sqrt{3}\frac{1}{q}r\cdot \frac{1}{2}'
                ],
                [
                    r'\frac{1}{2}r = \frac{3b}{2q}r',
                    r'-\frac{\sqrt{3}}{2}r = \frac{\sqrt{3}a}{q}r + \frac{\sqrt{3}b}{2q}r'
                ],
                [
                    r'1 = \frac{3b}{q}',
                    r'1 = -\frac{2a}{q} - \frac{b}{q}'
                ],
                [
                    r'b = \frac{q}{3}',
                    r'q = -2a - b'
                ],
                [
                    r'b = \frac{q}{3}',
                    r'2a = -b - q'
                ],
                [
                    r'b = \frac{q}{3}',
                    r'2a = -\frac{q}{3} - q'
                ],
                [
                    r'b = \frac{q}{3}',
                    r'a = -\frac{2q}{3}'
                ],
                r'-\frac{2q}{3}L\vec{s} + \frac{q}{3}L\vec{t}'
            ]
        ]):
            p_tex = outer_hexagon.texs[idx]
            p_tex_2 = None
            self.play(Transform(p_tex, p_tex.copy().move_to([0, 1.5, 0])))
            self.wait()
            for step in steps:
                if isinstance(step, str):
                    p_tex_tmp = MathTex(step).scale(0.5).move_to([0, 1.5, 0])
                    if p_tex_2 is None:
                        self.play(FadeTransform(p_tex, p_tex_tmp))
                    else:
                        self.play(FadeTransform(p_tex, p_tex_tmp), ShrinkToCenter(p_tex_2))
                        p_tex_2 = None
                    p_tex = p_tex_tmp
                else:
                    p_tex_tmp = MathTex(step[0]).scale(0.5).move_to([0, 1.8, 0])
                    p_tex_2_tmp = MathTex(step[1]).scale(0.5).move_to([0, 1.2, 0])

                    if p_tex_2 is None:
                        self.play(FadeTransform(p_tex, p_tex_tmp), GrowFromCenter(p_tex_2_tmp))
                    else:
                        self.play(FadeTransform(p_tex, p_tex_tmp), FadeTransform(p_tex_2, p_tex_2_tmp))

                    p_tex = p_tex_tmp
                    p_tex_2 = p_tex_2_tmp

                self.wait(4 if idx == 0 else 1)

            if p_tex_2 is not None:
                self.play(ShrinkToCenter(p_tex_2))
                p_tex_2 = None

            p_tex_tmp = p_tex.copy().next_to(outer_hexagon.dots[idx], [RIGHT, RIGHT, LEFT, LEFT, DOWN, DOWN][idx])
            self.play(FadeTransform(p_tex, p_tex_tmp))
            outer_hexagon.texs[idx] = p_tex_tmp
            if idx == 0:
                self.play(GrowFromCenter(l_tex))

        self.play(ShrinkToCenter(l_tex), ShrinkToCenter(s_tex), ShrinkToCenter(t_tex))

    def transform_hexagon_in_basis(self, outer_hexagon, q_tracker):
        vertex_starts = [
            np.array([self.radius * math.cos(angle * DEGREES), self.radius * math.sin(angle * DEGREES)])
            for angle in range(0, 360, 60)
        ]
        basis = np.array([
            [0, math.cos(30 * DEGREES)],
            [1, math.sin(30 * DEGREES)]
        ])
        inv_basis = np.linalg.inv(basis)
        q = q_tracker.get_value()
        inner_radius = self.radius / q
        L = math.sqrt(3) * inner_radius
        # L * q = math.sqrt(3) * (self.radius / q) * q = math.sqrt(3) * self.radius
        vertex_ends = [
            ((inv_basis @ vertex) / (L * q)) * 4
            for vertex in vertex_starts
        ]

        tex_dirs_initial = [RIGHT, RIGHT, LEFT, LEFT, DOWN, DOWN]
        tex_dirs_final = [UP, RIGHT, RIGHT, DOWN, LEFT, LEFT]

        reference_dot = Dot(ORIGIN)
        tex_starts = [
            tex.copy().next_to(reference_dot, dir).shift(project_2_to_3(vert)).get_center()
            for (tex, dir, vert) in zip(outer_hexagon.texs, tex_dirs_initial, vertex_starts)
        ]
        tex_ends = [
            tex.copy().next_to(reference_dot, dir).shift(project_2_to_3(vert)).get_center()
            for (tex, dir, vert) in zip(outer_hexagon.texs, tex_dirs_final, vertex_ends)
        ]

        alpha = ValueTracker(0)

        def create_updaters(idx):
            line_start_initial = vertex_starts[idx]
            line_start_finish = vertex_ends[idx]
            line_start_delta = line_start_finish - line_start_initial

            line_end_initial = vertex_starts[(idx + 1) % 6]
            line_end_finish = vertex_ends[(idx + 1) % 6]
            line_end_delta = line_end_finish - line_end_initial

            tex_initial = tex_starts[idx]
            tex_finish = tex_ends[idx]
            tex_delta = tex_finish - tex_initial

            def dot_updater(x):
                return x.become(Dot(project_2_to_3(line_start_initial + line_start_delta * alpha.get_value())))

            def line_updater(x):
                return x.become(
                    Line(
                        project_2_to_3(line_start_initial + line_start_delta * alpha.get_value()),
                        project_2_to_3(line_end_initial + line_end_delta * alpha.get_value())
                    )
                )

            def tex_updater(x):
                return x.become(x.copy().move_to(tex_initial + tex_delta * alpha.get_value()))

            return [
                (outer_hexagon.dots[idx], dot_updater),
                (outer_hexagon.lines[idx], line_updater),
                (outer_hexagon.texs[idx], tex_updater)
            ]

        alpha_updaters = []
        for idx in range(6):
            new_updaters = create_updaters(idx)
            for (mobj, updater) in new_updaters:
                mobj.add_updater(updater)
            alpha_updaters.extend(new_updaters)

        self.play(alpha.animate.set_value(1))

        for (mobj, updater) in alpha_updaters:
            mobj.remove_updater(updater)

        anims = []
        new_texs = []
        for (tex, dot, dir, new_label) in zip(outer_hexagon.texs, outer_hexagon.dots, tex_dirs_final, [
            r'\left(-\frac{1}{3}, \frac{2}{3}\right)qL',
            r'\left(\frac{1}{3}, \frac{1}{3}\right)qL',
            r'\left(\frac{2}{3}, -\frac{1}{3}\right)qL',
            r'\left(\frac{1}{3}, -\frac{2}{3}\right)qL',
            r'\left(-\frac{1}{3}, -\frac{1}{3}\right)qL',
            r'\left(-\frac{2}{3}, \frac{1}{3}\right)qL'
        ]):
            tmp_tex = MathTex(new_label).scale(0.5).next_to(dot, dir)
            new_texs.append(tmp_tex)
            anims.append(FadeTransform(tex, tmp_tex))

        self.play(*anims)
        outer_hexagon.texs = new_texs

        s_arrow = Arrow(ORIGIN, RIGHT, buff=0)
        s_tex = MathTex(r'\vec{s}').next_to(s_arrow, RIGHT)
        t_arrow = Arrow(ORIGIN, UP, buff=0)
        t_tex = MathTex(r'\vec{t}').next_to(t_arrow, UP)
        self.play(
            FadeIn(s_arrow), GrowFromCenter(s_tex),
            FadeIn(t_arrow), GrowFromCenter(t_tex)
        )
        self.wait(4)
        self.play(
            FadeOut(s_arrow), ShrinkToCenter(s_tex),
            FadeOut(t_arrow), ShrinkToCenter(t_tex)
        )
        self.wait()

    def show_transformed_normals(self, outer_hexagon):
        for (idx, (texs, dot_texs)) in enumerate([
            (
                [
                    r'\langle -\frac{1}{3}qL, -\frac{2}{3}qL \rangle',
                    r'\langle -1, -2 \rangle'
                ],
                [
                    r'\frac{1}{2}\left(\left(-\frac{1}{3},\frac{2}{3}\right)qL + \left(\frac{1}{3}, \frac{1}{3}\right)qL\right)',
                    r'\frac{1}{6}qL \left(0, 1\right)'
                ]
            ),
            (
                [
                    r'\langle -\frac{2}{3}qL, -\frac{1}{3}qL \rangle',
                    r'\langle -2, -1 \rangle'
                ],
                [
                    r'\frac{1}{2}\left(\left(\frac{1}{3}, \frac{1}{3}\right)qL + \left(\frac{2}{3}, -\frac{1}{3}\right)qL\right)',
                    r'\frac{1}{6}qL \left(1, 0\right)'
                ]
            ),
            (
                [
                    r'\langle -\frac{1}{3}qL, \frac{1}{3}qL \rangle',
                    r'\langle -1, 1 \rangle',
                ],
                [
                    r'\frac{1}{2}\left(\left(\frac{2}{3}, -\frac{1}{3}\right)qL + \left(\frac{1}{3}, -\frac{2}{3}\right)qL\right)',
                    r'\frac{1}{6}qL \left(1, -1\right)'
                ]
            ),
            (
                [
                    r'\langle \frac{1}{3}qL, \frac{2}{3}qL \rangle',
                    r'\langle 1, 2 \rangle'
                ],
                [
                    r'\frac{1}{2}\left(\left(\frac{1}{3}, -\frac{2}{3}\right)qL + \left(-\frac{1}{3}, -\frac{1}{3}\right)qL\right)',
                    r'\frac{1}{6}qL \left(0, -1\right)'
                ]
            ),
            (
                [
                    r'\langle \frac{2}{3}qL, \frac{1}{3}qL \rangle',
                    r'\langle 2, 1 \rangle'
                ],
                [
                    r'\frac{1}{2}\left(\left(-\frac{1}{3}, -\frac{1}{3}\right)qL + \left(-\frac{2}{3}, \frac{1}{3}\right)qL\right)',
                    r'\frac{1}{6}qL \left(-1, 0\right)'
                ]
            ),
            (
                [
                    r'\langle \frac{1}{3}, -\frac{1}{3} \rangle',
                    r'\langle 1, -1 \rangle'
                ],
                [
                    r'\frac{1}{2}\left(\left(-\frac{2}{3}, \frac{1}{3}\right)qL + \left(-\frac{1}{3}, \frac{2}{3}\right)qL\right)',
                    r'\frac{1}{6}qL \left(-1, 1\right)'
                ]
            ),
        ]):
            start = outer_hexagon.dots[idx].get_center()
            end = outer_hexagon.dots[(idx + 1) % 6].get_center()

            halfway = (start + end) / 2
            unit_v = end - start
            unit_v /= np.linalg.norm(unit_v)

            norm_v = np.cross(np.cross(unit_v, -halfway), unit_v)
            norm_v /= np.linalg.norm(norm_v)

            arrow = Arrow(halfway, halfway + norm_v, buff=0)
            tex = MathTex(texs[0]).scale(0.5).next_to(arrow, norm_v)

            dot = Dot(halfway)
            dot_tex = MathTex(dot_texs[0]).scale(0.5).next_to(dot, -norm_v)
            self.play(FadeIn(arrow), GrowFromCenter(tex), GrowFromCenter(dot), GrowFromCenter(dot_tex))
            for inner_idx in range(1, max(len(texs), len(dot_texs))):
                anims = []
                if inner_idx < len(texs):
                    tmp_tex = MathTex(texs[inner_idx]).scale(0.5).next_to(arrow, norm_v)
                    anims.append(FadeTransform(tex, tmp_tex))
                    tex = tmp_tex
                if inner_idx < len(dot_texs):
                    tmp_tex = MathTex(dot_texs[inner_idx]).scale(0.5).next_to(dot, -norm_v)
                    anims.append(FadeTransform(dot_tex, tmp_tex))
                    dot_tex = tmp_tex
                self.wait()
                self.play(*anims)

            self.wait()
            self.play(ShrinkToCenter(tex), FadeOut(arrow), ShrinkToCenter(dot), ShrinkToCenter(dot_tex))

    def show_transformed_contains(self, outer_hexagon):
        line_centers = []
        normal_vs = []
        for idx in range(6):
            start = outer_hexagon.dots[idx].get_center()
            end = outer_hexagon.dots[(idx + 1) % 6].get_center()
            halfway = (start + end) / 2
            unit_v = end - start
            unit_v /= np.linalg.norm(unit_v)
            norm_v = np.cross(np.cross(unit_v, -halfway), unit_v)
            norm_v /= np.linalg.norm(norm_v)
            line_centers.append(halfway)
            normal_vs.append(norm_v)

        px_tracker = ValueTracker(0)
        py_tracker = ValueTracker(0)
        arrows = []
        arrow_updaters = []

        def make_arrow(base, dir):
            proj = np.dot(-base, dir) * dir
            arrow = Arrow(base, base + proj, buff=0).set_color(GREEN)
            def arrow_updater(x):
                p = np.array((px_tracker.get_value(), py_tracker.get_value(), 0))
                length = np.dot(p - base, dir)
                proj = length * dir
                return x.become(Arrow(base, base + proj, buff=0).set_color(GREEN if length >= 0 else RED))
            return [arrow, arrow_updater]

        for base, dir in zip(line_centers, normal_vs):
            a, upd = make_arrow(base, dir)
            arrows.append(a)
            arrow_updaters.append(upd)


        p_dot = Dot(ORIGIN)
        self.play(GrowFromCenter(p_dot))
        self.play(*[FadeIn(a) for a in arrows])
        self.wait()

        def p_dot_updater(x):
            return x.become(Dot([px_tracker.get_value(), py_tracker.get_value(), 0]))

        p_dot.add_updater(p_dot_updater)
        for a, upd in zip(arrows, arrow_updaters):
            a.add_updater(upd)

        for (s, t, w) in [[-1, 0, 1], [0, 1, 1], [0, 4, 1], [1, -3.5, 1], [3.5, 1.5, 1], [0, 0, 0], [-2, 0, 1], [-2.5, 0, 2], [2, 0, 1], [2.5, 0, 2], [0, 0, 1]]:
            self.play(px_tracker.animate.set_value(s), py_tracker.animate.set_value(t))
            if w > 0:
                self.wait(w)

        p_dot.remove_updater(p_dot_updater)
        for a, upd in zip(arrows, arrow_updaters):
            a.remove_updater(upd)

        self.play(ShrinkToCenter(p_dot), *[FadeOut(a) for a in arrows])

    def transform_back(self, outer_hexagon):
        tmp_hexagon = Hexagon(ORIGIN, self.radius, dots=True, labels=True)

        self.play(
            *[Transform(og_line, new_line) for (og_line, new_line) in zip(outer_hexagon.lines, tmp_hexagon.lines)],
            *[Transform(og_dot, new_dot) for (og_dot, new_dot) in zip(outer_hexagon.dots, tmp_hexagon.dots)],
            *[Transform(og_tex, new_tex) for (og_tex, new_tex) in zip(outer_hexagon.texs, tmp_hexagon.texs)]
        )


class Hexagon:
    def __init__(self, center, radius, dots=False, labels=False, center_tex=None, radius_tex='r') -> None:
        if center_tex is None:
            center_tex = [pretty_float(i) for i in center]

        self.radius = radius
        self.center = center

        vertices = tuple(
            (center[0] + radius * math.cos(angle * DEGREES), center[1] + radius * math.sin(angle * DEGREES), center[2])
            for angle in range(0, 360, 60)
        )

        if dots:
            self.dots = [Dot(vert) for vert in vertices]
        else:
            self.dots = []

        self.lines = [Line(vertices[i], vertices[(i+1) % len(vertices)]) for i in range(len(vertices))]

        self.texs = []
        if labels:
            reference_dot = Dot(ORIGIN)
            self.texs = [
                MathTex(
                    pretty_coords(
                        pretty_linear(center_tex[0], pretty_cos(angle), radius_tex),
                        pretty_linear(center_tex[1], pretty_sin(angle), radius_tex)
                    )
                ).scale(0.75).next_to(vert, direction=direction).shift(reference_dot.get_critical_point(direction))
                for (angle, vert, direction) in zip(range(0, 360, 60), vertices, [RIGHT, RIGHT, LEFT, LEFT, DOWN, DOWN])
            ]

        self.tracker_pairs = []

    def children(self):
        return [*self.lines, *self.dots, *self.texs]

    def add_updaters(self, r_tracker, x_tracker=None, y_tracker=None):
        if x_tracker is None:
            x_tracker = ValueTracker(self.center[0])
        if y_tracker is None:
            y_tracker = ValueTracker(self.center[1])

        for angle, line in zip(range(0, 360, 60), self.lines):
            updater = self.create_line_updater(angle, r_tracker, x_tracker, y_tracker)
            self.tracker_pairs.append((line, updater))
            line.add_updater(updater)

    def remove_updaters(self):
        for (mobj, upd) in self.tracker_pairs:
            mobj.remove_updater(upd)

        self.tracker_pairs = []

    def create_line_updater(self, angle, r_tracker, x_tracker, y_tracker):
        def updater(x):
            radius = r_tracker.get_value()
            center_x = x_tracker.get_value()
            center_y = y_tracker.get_value()
            center_z = 0
            return x.become(Line(
                (center_x + radius * math.cos(angle * DEGREES), center_y + radius * math.sin(angle * DEGREES), center_z),
                (center_x + radius * math.cos((angle+60) * DEGREES), center_y + radius * math.sin((angle+60) * DEGREES), center_z)
            ))
        return updater


def pretty_sin(angle):
    sqrt_3_over_2 = r'\frac{\sqrt{3}}{2}'
    return {
        0: '0',
        60: sqrt_3_over_2,
        120: sqrt_3_over_2,
        180: '0',
        240: f'-{sqrt_3_over_2}',
        300: f'-{sqrt_3_over_2}'
    }[angle]


def pretty_cos(angle):
    one_half = r'\frac{1}{2}'
    return {
        0: '1',
        60: one_half,
        120: f'-{one_half}',
        180: '-1',
        240: f'-{one_half}',
        300: one_half
    }[angle]


def pretty_linear(a, b, x):
    if a == '0' and b == '0':
        return '0'

    if a == '0':
        if b == '1':
            return x
        if b == '-1':
            return f'-{x}'
        return f'{b}{x}'

    if b == '0':
        return str(a)

    if b == '1':
        return f'{a}+{x}'

    if b == '-1':
        return f'{a}-{x}'

    if b[0] == '-':
        return f'{a}{b}{x}'

    return f'{a} + {b}{x}'


def pretty_coords(x, y):
    return f'\\left({x}, {y}\\right)'


def pretty_float(f):
    if f == int(f):
        return str(int(f))
    return str(f)


class QToRadiusTracker:
    def __init__(self, q_tracker, radius):
        self.q_tracker = q_tracker
        self.radius = radius

    def get_value(self):
        return self.radius / self.q_tracker.get_value()


# switch from p=(x, y) to (a, b) in the basis [s, t]
def switch_basis(p, s, t):
    # (x, y) = a(s1, s2) + b(t1, t2)
    #
    # |x| = |s1, t1| |a|
    # |y|   |s2, t2| |b|
    #
    # X = BA
    # B^-1 X = A

    return np.linalg.inv(np.array([s[:2], t[:2]]).T) @ np.array(p[:2])


def project_2_to_3(twod):
    return np.array((twod[0], twod[1], 0))
