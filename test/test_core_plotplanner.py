import random
import unittest

from PIL import Image, ImageDraw

from meerk40t.core.cutcode import CutCode, LaserSettings, LineCut
from meerk40t.core.elements import LaserOperation
from meerk40t.core.plotplanner import PlotPlanner, Single
from meerk40t.device.basedevice import PLOT_AXIS, PLOT_SETTING
from meerk40t.svgelements import Circle, Path, Point, SVGImage


class TestPlotplanner(unittest.TestCase):

    def test_plotplanner_constant_move_x(self):
        """
        With raster_smooth set to 1 we should smooth the x axis so that no y=0 occurs.
        @return:
        """
        plan = PlotPlanner(LaserSettings(power=1000))
        settings = LaserSettings(power=1000)
        settings.constant_move_x = True
        plan.push(LineCut(Point(0, 0), Point(2, 20), settings=settings))
        plan.push(LineCut(Point(2, 20), Point(5, 20), settings=settings))
        plan.push(LineCut(Point(5, 20), Point(10, 100), settings=settings))
        last_x = None
        last_y = None
        for x, y, on in plan.gen():
            if on == 4:
                last_x = x
                last_y = y
            if on > 1:
                continue
            cx = x
            cy = y
            if cx is None:
                continue
            if last_x is not None:
                total_dx = cx - last_x
                total_dy = cy - last_y
                dx = 1 if total_dx > 0 else 0 if total_dx == 0 else -1
                dy = 1 if total_dy > 0 else 0 if total_dy == 0 else -1
                if x < 10:
                    self.assertFalse(dx == 0)
                for i in range(1, max(abs(total_dx), abs(total_dy))+1):
                    nx = last_x + (i * dx)
                    ny = last_y + (i * dy)
                    print(nx, ny, on)
            print(x, y, on)
            last_x = cx
            last_y = cy
            print(f"Moving to {x} {y}")

    def test_plotplanner_constant_move_y(self):
        """
        With smooth_raster set to 2 we should never have x = 0. The x should *always* be in motion.
        @return:
        """
        plan = PlotPlanner(LaserSettings(power=1000))
        settings = LaserSettings(power=1000)
        settings.constant_move_y = True
        plan.push(LineCut(Point(0, 0), Point(2, 20), settings=settings))
        plan.push(LineCut(Point(2, 20), Point(5, 20), settings=settings))
        plan.push(LineCut(Point(5, 20), Point(10, 100), settings=settings))
        last_x = None
        last_y = None
        for x, y, on in plan.gen():
            if on == 4:
                last_x = x
                last_y = y
            if on > 1:
                continue
            cx = x
            cy = y
            if cx is None:
                continue
            if last_x is not None:
                total_dx = cx - last_x
                total_dy = cy - last_y
                dx = 1 if total_dx > 0 else 0 if total_dx == 0 else -1
                dy = 1 if total_dy > 0 else 0 if total_dy == 0 else -1
                self.assertFalse(dy == 0)
                for i in range(0, max(abs(total_dx), abs(total_dy))):
                    nx = last_x + (i * dx)
                    ny = last_y + (i * dy)
                    print(nx, ny, on)

            last_x = cx
            last_y = cy
            print(f"Moving to {x} {y}")

    def test_plotplanner_constant_move_xy(self):
        """
        With raster_smooth set to 1 we should smooth the x axis so that no y=0 occurs.
        @return:
        """
        plan = PlotPlanner(LaserSettings(power=1000))
        settings = LaserSettings(power=1000)
        settings.constant_move_x = True
        settings.constant_move_y = True
        for i in range(100):
            plan.push(LineCut(Point(random.randint(0, 1000), random.randint(0,1000)), Point(random.randint(0,1000), random.randint(0,1000)), settings=settings))
        last_x = None
        last_y = None
        for x, y, on in plan.gen():
            if on == 4:
                last_x = x
                last_y = y
            if on > 1:
                continue
            cx = x
            cy = y
            if cx is None:
                continue
            if last_x is not None:
                total_dx = cx - last_x
                total_dy = cy - last_y
                dx = 1 if total_dx > 0 else 0 if total_dx == 0 else -1
                dy = 1 if total_dy > 0 else 0 if total_dy == 0 else -1
                for i in range(1, max(abs(total_dx), abs(total_dy))+1):
                    nx = last_x + (i * dx)
                    ny = last_y + (i * dy)
                    # print(nx, ny, on)
            # print(x, y, on)
            last_x = cx
            last_y = cy
            print(f"Moving to {x} {y}")


    def test_plotplanner_flush(self):
        """
        Intro test for plotplanner.

        This is needlessly complex.

        final value is "on", and provides commands.
        128 means settings were changed.
        64 indicates x_axis major
        32 indicates x_dir, y_dir
        256 indicates ended.
        1 means cut.
        0 means move.

        :return:
        """
        plan = PlotPlanner(LaserSettings(power=1000))
        settings = LaserSettings(power=1000)
        for i in range(211):
            plan.push(LineCut(Point(0, 0), Point(5, 100), settings=settings))
            plan.push(LineCut(Point(100, 50), Point(0, 0), settings=settings))
            plan.push(
                LineCut(
                    Point(50, -50), Point(100, -100), settings=LaserSettings(power=0)
                )
            )
            q = 0
            for x, y, on in plan.gen():
                # print(x, y, on)
                if q == i:
                    # for x, y, on in plan.process_plots(None):
                    # print("FLUSH!", x, y, on)
                    plan.clear()
                    break
                q += 1

    def test_plotplanner_walk_raster(self):
        """
        Test plotplanner operation of walking to a raster.

        PLOT_FINISH = 256
        PLOT_RAPID = 4
        PLOT_JOG = 2
        PLOT_SETTING = 128
        PLOT_AXIS = 64
        PLOT_DIRECTION = 32
        PLOT_LEFT_UPPER = 512
        PLOT_RIGHT_LOWER = 1024

        1 means cut.
        0 means move.

        :return:
        """

        rasterop = LaserOperation(operation="Raster")
        svg_image = SVGImage()
        svg_image.image = Image.new("RGBA", (256, 256))
        draw = ImageDraw.Draw(svg_image.image)
        draw.ellipse((0, 0, 255, 255), "black")
        rasterop.add(svg_image, type="opnode")

        vectorop = LaserOperation(operation="Engrave")
        vectorop.add(Path(Circle(cx=127, cy=127, r=128, fill="black")), type="opnode")
        cutcode = CutCode()
        cutcode.extend(vectorop.as_cutobjects())
        cutcode.extend(rasterop.as_cutobjects())

        plan = PlotPlanner(LaserSettings(power=500))
        for c in cutcode.flat():
            plan.push(c)

        setting_changed = False
        for x, y, on in plan.gen():
            if on > 2:
                if setting_changed:
                    # Settings change happens at vector to raster switch and must repost the axis.
                    self.assertEqual(on, PLOT_AXIS)
                if on == PLOT_SETTING:
                    setting_changed = True
                else:
                    setting_changed = False
