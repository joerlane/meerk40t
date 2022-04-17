from copy import copy

from meerk40t.core.cutcode import (
    CubicCut,
    CutGroup,
    DwellCut,
    LineCut,
    QuadCut,
    RasterCut,
    PlotCut,
)
from meerk40t.core.node.node import Node
from meerk40t.core.parameters import Parameters
from meerk40t.core.units import Length
from meerk40t.image.actualize import actualize
from meerk40t.svgelements import (
    Close,
    Color,
    CubicBezier,
    Line,
    Move,
    Path,
    Polygon,
    QuadraticBezier,
    Shape,
    SVGElement,
    SVGImage, Matrix, Angle,
)
from meerk40t.tools.pathtools import VectorMontonizer, EulerianFill

MILS_IN_MM = 39.3701


class RasterOpNode(Node, Parameters):
    """
    Default object defining any raster operation done on the laser.

    This is a Node of type "op raster".
    """

    def __init__(self, *args, **kwargs):
        if "setting" in kwargs:
            kwargs = kwargs["settings"]
            if "type" in kwargs:
                del kwargs["type"]
        Node.__init__(self, *args, type="op raster", **kwargs)
        Parameters.__init__(self, None, **kwargs)
        self.settings.update(kwargs)
        self._status_value = "Queued"

        if len(args) == 1:
            obj = args[0]
            if isinstance(obj, SVGElement):
                self.add(obj, type="ref elem")
            elif hasattr(obj, "settings"):
                self.settings = dict(obj.settings)
            elif isinstance(obj, dict):
                self.settings.update(obj)

    def __repr__(self):
        return "RasterOp()"

    def __str__(self):
        parts = list()
        if not self.output:
            parts.append("(Disabled)")
        if self.default:
            parts.append("✓")
        if self.passes_custom and self.passes != 1:
            parts.append("%dX" % self.passes)
        parts.append("Raster{step}".format(step=self.raster_step))
        if self.speed is not None:
            parts.append("%gmm/s" % float(self.speed))
        if self.frequency is not None:
            parts.append("%gkHz" % float(self.frequency))
        if self.raster_swing:
            raster_dir = "-"
        else:
            raster_dir = "="
        if self.raster_direction == 0:
            raster_dir += "T2B"
        elif self.raster_direction == 1:
            raster_dir += "B2T"
        elif self.raster_direction == 2:
            raster_dir += "R2L"
        elif self.raster_direction == 3:
            raster_dir += "L2R"
        elif self.raster_direction == 4:
            raster_dir += "X"
        else:
            raster_dir += "%d" % self.raster_direction
        parts.append(raster_dir)
        if self.power is not None:
            parts.append("%gppi" % float(self.power))
        parts.append("±{overscan}".format(overscan=self.overscan))
        if self.acceleration_custom:
            parts.append("a:%d" % self.acceleration)
        return " ".join(parts)

    def __copy__(self):
        return RasterOpNode(self)

    def load(self, settings, section):
        settings.read_persistent_attributes(section, self)
        update_dict = settings.read_persistent_string_dict(section, suffix=True)
        self.settings.update(update_dict)
        self.validate()
        hexa = self.settings.get("hex_color")
        if hexa is not None:
            self.color = Color(hexa)
        self.notify_update()

    def save(self, settings, section):
        settings.write_persistent_attributes(section, self)
        settings.write_persistent(section, "hex_color", self.color.hexa)
        settings.write_persistent_dict(section, self.settings)

    def copy_children(self, obj):
        for element in obj.children:
            self.add(element.object, type="ref elem")

    def deep_copy_children(self, obj):
        for element in obj.children:
            self.add(copy(element.object), type="elem")

    def time_estimate(self):
        # TODO: Strictly speaking this is wrong. The time estimate is raster of non-svgimage objects.
        estimate = 0
        for e in self.children:
            e = e.object
            if isinstance(e, SVGImage):
                try:
                    step = e.raster_step
                except AttributeError:
                    try:
                        step = int(e.values["raster_step"])
                    except (KeyError, ValueError):
                        step = 1
                estimate += (e.image_width * e.image_height * step) / (
                    MILS_IN_MM * self.speed
                )
        hours, remainder = divmod(estimate, 3600)
        minutes, seconds = divmod(remainder, 60)
        return "%s:%s:%s" % (
            int(hours),
            str(int(minutes)).zfill(2),
            str(int(seconds)).zfill(2),
        )

    def as_cutobjects(self, closed_distance=15, passes=1):
        """Generator of cutobjects for a particular operation."""
        settings = self.derive()
        step = self.raster_step
        assert step > 0
        direction = self.raster_direction
        for element in self.children:
            svg_image = element.object
            if not isinstance(svg_image, SVGImage):
                continue

            matrix = svg_image.transform
            pil_image = svg_image.image
            pil_image, matrix = actualize(pil_image, matrix, step)
            box = (
                matrix.value_trans_x(),
                matrix.value_trans_y(),
                matrix.value_trans_x() + pil_image.width * step,
                matrix.value_trans_y() + pil_image.height * step,
            )
            path = Path(
                Polygon(
                    (box[0], box[1]),
                    (box[0], box[3]),
                    (box[2], box[3]),
                    (box[2], box[1]),
                )
            )
            cut = RasterCut(
                pil_image,
                matrix.value_trans_x(),
                matrix.value_trans_y(),
                settings=settings,
                passes=passes,
            )
            cut.path = path
            cut.original_op = self.type
            yield cut
            if direction == 4:
                cut = RasterCut(
                    pil_image,
                    matrix.value_trans_x(),
                    matrix.value_trans_y(),
                    crosshatch=True,
                    settings=settings,
                    passes=passes,
                )
                cut.path = path
                cut.original_op = self.type
                yield cut