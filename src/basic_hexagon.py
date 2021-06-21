from itertools import chain
import itertools
from manim import *
import math


class BasicHexagon(Scene):
    def construct(self):
        radius = 3

        # Show the center
        cog = Dot([0, 0, 0])
        origin_text = MathTex('(0, 0)').next_to(cog, DOWN)

        self.play(GrowFromCenter(cog))
        self.play(GrowFromCenter(origin_text))
        self.wait()

        # Draw the line to the first point on the right
        line = Line([0, 0, 0], [radius, 0, 0])
        self.play(Create(line))

        # Add the first dot
        hexagon_dots = [Dot([radius, 0, 0])]
        self.add(hexagon_dots[0])

        # Grow the brace defining r
        radius_brace = Brace(line)
        self.play(GrowFromCenter(radius_brace))

        # Show the text for the brace defining r
        radius_text = radius_brace.get_tex('r')
        self.play(GrowFromCenter(radius_text))

        # Show the location of the first point
        hexagon_dot_texts = [MathTex('(r, 0)').next_to(hexagon_dots[0], RIGHT)]
        self.play(GrowFromCenter(hexagon_dot_texts[0]))
        self.play(
            Transform(
                hexagon_dot_texts[0],
                MathTex(r'(r\cos(0^\circ), r\sin(0^\circ))').scale(0.5).next_to(hexagon_dots[0], RIGHT)
            )
        )

        # Shrink the base
        self.play(ShrinkToCenter(radius_brace), ShrinkToCenter(radius_text))

        self.wait()

        # Animate the second radial line to 60 degrees
        theta_tracker = ValueTracker(1)
        theta_line = line.copy().rotate(theta_tracker.get_value() * DEGREES, about_point=ORIGIN)
        theta_angle = Angle(line, theta_line, radius=0.5)

        self.add(theta_line, theta_angle)

        def theta_line_updater(x):
            return x.become(line.copy()).rotate(
                theta_tracker.get_value() * DEGREES, about_point=ORIGIN
            )

        theta_line.add_updater(theta_line_updater)

        def theta_angle_updater(x):
            return x.become(Angle(line, theta_line, radius=0.5))

        theta_angle.add_updater(theta_angle_updater)

        self.play(theta_tracker.animate.set_value(60))

        theta_tex = MathTex(r'60^\circ').move_to(
            Angle(line, theta_line, radius=0.5 + MED_LARGE_BUFF).point_from_proportion(0.5)
        )
        self.play(GrowFromCenter(theta_tex))

        def theta_tex_updater(x):
            return x.move_to(
                Angle(line, theta_line, radius=0.5 + MED_LARGE_BUFF).point_from_proportion(0.5)
            )

        theta_tex.add_updater(theta_tex_updater)

        hexagon_dots.append(Dot([radius * math.cos(60 * DEGREES), radius * math.sin(60 * DEGREES), 0]))
        hexagon_dot_texts.append(
            MathTex(r'(r\cos(60^\circ), r\sin(60^\circ))').scale(0.5).next_to(hexagon_dots[-1], RIGHT)
        )
        self.play(GrowFromCenter(hexagon_dots[-1]), GrowFromCenter(hexagon_dot_texts[-1]))

        # Animate the remaining points
        text_dir_by_angle = {
            0: RIGHT,
            60: RIGHT,
            120: LEFT,
            180: LEFT,
            240: DOWN,
            300: DOWN,
        }
        for angle in range(120, 360, 60):
            self.play(theta_tracker.animate.set_value(angle))
            self.play(Transform(theta_tex, MathTex(f'{angle}^\\circ').move_to(
                Angle(line, theta_line, radius=0.5 + MED_LARGE_BUFF).point_from_proportion(0.5)
            )))

            hexagon_dots.append(Dot([radius * math.cos(angle * DEGREES), radius * math.sin(angle * DEGREES), 0]))
            hexagon_dot_texts.append(
                MathTex(f'(r\\cos({angle}^\\circ), r\\sin({angle}^\\circ))').scale(0.5).next_to(hexagon_dots[-1], text_dir_by_angle[angle])
            )
            self.play(GrowFromCenter(hexagon_dots[-1]), GrowFromCenter(hexagon_dot_texts[-1]))

        theta_line.remove_updater(theta_line_updater)
        theta_angle.remove_updater(theta_angle_updater)
        theta_tex.remove_updater(theta_tex_updater)
        self.play(
            ShrinkToCenter(theta_line), ShrinkToCenter(line),
            ShrinkToCenter(cog), ShrinkToCenter(theta_tex),
            ShrinkToCenter(theta_angle), ShrinkToCenter(origin_text),
        )

        hexagon_lines = [
            Line(
                [radius * math.cos(angle * DEGREES), radius * math.sin(angle * DEGREES), 0],
                [radius * math.cos((angle + 60) * DEGREES), radius * math.sin((angle + 60) * DEGREES), 0],
            )
            for angle in range(0, 360, 60)
        ]
        for line in hexagon_lines:
            self.play(Create(line))

        # Simplify all the points
        simplified_cos = {
            0: 'r',
            60: '\\frac{1}{2}r',
            120: '-\\frac{1}{2}r',
            180: '-r',
            240: '-\\frac{1}{2}r',
            300: '\\frac{1}{2}r'
        }
        simplified_sin = {
            0: '0',
            60: '\\frac{\\sqrt{3}}{2}r',
            120: '\\frac{\\sqrt{3}}{2}r',
            180: '0',
            240: '-\\frac{\\sqrt{3}}{2}r',
            300: '-\\frac{\\sqrt{3}}{2}r'
        }

        tmp_hexagon_dot_texts = []
        for idx, angle in enumerate(range(0, 360, 60)):
            tmp_hexagon_dot_texts.append(
                MathTex(f'\\left({simplified_cos[angle]}, {simplified_sin[angle]}\\right)')
                .scale(0.75).next_to(hexagon_dots[idx], text_dir_by_angle[angle])
            )

        self.play(*[
            Transform(og, tmp) for og, tmp in zip(hexagon_dot_texts, tmp_hexagon_dot_texts)
        ])
        tmp_hexagon_dot_texts = None

        # Brace & calculate line length at first line
        line_length_brace = Brace(hexagon_lines[0], direction=hexagon_lines[0].copy().rotate(PI / 2).get_unit_vector())
        self.play(GrowFromCenter(line_length_brace))
        self.wait()

        slanted_line_tex = MathTex(r'\sqrt{\left(r - \frac{1}{2}r\right)^2 + \left(0 - \frac{\sqrt{3}}{2}r\right)^2}').scale(0.5)
        line_length_brace.put_at_tip(slanted_line_tex)
        self.play(GrowFromCenter(slanted_line_tex))
        self.wait(5)

        for (new_val, scale, delay) in [
            [r'\sqrt{\left(\frac{1}{2}r\right)^2 + \left(-\frac{\sqrt{3}}{2}r\right)^2', 0.5, 5],
            [r'\sqrt{\frac{1}{4}r^2 + \frac{3}{4}r^2}', 0.5, 5],
            [r'\sqrt{r^2}', 1, 3],
            ['r', 1, 5]
        ]:
            tmp_slanted_line_tex = MathTex(new_val).scale(scale)
            line_length_brace.put_at_tip(tmp_slanted_line_tex)
            self.play(FadeTransform(slanted_line_tex, tmp_slanted_line_tex))
            slanted_line_tex = tmp_slanted_line_tex
            self.wait(delay)

        self.play(
            ShrinkToCenter(line_length_brace),
            MoveAlongPath(slanted_line_tex, Line(slanted_line_tex.get_center(), line_length_brace.get_center()))
        )
        self.wait()

        # Brace & calculate the second line length quickly as it's pretty obvious
        line_length_brace = Brace(hexagon_lines[1], direction=DOWN)
        self.play(GrowFromCenter(line_length_brace))

        top_line_tex = MathTex(r'\sqrt{\left(-\frac{1}{2}r - \frac{1}{2}r\right)^2 + \left(\frac{\sqrt{3}}{2}r - \frac{\sqrt{3}}{2}r\right)^2}').scale(0.5)
        line_length_brace.put_at_tip(top_line_tex)
        self.play(GrowFromCenter(top_line_tex))
        self.wait()

        for new_val, scale in [[r'\sqrt{(-r)^2 + (0)^2}', 0.5], [r'\sqrt{r^2}', 1], ['r', 1]]:
            tmp_top_line_tex = MathTex(new_val).scale(scale)
            line_length_brace.put_at_tip(tmp_top_line_tex)
            self.play(FadeTransform(top_line_tex, tmp_top_line_tex))
            top_line_tex = tmp_top_line_tex
            self.wait(2)

        self.play(
            ShrinkToCenter(line_length_brace),
            MoveAlongPath(top_line_tex, Line(top_line_tex.get_center(), line_length_brace.get_center()))
        )
        self.wait(3)

        self.play(ShrinkToCenter(top_line_tex), ShrinkToCenter(slanted_line_tex))
        self.wait()

        # Show the half-height of the hexagon quickly
        line_length_brace = Brace(hexagon_lines[0], direction=LEFT)
        self.play(GrowFromCenter(line_length_brace))
        self.wait(3)
        tex = MathTex(r'\frac{\sqrt{3}}{2}r')
        line_length_brace.put_at_tip(tex)
        self.play(GrowFromCenter(tex))
        self.wait(3)
        self.play(ShrinkToCenter(line_length_brace), ShrinkToCenter(tex))


        inner_hex_radius = radius / 3
        inner_hex_lines = self.make_hex_lines(center=ORIGIN, radius=inner_hex_radius)
        self.play(*[Create(line) for line in inner_hex_lines])

        line_length_brace = Brace(inner_hex_lines[1], direction=UP)
        top_line_tex = MathTex(r'\frac{1}{3}r').scale(0.5)
        line_length_brace.put_at_tip(top_line_tex)
        self.play(GrowFromCenter(line_length_brace), GrowFromCenter(top_line_tex))

        self.wait(3)

        inner_hex_lines_2 = [line.copy() for line in inner_hex_lines]
        self.add(*inner_hex_lines_2)
        self.play(*[
            MoveAlongPath(line, Line(line.get_center(), line.get_center() + [(2/3) * radius, 0, 0]))
            for line in inner_hex_lines_2
        ])

        self.wait(3)

        x_lines = [
            Line([0, 2/3 * radius, 0], [radius, -2/3 * radius, 0]).set_color(RED_A),
            Line([radius, 2/3 * radius, 0], [0, -2/3 * radius, 0]).set_color(RED_A)
        ]
        self.play(*[Create(line) for line in x_lines])
        self.wait(3)
        self.play(
            *[ShrinkToCenter(line) for line in x_lines],
            *[ShrinkToCenter(line) for line in inner_hex_lines_2]
        )
        self.wait()

        line = Line(ORIGIN, [radius, 0, 0])
        theta_line = Line(ORIGIN, [radius * math.cos(30 * DEGREES), radius * math.sin(30 * DEGREES), 0])
        theta_angle = Angle(line, theta_line, 1.5)
        theta_tex = MathTex(r'30^\circ').scale(0.75).move_to(
            Angle(line, theta_line, 2).point_from_proportion(0.5)
        )

        self.play(
            Create(line), Create(theta_line),
            Create(theta_angle), GrowFromCenter(theta_tex)
        )

        self.wait(5)
        self.play(
            ShrinkToCenter(line), ShrinkToCenter(theta_line),
            ShrinkToCenter(theta_angle), ShrinkToCenter(theta_tex)
        )
        self.wait()

        inner_hex_height = inner_hex_radius * math.sqrt(3) / 2
        theta_line = Line(ORIGIN, [0, inner_hex_height, 0])
        self.play(Create(theta_line))

        theta_brace = Brace(theta_line, direction=RIGHT)
        self.play(GrowFromCenter(theta_brace))

        theta_tex = MathTex(r'\frac{\sqrt{3}}{2} \cdot \frac{1}{3}r')
        theta_brace.put_at_tip(theta_tex)
        self.play(GrowFromCenter(theta_tex))
        self.wait()

        tmp_theta_tex = MathTex(r'\frac{\sqrt{3}}{6}r')
        theta_brace.put_at_tip(tmp_theta_tex)
        self.play(Transform(theta_tex, tmp_theta_tex))

        theta_tracker = ValueTracker(90)
        def theta_line_updater(x):
            rads = theta_tracker.get_value() * DEGREES
            return x.become(Line(ORIGIN, [inner_hex_height * math.cos(rads), inner_hex_height * math.sin(rads), 0]))

        def theta_brace_updater(x):
            rads = theta_tracker.get_value() * DEGREES
            return x.become(Brace(theta_line, direction=[math.cos(rads - math.pi / 2), math.sin(rads - math.pi / 2), 0]))

        def theta_tex_updater(x):
            cp_x = x.copy()
            theta_brace.put_at_tip(cp_x)
            return x.become(cp_x)

        theta_line.add_updater(theta_line_updater)
        theta_brace.add_updater(theta_brace_updater)
        theta_tex.add_updater(theta_tex_updater)

        self.play(theta_tracker.animate.set_value(30))
        self.wait()

        theta_line.remove_updater(theta_line_updater)
        theta_brace.remove_updater(theta_brace_updater)
        theta_tex.remove_updater(theta_tex_updater)

        tmp_theta_line = Line(ORIGIN, [inner_hex_height * math.sqrt(3), inner_hex_height, 0])
        tmp_theta_brace = Brace(tmp_theta_line, direction=[math.cos(-60 * DEGREES), math.sin(-60 * DEGREES), 0])
        tmp_theta_tex = MathTex(r'\frac{\sqrt{3}}{6}r \cdot 2')
        tmp_theta_brace.put_at_tip(tmp_theta_tex)
        tiled_hex_2_cdot = Dot([inner_hex_height * math.sqrt(3), inner_hex_height, 0])
        self.play(
            Transform(theta_line, tmp_theta_line),
            Transform(theta_brace, tmp_theta_brace),
            Transform(theta_tex, tmp_theta_tex),
            GrowFromCenter(tiled_hex_2_cdot)
        )
        self.wait()

        tmp_theta_tex = MathTex(r'\frac{\sqrt{3}}{3}r')
        theta_brace.put_at_tip(tmp_theta_tex)
        self.play(Transform(theta_tex, tmp_theta_tex))

        tiled_hex_2_ctex = MathTex(r'\left(\frac{\sqrt{3}}{3}r\cos(30^\circ), \frac{\sqrt{3}}{3}r\sin(30^\circ)\right)').scale(0.5).next_to(tiled_hex_2_cdot, direction=UP).shift([2.5, 0, 0])
        self.play(GrowFromCenter(tiled_hex_2_ctex))
        self.wait(3)

        for (new_val, shift) in [
            [r'\left(\frac{\sqrt{3}}{3}r\cdot\frac{\sqrt{3}}{2}, \frac{\sqrt{3}}{3}r\cdot\frac{1}{2}\right)', [2, 0, 0]],
            [r'\left(\frac{3}{6}r, \frac{\sqrt{3}}{6}r\right)', [-0.1, 0, 0]],
            [r'\left(\frac{1}{2}r, \frac{\sqrt{3}}{6}r\right)', [-0.3, 0, 0]]
        ]:
            tmp_tiled_hex_2_ctex = MathTex(new_val).scale(0.5).next_to(tiled_hex_2_cdot, direction=UP).shift(shift)
            self.play(FadeTransform(tiled_hex_2_ctex, tmp_tiled_hex_2_ctex))
            self.wait()
            tiled_hex_2_ctex = tmp_tiled_hex_2_ctex

        self.wait(2)
        inner_hex_lines_2 = self.make_hex_lines([0.5 * radius, (math.sqrt(3) / 6) * radius, 0], inner_hex_radius)
        self.play(
            ShrinkToCenter(tiled_hex_2_ctex), ShrinkToCenter(theta_brace),
            ShrinkToCenter(theta_tex), ShrinkToCenter(theta_line),
            ShrinkToCenter(tiled_hex_2_cdot),
            *[Create(line) for line in inner_hex_lines_2]
        )
        self.wait()

        inner_hexes_lines = [inner_hex_lines_2]
        for angle in range(90, 360, 60):
            inner_hexes_lines.append(
                self.make_hex_lines([
                    (math.sqrt(3)/3) * math.cos(angle * DEGREES) * radius,
                    (math.sqrt(3)/3) * math.sin(angle * DEGREES) * radius,
                    0
                ], inner_hex_radius)
            )
            self.play(*[Create(line) for line in inner_hexes_lines[-1]])

        self.wait()

        verify_line = Line(ORIGIN, [inner_hex_radius, 0, 0])
        verify_brace = Brace(verify_line, direction=DOWN)
        verify_tex = MathTex(r'\frac{1}{3}r').scale(0.5)
        verify_brace.put_at_tip(verify_tex)
        verify_tex.shift([0, -0.5, 0])

        self.play(
            ReplacementTransform(top_line_tex, verify_tex),
            ReplacementTransform(line_length_brace, verify_brace),
            Create(verify_line)
        )
        self.wait(2)

        offset_tracker = ValueTracker(0)
        def verify_line_updater(x):
            v = offset_tracker.get_value()
            return x.become(Line([v, 0, 0], [v+inner_hex_radius, 0, 0]))

        def verify_brace_updater(x):
            return x.become(Brace(verify_line, direction=DOWN))

        def verify_tex_updater(x):
            cp_x = x.copy()
            verify_brace.put_at_tip(cp_x)
            cp_x.shift([0, -0.5, 0])
            return x.become(cp_x)

        verify_line.add_updater(verify_line_updater)
        verify_brace.add_updater(verify_brace_updater)
        verify_tex.add_updater(verify_tex_updater)

        self.play(offset_tracker.animate.set_value(inner_hex_radius))
        self.wait(2)
        self.play(offset_tracker.animate.set_value(2*inner_hex_radius))
        self.wait(3)

        verify_line.remove_updater(verify_line_updater)
        verify_brace.remove_updater(verify_brace_updater)
        verify_tex.remove_updater(verify_tex_updater)

        self.play(
            ShrinkToCenter(verify_line), ShrinkToCenter(verify_brace), ShrinkToCenter(verify_tex),
            *[ShrinkToCenter(line) for line in itertools.chain(inner_hex_lines, *inner_hexes_lines)]
        )
        self.wait()

    def make_hex_lines(self, center, radius):
        return [
            Line(
                [center[0] + radius * math.cos(angle * DEGREES), center[1] + radius * math.sin(angle * DEGREES), center[2]],
                [center[0] + radius * math.cos((angle + 60) * DEGREES), center[1] + radius * math.sin((angle + 60) * DEGREES), center[2]]
            )
            for angle in range(0, 360, 60)
        ]
