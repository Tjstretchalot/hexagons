from manim import *
from transformed_hexagon_math import TransformedHexagon, BASIS, INV_BASIS
import math

class QEvenIndexer(Scene):
    def construct(self):
        self.radius = 4 / math.sqrt(3)
        self.height = math.sqrt(3) * self.radius

        outer_hexagon = self.add_transformed_hexagon()
        q_even_tex = self.replace_q_with_6k(outer_hexagon)
        self.wait()
        self.show_indexes(outer_hexagon)

    def add_transformed_hexagon(self):
        hex = TransformedHexagon(ORIGIN, self.radius, dots=True, labels=True)
        self.add(*hex.children())
        return hex

    def replace_q_with_6k(self, outer_hexagon):
        tex = MathTex(r'\text{assume } \exists k \in \mathbb{Z} | q = 6k').scale(2 / 3).next_to(np.array([-6, 3.25, 0]), RIGHT)
        self.play(GrowFromCenter(tex))
        self.wait(2)

        tmp_tex = MathTex('q = 6k').next_to(np.array([-6, 3.25, 0]), RIGHT)
        self.play(FadeTransform(tex, tmp_tex))
        self.wait()

        return tmp_tex

    def show_indexes(self, outer_hexagon):
        vals = WrappedKTracker(self.radius, 1)

        hexes_by_st_coord = {}
        needed_hexes = set()
        ctr = 0
        hex_grow_anims = []

        def add_hexes(s_idx, top_t, bot_t, dry_run=False, label=None):
            nonlocal ctr
            if label is None:
                label = int(vals.get_k()) == 1

            top_t_idx = round_toward_zero(top_t / vals.get_L())
            bot_t_idx = round_toward_zero(bot_t / vals.get_L())

            for t_idx in range(bot_t_idx, top_t_idx + 1):
                if dry_run:
                    needed_hexes.add((s_idx, t_idx))
                    continue

                # the set is strictly for when reusing hexes in animations; NOT
                # required for getting unique (s_idx, t_idx) pairs otherwise
                if (s_idx, t_idx) in hexes_by_st_coord:
                    hex = hexes_by_st_coord[(s_idx, t_idx)]
                    if label:
                        hex.create_label(str(ctr))
                        hex_grow_anims.append([GrowFromCenter(hex.label)])
                    ctr += 1
                    continue

                hex = InnerTransformedHexagon(s_idx, t_idx, vals)
                hexes_by_st_coord[(s_idx, t_idx)] = hex
                if label:
                    hex.create_label(str(ctr))
                    hex_grow_anims.append([*[Create(line) for line in hex.lines], GrowFromCenter(hex.label)])
                else:
                    hex_grow_anims.append([Create(line) for line in hex.lines])

                ctr += 1

        def add_all_hexes(group_size=1, anim_speed=1, dry_run=False, label=None):
            for s_idx in range(int(-vals.get_k() * 4), int(-vals.get_k() * 2) + 1):
                s = s_idx * vals.get_L()
                top_t = vals.get_q() * vals.get_L() + s
                bot_t = -vals.get_q() * vals.get_L() - 2 * s
                add_hexes(s_idx, top_t, bot_t, dry_run=dry_run, label=label)

            for s_idx in range(int(-vals.get_k() * 2) + 1, int(vals.get_k() * 2) + 1):
                s = s_idx * vals.get_L()
                top_t = (vals.get_q() * vals.get_L() - s) / 2
                bot_t = -(vals.get_q() * vals.get_L() + s) / 2
                add_hexes(s_idx, top_t, bot_t, dry_run=dry_run, label=label)

            for s_idx in range(int(vals.get_k() * 2) + 1, int(vals.get_k() * 4) + 1):
                s = s_idx * vals.get_L()
                top_t = vals.get_q() * vals.get_L() - 2 * s
                bot_t = -vals.get_q() * vals.get_L() + s
                add_hexes(s_idx, top_t, bot_t, dry_run=dry_run, label=label)

            for start_idx in range(0, len(hex_grow_anims), group_size):
                arrs = hex_grow_anims[start_idx:start_idx + group_size]
                merged = []
                for arr in arrs:
                    merged.extend(arr)
                self.play(*merged, run_time=1 / anim_speed)

            hex_grow_anims.clear()

        def hide_labels():
            anims = [ShrinkToCenter(hex.label) for hex in hexes_by_st_coord.values() if hex.label is not None]
            if not anims:
                return
            self.play(*anims)
            for hex in hexes_by_st_coord.values():
                hex.label = None

        for idx, k in enumerate([1, 2, 3, 1]):
            if hexes_by_st_coord:
                hide_labels()
                needed_hexes.clear()
                old_k = vals.get_k()
                vals.k_tracker.set_value(k)
                add_all_hexes(dry_run=True)
                vals.k_tracker.set_value(old_k)

                anims = []
                new_hexes_by_st_coord = {}
                for coord, hex in hexes_by_st_coord.items():
                    if coord not in needed_hexes:
                        for line in hex.lines:
                            anims.append(ShrinkToCenter(line))
                    else:
                        new_hexes_by_st_coord[coord] = hex

                if anims:
                    self.play(*anims)
                    hexes_by_st_coord = new_hexes_by_st_coord

                og_hexes = tuple(hexes_by_st_coord.values())
                for hex in og_hexes:
                    hex.add_updaters()
                self.play(vals.k_tracker.animate.set_value(k))
                for hex in og_hexes:
                    hex.remove_updaters()

            ctr = 0
            add_all_hexes(anim_speed=4 * k, group_size=k, label=idx == 0)
            self.wait()

        anims = []
        for coord, hex in hexes_by_st_coord.items():
            for line in hex.lines:
                anims.append(ShrinkToCenter(line))

        self.play(*anims)


class WrappedKTracker:
    def __init__(self, radius, initial_value=1):
        self.radius = radius
        self.canonical_outer_hexagon = TransformedHexagon(ORIGIN, self.radius)
        self.canonical_outer_normals = self.calc_canonical_outer_normals()
        self.k_tracker = ValueTracker(initial_value)

    def calc_canonical_outer_normals(self):
        res = []
        for idx in range(6):
            start = self.canonical_outer_hexagon.vertices[idx]
            end = self.canonical_outer_hexagon.vertices[(idx+1) % 6]

            halfway = (start + end) / 2
            unit_v = end - start
            unit_v /= np.linalg.norm(unit_v)

            norm_v = np.cross(np.cross(unit_v, -halfway), unit_v)
            norm_v /= np.linalg.norm(norm_v)

            res.append((halfway, norm_v))

        return res


    def get_value(self) -> float:
        return self.k_tracker.get_value()

    def get_k(self) -> float:
        return self.get_value()

    def get_q(self) -> float:
        return self.get_k() * 6

    def get_inner_radius(self) -> float:
        return self.radius / self.get_q()

    def get_inner_height(self) -> float:
        return (math.sqrt(3)/2) * self.get_inner_radius()

    def get_L(self) -> float:
        return math.sqrt(3) * self.get_inner_radius()


class InnerTransformedHexagon:
    def __init__(self, s_idx: int, t_idx: int, k_tracker: WrappedKTracker):
        self.s_idx = s_idx
        self.t_idx = t_idx
        self.k_tracker = k_tracker
        self.updaters = []

        self.lines = self.canonical_lines()
        self.label = None

    @property
    def center(self):
        return np.array([self.s_idx * self.k_tracker.get_L(), self.t_idx * self.k_tracker.get_L(), 0])

    @property
    def radius(self):
        return self.k_tracker.get_inner_radius()

    @property
    def vertices(self):
        center = self.center
        radius = self.radius
        center_xy = BASIS @ center[:2]

        res = []
        for angle in range(0, 360, 60):
            coord_xy = np.array((center_xy[0] + radius * math.cos(angle * DEGREES), center_xy[1] + radius * math.sin(angle * DEGREES)))
            coord_st = INV_BASIS @ coord_xy
            res.append(np.array([coord_st[0], coord_st[1], 0]))
        return res

    def vertex_within_outer_hexagon(self, vert):
        for (halfway, norm) in self.k_tracker.canonical_outer_normals:
            if np.dot(vert - halfway, norm) < -1e-6:
                return False

        return True

    @property
    def visual_center(self):
        return np.average(
            np.array([
                *[
                    vert for vert in self.vertices
                    if self.vertex_within_outer_hexagon(vert)
                ],
                self.center
            ]),
            0
        )

    def canonical_line(self, idx, verts=None):
        verts = verts or self.vertices
        line = Line(verts[idx], verts[(idx + 1) % 6])
        if not self.vertex_within_outer_hexagon(line.get_start()) or not self.vertex_within_outer_hexagon(line.get_end()):
            line.fade(1)
        return line

    def canonical_lines(self):
        verts = self.vertices
        return [self.canonical_line(idx, verts=verts) for idx in range(6)]

    def children(self):
        return self.lines.copy()

    def create_line_updater(self, idx):
        def updater(x):
            return x.become(self.canonical_line(idx))

        return updater

    def add_updaters(self):
        assert not self.updaters

        for (idx, line) in enumerate(self.lines):
            self.updaters.append([line, self.create_line_updater(idx)])

        for (mobj, upd) in self.updaters:
            mobj.add_updater(upd)

    def remove_updaters(self):
        for (mobj, upd) in self.updaters:
            mobj.remove_updater(upd)
        self.updaters = []

    def create_label(self, idx: int) -> MathTex:
        self.label = MathTex(str(idx)).scale(0.5).shift(self.visual_center)
        return self.label


def round_toward_zero(x: float) -> int:
    if abs(x - int(x)) == 0.5:
        return int(x)

    return round(x)
