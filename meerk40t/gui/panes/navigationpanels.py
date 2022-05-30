import wx
from wx import aui

from meerk40t.gui.icons import (
    icon_corner1,
    icon_corner2,
    icon_corner3,
    icon_corner4,
    icons8_center_of_gravity_50,
    icons8_compress_50,
    icons8_delete_50,
    icons8_down,
    icons8_down_50,
    icons8_down_left_50,
    icons8_down_right_50,
    icons8_enlarge_50,
    icons8_home_filled_50,
    icons8_laser_beam_52,
    icons8_left,
    icons8_left_50,
    icons8_level_1_50,
    icons8_lock_50,
    icons8_move_50,
    icons8_padlock_50,
    icons8_pentagon_50,
    icons8_pentagon_square_50,
    icons8_right,
    icons8_right_50,
    icons8_rotate_left_50,
    icons8_rotate_right_50,
    icons8_square_border_50,
    icons8_up_50,
    icons8_up_left_50,
    icons8_up_right_50,
    icons8up,
)
from meerk40t.gui.mwindow import MWindow
from meerk40t.svgelements import Angle, Group, Length

_ = wx.GetTranslation


MILS_IN_MM = 39.3701


def register_panel_navigation(window, context):
    panel = Drag(window, wx.ID_ANY, context=context)
    pane = (
        aui.AuiPaneInfo()
        .Right()
        .MinSize(174, 230)
        .FloatingSize(174, 230)
        .MaxSize(300, 300)
        .Caption(_("Drag"))
        .Name("drag")
        .CaptionVisible(not context.pane_lock)
        .Hide()
    )
    pane.dock_proportion = 230
    pane.control = panel
    pane.submenu = _("Navigation")

    window.on_pane_add(pane)
    context.register("pane/drag", pane)
    panel = Jog(window, wx.ID_ANY, context=context)
    pane = (
        aui.AuiPaneInfo()
        .Right()
        .MinSize(174, 230)
        .FloatingSize(174, 230)
        .MaxSize(300, 300)
        .Caption(_("Jog"))
        .Name("jog")
        .CaptionVisible(not context.pane_lock)
    )
    pane.dock_proportion = 230
    pane.control = panel
    pane.submenu = _("Navigation")

    window.on_pane_add(pane)
    context.register("pane/jog", pane)

    panel = MovePanel(window, wx.ID_ANY, context=context)
    pane = (
        aui.AuiPaneInfo()
        .Right()
        .MinSize(150, 75)
        .FloatingSize(150, 75)
        .MaxSize(200, 100)
        .Caption(_("Move"))
        .CaptionVisible(not context.pane_lock)
        .Name("move")
    )
    pane.dock_proportion = 150
    pane.control = panel
    pane.submenu = _("Navigation")

    window.on_pane_add(pane)
    context.register("pane/move", pane)

    panel = PulsePanel(window, wx.ID_ANY, context=context)
    pane = (
        aui.AuiPaneInfo()
        .Right()
        .MinSize(75, 50)
        .FloatingSize(150, 75)
        .Hide()
        .Caption(_("Pulse"))
        .CaptionVisible(not context.pane_lock)
        .Name("pulse")
    )
    pane.dock_proportion = 150
    pane.control = panel
    pane.submenu = _("Navigation")

    window.on_pane_add(pane)
    context.register("pane/pulse", pane)

    panel = SizePanel(window, wx.ID_ANY, context=context)
    pane = (
        aui.AuiPaneInfo()
        .Right()
        .MinSize(75, 50)
        .FloatingSize(150, 75)
        .Hide()
        .Caption(_("Element-Size"))
        .CaptionVisible(not context.pane_lock)
        .Name("objsizer")
    )
    pane.dock_proportion = 150
    pane.control = panel
    pane.submenu = _("Navigation")

    window.on_pane_add(pane)
    context.register("pane/objsizer", pane)

    panel = Transform(window, wx.ID_ANY, context=context)
    pane = (
        aui.AuiPaneInfo()
        .Right()
        .MinSize(174, 230)
        .FloatingSize(174, 230)
        .MaxSize(300, 300)
        .Caption(_("Transform"))
        .Name("transform")
        .CaptionVisible(not context.pane_lock)
        .Hide()
    )
    pane.dock_proportion = 230
    pane.control = panel
    pane.submenu = _("Navigation")

    window.on_pane_add(pane)
    context.register("pane/transform", pane)

    panel = JogDistancePanel(window, wx.ID_ANY, context=context, pane=True)
    pane = (
        aui.AuiPaneInfo()
        .Float()
        .MinSize(190, 110)
        .FloatingSize(190, 110)
        .Hide()
        .Caption(_("Distances"))
        .CaptionVisible(not context.pane_lock)
        .Name("jogdist")
    )
    pane.dock_proportion = 110
    pane.control = panel
    pane.submenu = _("Navigation")

    window.on_pane_add(pane)
    context.register("pane/jogdist", pane)


class Drag(wx.Panel):
    def __init__(self, *args, context=None, **kwds):
        # begin wxGlade: Drag.__init__
        kwds["style"] = kwds.get("style", 0) | wx.TAB_TRAVERSAL
        wx.Panel.__init__(self, *args, **kwds)
        self.context = context
        self.button_align_corner_top_left = wx.BitmapButton(
            self, wx.ID_ANY, icon_corner1.GetBitmap()
        )
        self.button_align_drag_up = wx.BitmapButton(
            self, wx.ID_ANY, icons8up.GetBitmap()
        )
        self.button_align_corner_top_right = wx.BitmapButton(
            self, wx.ID_ANY, icon_corner2.GetBitmap()
        )
        self.button_align_drag_left = wx.BitmapButton(
            self, wx.ID_ANY, icons8_left.GetBitmap()
        )
        self.button_align_center = wx.BitmapButton(
            self, wx.ID_ANY, icons8_square_border_50.GetBitmap()
        )
        self.button_align_drag_right = wx.BitmapButton(
            self, wx.ID_ANY, icons8_right.GetBitmap()
        )
        self.button_align_corner_bottom_left = wx.BitmapButton(
            self, wx.ID_ANY, icon_corner4.GetBitmap()
        )
        self.button_align_drag_down = wx.BitmapButton(
            self, wx.ID_ANY, icons8_down.GetBitmap()
        )
        self.button_align_corner_bottom_right = wx.BitmapButton(
            self, wx.ID_ANY, icon_corner3.GetBitmap()
        )
        self.button_align_first_position = wx.BitmapButton(
            self, wx.ID_ANY, icons8_level_1_50.GetBitmap()
        )
        self.button_align_trace_hull = wx.BitmapButton(
            self, wx.ID_ANY, icons8_pentagon_50.GetBitmap()
        )
        self.button_align_trace_quick = wx.BitmapButton(
            self, wx.ID_ANY, icons8_pentagon_square_50.GetBitmap()
        )

        self.__set_properties()
        self.__do_layout()

        self.Bind(
            wx.EVT_BUTTON,
            self.on_button_align_corner_tl,
            self.button_align_corner_top_left,
        )
        self.Bind(
            wx.EVT_BUTTON, self.on_button_align_drag_up, self.button_align_drag_up
        )
        self.Bind(
            wx.EVT_BUTTON,
            self.on_button_align_corner_tr,
            self.button_align_corner_top_right,
        )
        self.Bind(
            wx.EVT_BUTTON, self.on_button_align_drag_left, self.button_align_drag_left
        )
        self.Bind(wx.EVT_BUTTON, self.on_button_align_center, self.button_align_center)
        self.Bind(
            wx.EVT_BUTTON, self.on_button_align_drag_right, self.button_align_drag_right
        )
        self.Bind(
            wx.EVT_BUTTON,
            self.on_button_align_corner_bl,
            self.button_align_corner_bottom_left,
        )
        self.Bind(
            wx.EVT_BUTTON, self.on_button_align_drag_down, self.button_align_drag_down
        )
        self.Bind(
            wx.EVT_BUTTON,
            self.on_button_align_corner_br,
            self.button_align_corner_bottom_right,
        )
        self.Bind(
            wx.EVT_BUTTON, self.on_button_align_trace_hull, self.button_align_trace_hull
        )
        self.Bind(
            wx.EVT_BUTTON,
            self.on_button_align_trace_quick,
            self.button_align_trace_quick,
        )
        # end wxGlade
        self.elements = None
        self.console = None
        self.design_locked = False
        self.drag_ready(False)

    def __set_properties(self):
        # begin wxGlade: Drag.__set_properties
        self.button_align_corner_top_left.SetToolTip(
            _("Align laser with the upper left corner of the selection")
        )
        self.button_align_corner_top_left.SetSize(
            self.button_align_corner_top_left.GetBestSize()
        )
        self.button_align_drag_up.SetToolTip(
            _("Move the selection and laser position upwards")
        )
        self.button_align_drag_up.SetSize(self.button_align_drag_up.GetBestSize())
        self.button_align_corner_top_right.SetToolTip(
            _("Align laser with the upper right corner of the selection")
        )
        self.button_align_corner_top_right.SetSize(
            self.button_align_corner_top_right.GetBestSize()
        )
        self.button_align_drag_left.SetToolTip(
            _("Move the selection and laser position leftwards")
        )
        self.button_align_drag_left.SetSize(self.button_align_drag_left.GetBestSize())
        self.button_align_center.SetToolTip(
            _("Align laser with the center of the selection")
        )
        self.button_align_center.SetSize(self.button_align_center.GetBestSize())
        self.button_align_drag_right.SetToolTip(
            _("Move the selection and laser position rightwards")
        )
        self.button_align_drag_right.SetSize(self.button_align_drag_right.GetBestSize())
        self.button_align_corner_bottom_left.SetToolTip(
            _("Align laser with the lower left corner of the selection")
        )
        self.button_align_corner_bottom_left.SetSize(
            self.button_align_corner_bottom_left.GetBestSize()
        )
        self.button_align_drag_down.SetToolTip(
            _("Move the selection and laser position downwards")
        )
        self.button_align_drag_down.SetSize(self.button_align_drag_down.GetBestSize())
        self.button_align_corner_bottom_right.SetToolTip(
            _("Align laser with the lower right corner of the selection")
        )
        self.button_align_corner_bottom_right.SetSize(
            self.button_align_corner_bottom_right.GetBestSize()
        )
        self.button_align_first_position.SetToolTip(
            _("Align laser with the first position")
        )
        self.button_align_first_position.SetSize(
            self.button_align_first_position.GetBestSize()
        )
        self.button_align_trace_hull.SetToolTip(
            _("Perform a convex hull trace of the selection")
        )
        self.button_align_trace_hull.SetSize(self.button_align_trace_hull.GetBestSize())
        self.button_align_trace_quick.SetToolTip(
            _("Perform a simple trace of the selection")
        )
        self.button_align_trace_quick.SetSize(
            self.button_align_trace_quick.GetBestSize()
        )
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: Drag.__do_layout
        align_sizer = wx.FlexGridSizer(4, 3, 0, 0)
        align_sizer.Add(self.button_align_corner_top_left, 0, 0, 0)
        align_sizer.Add(self.button_align_drag_up, 0, 0, 0)
        align_sizer.Add(self.button_align_corner_top_right, 0, 0, 0)
        align_sizer.Add(self.button_align_drag_left, 0, 0, 0)
        align_sizer.Add(self.button_align_center, 0, 0, 0)
        align_sizer.Add(self.button_align_drag_right, 0, 0, 0)
        align_sizer.Add(self.button_align_corner_bottom_left, 0, 0, 0)
        align_sizer.Add(self.button_align_drag_down, 0, 0, 0)
        align_sizer.Add(self.button_align_corner_bottom_right, 0, 0, 0)
        align_sizer.Add(self.button_align_first_position, 0, 0, 0)
        align_sizer.Add(self.button_align_trace_hull, 0, 0, 0)
        align_sizer.Add(self.button_align_trace_quick, 0, 0, 0)
        self.SetSizer(align_sizer)
        align_sizer.Fit(self)
        self.Layout()
        # end wxGlade

    def drag_ready(self, v):
        self.design_locked = v
        self.button_align_drag_down.Enable(v)
        self.button_align_drag_up.Enable(v)
        self.button_align_drag_right.Enable(v)
        self.button_align_drag_left.Enable(v)

    def get_bbox(self):
        elements = self.context.elements
        if elements.has_emphasis():
            elements.validate_selected_area()
            bbox = elements.selected_area()
        else:
            bbox = Group.union_bbox(elements.elems())
        return bbox

    def on_button_align_center(self, event=None):  # wxGlade: Navigation.<event_handler>
        bbox = self.get_bbox()
        if bbox is None:
            return
        px = (bbox[0] + bbox[2]) / 2.0
        py = (bbox[3] + bbox[1]) / 2.0
        self.context("move_absolute %f %f\n" % (px, py))
        self.drag_ready(True)

    def on_button_align_corner_tl(
        self, event=None
    ):  # wxGlade: Navigation.<event_handler>
        bbox = self.get_bbox()
        if bbox is None:
            return
        self.context("move_absolute %f %f\n" % (bbox[0], bbox[1]))
        self.drag_ready(True)

    def on_button_align_corner_tr(
        self, event=None
    ):  # wxGlade: Navigation.<event_handler>
        bbox = self.get_bbox()
        if bbox is None:
            return
        self.context("move_absolute %f %f\n" % (bbox[2], bbox[1]))
        self.drag_ready(True)

    def on_button_align_corner_bl(
        self, event=None
    ):  # wxGlade: Navigation.<event_handler>
        bbox = self.get_bbox()
        if bbox is None:
            return
        self.context("move_absolute %f %f\n" % (bbox[0], bbox[3]))
        self.drag_ready(True)

    def on_button_align_corner_br(
        self, event=None
    ):  # wxGlade: Navigation.<event_handler>
        bbox = self.get_bbox()
        if bbox is None:
            return
        self.context("move_absolute %f %f\n" % (bbox[2], bbox[3]))
        self.drag_ready(True)

    def drag_relative(self, dx, dy):
        self.context("move_relative %d %d\ntranslate %d %d\n" % (dx, dy, dx, dy))

    def on_button_align_drag_down(
        self, event=None
    ):  # wxGlade: Navigation.<event_handler>
        self.drag_relative(0, self.context.navigate_jog)

    def on_button_align_drag_right(
        self, event=None
    ):  # wxGlade: Navigation.<event_handler>
        self.drag_relative(self.context.navigate_jog, 0)

    def on_button_align_drag_up(
        self, event=None
    ):  # wxGlade: Navigation.<event_handler>
        self.drag_relative(0, -self.context.navigate_jog)

    def on_button_align_drag_left(
        self, event=None
    ):  # wxGlade: Navigation.<event_handler>
        self.drag_relative(-self.context.navigate_jog, 0)

    def on_button_align_first_position(self, event=None):
        elements = self.context.elements
        e = list(elements.elems(emphasized=True))
        try:
            pos = e[0].first_point * e[0].transform
        except (IndexError, AttributeError):
            return
        if pos is None:
            return
        self.context("move_absolute %f %f\n" % (pos[0], pos[1]))
        self.drag_ready(True)

    def on_button_align_trace_hull(
        self, event=None
    ):  # wxGlade: Navigation.<event_handler>
        self.context("trace_hull\n")

    def on_button_align_trace_quick(
        self, event=None
    ):  # wxGlade: Navigation.<event_handler>
        self.context("trace_quick\n")
        self.drag_ready(True)


class Jog(wx.Panel):
    def __init__(self, *args, context=None, **kwds):
        # begin wxGlade: Jog.__init__
        kwds["style"] = kwds.get("style", 0) | wx.TAB_TRAVERSAL

        wx.Panel.__init__(self, *args, **kwds)
        self.context = context
        context.setting(float, "navigate_jog", 394.0)
        self.button_navigate_up_left = wx.BitmapButton(
            self, wx.ID_ANY, icons8_up_left_50.GetBitmap()
        )
        self.button_navigate_up = wx.BitmapButton(
            self, wx.ID_ANY, icons8_up_50.GetBitmap()
        )
        self.button_navigate_up_right = wx.BitmapButton(
            self, wx.ID_ANY, icons8_up_right_50.GetBitmap()
        )
        self.button_navigate_left = wx.BitmapButton(
            self, wx.ID_ANY, icons8_left_50.GetBitmap()
        )
        self.button_navigate_home = wx.BitmapButton(
            self, wx.ID_ANY, icons8_home_filled_50.GetBitmap()
        )
        self.button_navigate_right = wx.BitmapButton(
            self, wx.ID_ANY, icons8_right_50.GetBitmap()
        )
        self.button_navigate_down_left = wx.BitmapButton(
            self, wx.ID_ANY, icons8_down_left_50.GetBitmap()
        )
        self.button_navigate_down = wx.BitmapButton(
            self, wx.ID_ANY, icons8_down_50.GetBitmap()
        )
        self.button_navigate_down_right = wx.BitmapButton(
            self, wx.ID_ANY, icons8_down_right_50.GetBitmap()
        )
        self.button_navigate_unlock = wx.BitmapButton(
            self, wx.ID_ANY, icons8_padlock_50.GetBitmap()
        )
        self.button_navigate_lock = wx.BitmapButton(
            self, wx.ID_ANY, icons8_lock_50.GetBitmap()
        )
        self.__set_properties()
        self.__do_layout()

        self.Bind(
            wx.EVT_BUTTON, self.on_button_navigate_ul, self.button_navigate_up_left
        )
        self.Bind(wx.EVT_BUTTON, self.on_button_navigate_u, self.button_navigate_up)
        self.Bind(
            wx.EVT_BUTTON, self.on_button_navigate_ur, self.button_navigate_up_right
        )
        self.Bind(wx.EVT_BUTTON, self.on_button_navigate_l, self.button_navigate_left)
        self.Bind(
            wx.EVT_BUTTON, self.on_button_navigate_home, self.button_navigate_home
        )
        self.Bind(wx.EVT_BUTTON, self.on_button_navigate_r, self.button_navigate_right)
        self.Bind(
            wx.EVT_BUTTON, self.on_button_navigate_dl, self.button_navigate_down_left
        )
        self.Bind(wx.EVT_BUTTON, self.on_button_navigate_d, self.button_navigate_down)
        self.Bind(
            wx.EVT_BUTTON, self.on_button_navigate_dr, self.button_navigate_down_right
        )
        self.Bind(
            wx.EVT_BUTTON, self.on_button_navigate_unlock, self.button_navigate_unlock
        )
        self.Bind(
            wx.EVT_BUTTON, self.on_button_navigate_lock, self.button_navigate_lock
        )
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: Jog.__set_properties
        self.button_navigate_up_left.SetToolTip(
            _("Move laser diagonally in the up and left direction")
        )
        self.button_navigate_up_left.SetSize(self.button_navigate_up_left.GetBestSize())
        self.button_navigate_up.SetToolTip(_("Move laser in the up direction"))
        self.button_navigate_up.SetSize(self.button_navigate_up.GetBestSize())
        self.button_navigate_up_right.SetToolTip(
            _("Move laser diagonally in the up and right direction")
        )
        self.button_navigate_up_right.SetSize(
            self.button_navigate_up_right.GetBestSize()
        )
        self.button_navigate_left.SetToolTip(_("Move laser in the left direction"))
        self.button_navigate_left.SetSize(self.button_navigate_left.GetBestSize())
        self.button_navigate_home.SetSize(self.button_navigate_home.GetBestSize())
        self.button_navigate_right.SetToolTip(_("Move laser in the right direction"))
        self.button_navigate_right.SetSize(self.button_navigate_right.GetBestSize())
        self.button_navigate_down_left.SetToolTip(
            _("Move laser diagonally in the down and left direction")
        )
        self.button_navigate_down_left.SetSize(
            self.button_navigate_down_left.GetBestSize()
        )
        self.button_navigate_down.SetToolTip(_("Move laser in the down direction"))
        self.button_navigate_down.SetSize(self.button_navigate_down.GetBestSize())
        self.button_navigate_down_right.SetToolTip(
            _("Move laser diagonally in the down and right direction")
        )
        self.button_navigate_down_right.SetSize(
            self.button_navigate_down_right.GetBestSize()
        )
        self.button_navigate_unlock.SetToolTip(_("Unlock the laser rail"))
        self.button_navigate_unlock.SetSize(self.button_navigate_unlock.GetBestSize())
        self.button_navigate_lock.SetToolTip(_("Lock the laser rail"))
        self.button_navigate_lock.SetSize(self.button_navigate_lock.GetBestSize())
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: Jog.__do_layout
        navigation_sizer = wx.FlexGridSizer(4, 3, 0, 0)
        navigation_sizer.Add(self.button_navigate_up_left, 0, 0, 0)
        navigation_sizer.Add(self.button_navigate_up, 0, 0, 0)
        navigation_sizer.Add(self.button_navigate_up_right, 0, 0, 0)
        navigation_sizer.Add(self.button_navigate_left, 0, 0, 0)
        navigation_sizer.Add(self.button_navigate_home, 0, 0, 0)
        navigation_sizer.Add(self.button_navigate_right, 0, 0, 0)
        navigation_sizer.Add(self.button_navigate_down_left, 0, 0, 0)
        navigation_sizer.Add(self.button_navigate_down, 0, 0, 0)
        navigation_sizer.Add(self.button_navigate_down_right, 0, 0, 0)
        navigation_sizer.Add(self.button_navigate_unlock, 0, 0, 0)
        navigation_sizer.Add((0, 0), 0, 0, 0)
        navigation_sizer.Add(self.button_navigate_lock, 0, 0, 0)
        self.SetSizer(navigation_sizer)
        navigation_sizer.Fit(self)
        self.Layout()
        # end wxGlade

    def on_button_navigate_home(
        self, event=None
    ):  # wxGlade: Navigation.<event_handler>
        self.context("home\n")

    def on_button_navigate_ul(self, event=None):  # wxGlade: Navigation.<event_handler>
        dx = -self.context.navigate_jog
        dy = -self.context.navigate_jog
        self.context("move_relative %d %d\n" % (dx, dy))

    def on_button_navigate_u(self, event=None):  # wxGlade: Navigation.<event_handler>
        dx = 0
        dy = -self.context.navigate_jog
        self.context("move_relative %d %d\n" % (dx, dy))

    def on_button_navigate_ur(self, event=None):  # wxGlade: Navigation.<event_handler>
        dx = self.context.navigate_jog
        dy = -self.context.navigate_jog
        self.context("move_relative %d %d\n" % (dx, dy))

    def on_button_navigate_l(self, event=None):  # wxGlade: Navigation.<event_handler>
        dx = -self.context.navigate_jog
        dy = 0
        self.context("move_relative %d %d\n" % (dx, dy))

    def on_button_navigate_r(self, event=None):  # wxGlade: Navigation.<event_handler>
        dx = self.context.navigate_jog
        dy = 0
        self.context("move_relative %d %d\n" % (dx, dy))

    def on_button_navigate_dl(self, event=None):  # wxGlade: Navigation.<event_handler>
        dx = -self.context.navigate_jog
        dy = self.context.navigate_jog
        self.context("move_relative %d %d\n" % (dx, dy))

    def on_button_navigate_d(self, event=None):  # wxGlade: Navigation.<event_handler>
        dx = 0
        dy = self.context.navigate_jog
        self.context("move_relative %d %d\n" % (dx, dy))

    def on_button_navigate_dr(self, event=None):  # wxGlade: Navigation.<event_handler>
        dx = self.context.navigate_jog
        dy = self.context.navigate_jog
        self.context("move_relative %d %d\n" % (dx, dy))

    def on_button_navigate_unlock(
        self, event=None
    ):  # wxGlade: Navigation.<event_handler>
        self.context("unlock\n")

    def on_button_navigate_lock(
        self, event=None
    ):  # wxGlade: Navigation.<event_handler>
        self.context("lock\n")


class MovePanel(wx.Panel):
    def __init__(self, *args, context=None, **kwds):
        # begin wxGlade: MovePanel.__init__
        kwds["style"] = kwds.get("style", 0) | wx.TAB_TRAVERSAL
        wx.Panel.__init__(self, *args, **kwds)
        self.context = context
        self.button_navigate_move_to = wx.BitmapButton(
            self, wx.ID_ANY, icons8_center_of_gravity_50.GetBitmap()
        )
        default_pos = "0{units}".format(units=context.root.units_name)
        self.text_position_x = wx.TextCtrl(
            self, wx.ID_ANY, value=default_pos, style=wx.TE_PROCESS_ENTER
        )
        self.text_position_y = wx.TextCtrl(
            self, wx.ID_ANY, value=default_pos, style=wx.TE_PROCESS_ENTER
        )

        self.__set_properties()
        self.__do_layout()

        self.Bind(
            wx.EVT_BUTTON, self.on_button_navigate_move_to, self.button_navigate_move_to
        )
        self.Bind(
            wx.EVT_TEXT_ENTER, self.on_button_navigate_move_to, self.text_position_x
        )
        self.Bind(
            wx.EVT_TEXT_ENTER, self.on_button_navigate_move_to, self.text_position_y
        )
        # end wxGlade
        self.bed_dim = context.root
        self.bed_dim.setting(int, "bed_width", 310)  # Default Value
        self.bed_dim.setting(int, "bed_height", 210)  # Default Value

    def __set_properties(self):
        # begin wxGlade: MovePanel.__set_properties
        self.button_navigate_move_to.SetToolTip(_("Move to the set position"))
        self.button_navigate_move_to.SetSize(self.button_navigate_move_to.GetBestSize())
        self.text_position_x.SetToolTip(_("Set X value for the Move To"))
        self.text_position_y.SetToolTip(_("Set Y value for the Move To"))
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: MovePanel.__do_layout
        sizer_12 = wx.StaticBoxSizer(
            wx.StaticBox(self, wx.ID_ANY, _("Move To:")), wx.HORIZONTAL
        )
        sizer_13 = wx.BoxSizer(wx.VERTICAL)
        sizer_15 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_14 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_12.Add(self.button_navigate_move_to, 0, 0, 0)
        label_9 = wx.StaticText(self, wx.ID_ANY, "X:")
        label_9.SetMinSize((-1, 23))
        sizer_14.Add(label_9, 0, 0, 0)
        sizer_14.Add(self.text_position_x, 0, 0, 0)
        sizer_13.Add(sizer_14, 0, wx.EXPAND, 0)
        label_10 = wx.StaticText(self, wx.ID_ANY, "Y:")
        label_10.SetMinSize((-1, 23))
        sizer_15.Add(label_10, 0, 0, 0)
        sizer_15.Add(self.text_position_y, 0, 0, 0)
        sizer_13.Add(sizer_15, 0, wx.EXPAND, 0)
        sizer_12.Add(sizer_13, 0, wx.EXPAND, 0)
        self.SetSizer(sizer_12)
        sizer_12.Fit(self)
        self.Layout()
        # end wxGlade

    def on_button_navigate_move_to(
        self, event=None
    ):  # wxGlade: Navigation.<event_handler>
        try:
            width = self.bed_dim.bed_width * MILS_IN_MM
            height = self.bed_dim.bed_height * MILS_IN_MM
            x = Length(self.text_position_x.GetValue()).value(
                ppi=1000.0, relative_length=width
            )
            y = Length(self.text_position_y.GetValue()).value(
                ppi=1000.0, relative_length=height
            )
            if x > width or y > height or x < 0 or y < 0:
                dlg = wx.MessageDialog(
                    None,
                    _("Cannot Move Outside Bed Dimensions"),
                    _("Error"),
                    wx.ICON_WARNING,
                )
                dlg.ShowModal()
                dlg.Destroy()
                return
            self.context("move %d %d\n" % (x, y))
        except ValueError:
            return


class PulsePanel(wx.Panel):
    def __init__(self, *args, context=None, **kwds):
        # begin wxGlade: PulsePanel.__init__
        kwds["style"] = kwds.get("style", 0) | wx.TAB_TRAVERSAL
        wx.Panel.__init__(self, *args, **kwds)
        self.context = context
        self.button_navigate_pulse = wx.BitmapButton(
            self, wx.ID_ANY, icons8_laser_beam_52.GetBitmap()
        )
        self.spin_pulse_duration = wx.SpinCtrl(
            self, wx.ID_ANY, style=wx.TE_PROCESS_ENTER, value="50", min=1, max=1000
        )
        self.__set_properties()
        self.__do_layout()

        self.Bind(
            wx.EVT_BUTTON, self.on_button_navigate_pulse, self.button_navigate_pulse
        )
        self.Bind(
            wx.EVT_SPINCTRL, self.on_spin_pulse_duration, self.spin_pulse_duration
        )
        self.Bind(
            wx.EVT_TEXT_ENTER, self.on_button_navigate_pulse, self.spin_pulse_duration
        )
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: PulsePanel.__set_properties
        self.button_navigate_pulse.SetToolTip(_("Fire a short laser pulse"))
        self.button_navigate_pulse.SetSize(self.button_navigate_pulse.GetBestSize())
        self.spin_pulse_duration.SetMinSize((80, 23))
        self.spin_pulse_duration.SetToolTip(_("Set the duration of the laser pulse"))
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: PulsePanel.__do_layout
        sizer_5 = wx.StaticBoxSizer(
            wx.StaticBox(self, wx.ID_ANY, _("Short Pulse:")), wx.HORIZONTAL
        )
        sizer_5.Add(self.button_navigate_pulse, 0, 0, 0)
        sizer_5.Add(self.spin_pulse_duration, 0, 0, 0)
        label_4 = wx.StaticText(self, wx.ID_ANY, _(" ms"))
        sizer_5.Add(label_4, 0, 0, 0)
        self.SetSizer(sizer_5)
        sizer_5.Fit(self)
        self.Layout()
        # end wxGlade

    def on_button_navigate_pulse(
        self, event=None
    ):  # wxGlade: Navigation.<event_handler>
        value = self.spin_pulse_duration.GetValue()
        self.context("pulse %f\n" % value)

    def on_spin_pulse_duration(self, event=None):  # wxGlade: Navigation.<event_handler>
        self.context.navigate_pulse = float(self.spin_pulse_duration.GetValue())


class SizePanel(wx.Panel):
    def __init__(self, *args, context=None, **kwds):
        # begin wxGlade: SizePanel.__init__
        kwds["style"] = kwds.get("style", 0) | wx.TAB_TRAVERSAL
        wx.Panel.__init__(self, *args, **kwds)
        self.context = context

        self.mainsizer = wx.StaticBoxSizer(
            wx.StaticBox(self, wx.ID_ANY, _("Object Dimensions")), wx.HORIZONTAL
        )
        self.button_navigate_resize = wx.BitmapButton(
            self, wx.ID_ANY, icons8_compress_50.GetBitmap()
        )
        self.label_9 = wx.StaticText(self, wx.ID_ANY, _("Width:"))
        self.label_10 = wx.StaticText(self, wx.ID_ANY, _("Height:"))

        self.text_width = wx.TextCtrl(self, wx.ID_ANY, "0")
        self.text_height = wx.TextCtrl(self, wx.ID_ANY, "0")
        self.btn_lock_ratio = wx.ToggleButton(self, wx.ID_ANY, "")

        self.__set_properties()
        self.__do_layout()

        self.Bind(
            wx.EVT_BUTTON, self.on_button_navigate_resize, self.button_navigate_resize
        )
        self.text_width.Bind(wx.EVT_KILL_FOCUS, self.on_lostfocus_w)
        self.text_height.Bind(wx.EVT_KILL_FOCUS, self.on_lostfocus_h)
        # self.Bind(wx.EVT_TOGGLEBUTTON, self.on_button_lock_toggle, self.btn_lock_ratio)
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: SizePanel.__set_properties
        self.button_navigate_resize.SetToolTip(_("Resize the object"))
        self.button_navigate_resize.SetSize(self.button_navigate_resize.GetBestSize())
        self.text_width.SetToolTip(_("Define width of selected object"))
        self.text_height.SetToolTip(_("Define height of selected object"))
        self.btn_lock_ratio.SetMinSize((32, 32))
        self.btn_lock_ratio.SetBitmap(
            icons8_lock_50.GetBitmap(resize=25, use_theme=False)
        )
        self.btn_lock_ratio.SetToolTip(
            _("Lock the ratio of width / height to the original values")
        )
        self.text_height.Enable(False)
        self.text_width.Enable(False)
        self.button_navigate_resize.Enable(False)

        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: SizePanel.__do_layout
        self.mainsizer.Add(self.button_navigate_resize, 0, 0, 0)
        fieldsizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer_label = wx.BoxSizer(wx.VERTICAL)

        self.mainsizer.Add(fieldsizer, 1, wx.EXPAND, 0)

        fieldsizer.Add(sizer_label, 0, wx.EXPAND, 0)

        self.label_9.SetMinSize((-1, 23))
        sizer_label.Add(self.label_9, 0, 0, 0)

        self.label_10.SetMinSize((-1, 23))
        sizer_label.Add(self.label_10, 0, 0, 0)

        sizer_text = wx.BoxSizer(wx.VERTICAL)
        fieldsizer.Add(sizer_text, 1, wx.EXPAND, 0)

        sizer_text.Add(self.text_width, 0, wx.EXPAND, 0)

        sizer_text.Add(self.text_height, 0, wx.EXPAND, 0)

        sizer_lock = wx.BoxSizer(wx.VERTICAL)
        fieldsizer.Add(sizer_lock, 0, wx.EXPAND, 0)

        sizer_lock.Add(self.btn_lock_ratio, 0, 0, 0)

        self.SetSizer(self.mainsizer)
        self.mainsizer.Fit(self)

        self.Layout()
        # end wxGlade

    def initialize(self, *args):
        self.context.listen("emphasized", self.on_emphasized_elements_changed)
        self.context.listen("modified", self.on_modified_element)
        self.update_sizes()

    def finalize(self, *args):
        self.context.unlisten("emphasized", self.on_emphasized_elements_changed)
        self.context.unlisten("modified", self.on_modified_element)

    def on_modified_element(self, origin, *args):
        self.update_sizes()

    def on_emphasized_elements_changed(self, origin, elements):
        self.update_sizes()

    objratio = 1.0
    org_x = 0
    org_y = 0
    org_w = 0
    org_h = 0

    def update_sizes(self):
        f = self.context.elements.first_element(emphasized=True)
        v = f is not None
        if self.context.root.units_name == "mm":
            fmt = "{valu:.2f}{units}"
            scale_factor = 1.0 / MILS_IN_MM
        elif self.context.root.units_name == "cm":
            fmt = "{valu:.4f}{units}"
            scale_factor = 1.0 / (10.0 * MILS_IN_MM)
        elif self.context.root.units_name == "inch":
            fmt = "{valu:.4f}{units}"
            scale_factor = 0.001
        else:
            fmt = "{valu:.1f}{units}"
            scale_factor = 1.0

        if v:
            try:
                bb = f.bbox()
                self.org_x = bb[0]
                self.org_y = bb[1]
                mw = abs(bb[2] - bb[0]) * scale_factor
                mh = abs(bb[3] - bb[1]) * scale_factor
                self.org_w = mw
                self.org_h = mh
                if mh == 0:
                    self.objratio = 0
                else:
                    self.objratio = mw / mh
            except (ValueError, AttributeError, TypeError):
                self.objratio = 1.0
                v = False  # has no bounding box...

        self.button_navigate_resize.Enable(v)
        self.text_width.Enable(v)
        self.text_height.Enable(v)

        if v:
            self.text_width.SetValue(
                fmt.format(units=self.context.root.units_name, valu=mw)
            )
            self.text_height.SetValue(
                fmt.format(units=self.context.root.units_name, valu=mh)
            )
        else:
            self.text_width.SetValue("---")
            self.text_height.SetValue("---")

    def on_button_navigate_resize(self, event):  # wxGlade: SizePanel.<event_handler>
        llw = Length(self.text_width.Value, relative_length=self.org_w)
        llh = Length(self.text_height.Value, relative_length=self.org_w)
        munits1 = llw.units
        munits2 = llh.units
        mval1 = float(llw.value(relative_length=self.org_w))
        mval2 = float(llh.value(relative_length=self.org_h))
        # print("Target size: %f %s x %f %s" % (mval1, munits1, mval2, munits2))
        self.context(
            "resize %f %f %f%s %f%s"
            % (self.org_x, self.org_y, mval1, munits1, mval2, munits2)
        )

    def on_lostfocus_w(self, event):  # wxGlade: SizePanel.<event_handler>
        if self.btn_lock_ratio.GetValue():
            ll = Length(self.text_width.Value, relative_length=self.org_w)
            munits = ll.units
            mval = float(ll.value(relative_length=self.org_w))
            print("Length provides for width: %f" % mval)
            if mval != 0:
                mval = mval / self.objratio
            self.text_height.SetValue(
                "{valu:.4f}{units}".format(units=munits, valu=mval)
            )
        event.Skip()

    def on_lostfocus_h(self, event):  # wxGlade: SizePanel.<event_handler>
        if self.btn_lock_ratio.GetValue():
            ll = Length(self.text_height.Value, relative_length=self.org_h)
            munits = ll.units
            mval = float(ll.value(relative_length=self.org_h))
            if mval != 0:
                mval = self.objratio * mval
            self.text_width.SetValue(
                "{valu:.4f}{units}".format(units=munits, valu=mval)
            )
        event.Skip()


class Transform(wx.Panel):
    def __init__(self, *args, context=None, **kwds):
        # begin wxGlade: Transform.__init__
        kwds["style"] = kwds.get("style", 0) | wx.TAB_TRAVERSAL
        wx.Panel.__init__(self, *args, **kwds)
        self.context = context
        self.button_scale_down = wx.BitmapButton(
            self, wx.ID_ANY, icons8_compress_50.GetBitmap()
        )
        self.button_translate_up = wx.BitmapButton(
            self, wx.ID_ANY, icons8_up_50.GetBitmap()
        )
        self.button_scale_up = wx.BitmapButton(
            self, wx.ID_ANY, icons8_enlarge_50.GetBitmap()
        )
        self.button_translate_left = wx.BitmapButton(
            self, wx.ID_ANY, icons8_left_50.GetBitmap()
        )
        self.button_reset = wx.BitmapButton(
            self, wx.ID_ANY, icons8_delete_50.GetBitmap()
        )
        self.button_translate_right = wx.BitmapButton(
            self, wx.ID_ANY, icons8_right_50.GetBitmap()
        )
        self.button_rotate_ccw = wx.BitmapButton(
            self, wx.ID_ANY, icons8_rotate_left_50.GetBitmap()
        )
        self.button_translate_down = wx.BitmapButton(
            self, wx.ID_ANY, icons8_down_50.GetBitmap()
        )
        self.button_rotate_cw = wx.BitmapButton(
            self, wx.ID_ANY, icons8_rotate_right_50.GetBitmap()
        )
        self.text_a = wx.TextCtrl(
            self, wx.ID_ANY, style=wx.TE_PROCESS_ENTER, value="1.000000"
        )
        self.text_d = wx.TextCtrl(
            self, wx.ID_ANY, style=wx.TE_PROCESS_ENTER, value="1.000000"
        )
        self.text_c = wx.TextCtrl(
            self, wx.ID_ANY, style=wx.TE_PROCESS_ENTER, value="0.000000"
        )
        self.text_b = wx.TextCtrl(
            self, wx.ID_ANY, style=wx.TE_PROCESS_ENTER, value="0.000000"
        )
        self.text_e = wx.TextCtrl(
            self, wx.ID_ANY, style=wx.TE_PROCESS_ENTER, value="0.0"
        )
        self.text_f = wx.TextCtrl(
            self, wx.ID_ANY, style=wx.TE_PROCESS_ENTER, value="0.0"
        )

        self.__set_properties()
        self.__do_layout()

        self.button_scale_down.Bind(wx.EVT_BUTTON, self.on_scale_down_5)
        self.button_translate_up.Bind(wx.EVT_BUTTON, self.on_translate_up_1)
        self.button_scale_up.Bind(wx.EVT_BUTTON, self.on_scale_up_5)
        self.button_translate_left.Bind(wx.EVT_BUTTON, self.on_translate_left_1)
        self.button_reset.Bind(wx.EVT_BUTTON, self.on_reset)
        self.button_rotate_ccw.Bind(wx.EVT_BUTTON, self.on_rotate_ccw_5)
        self.button_translate_right.Bind(wx.EVT_BUTTON, self.on_translate_right_1)
        self.button_rotate_cw.Bind(wx.EVT_BUTTON, self.on_rotate_cw_5)
        self.button_translate_down.Bind(wx.EVT_BUTTON, self.on_translate_down_1)
        self.text_a.Bind(wx.EVT_TEXT_ENTER, self.on_text_matrix)
        self.text_b.Bind(wx.EVT_TEXT_ENTER, self.on_text_matrix)
        self.text_c.Bind(wx.EVT_TEXT_ENTER, self.on_text_matrix)
        self.text_d.Bind(wx.EVT_TEXT_ENTER, self.on_text_matrix)
        self.text_e.Bind(wx.EVT_TEXT_ENTER, self.on_text_matrix)
        self.text_f.Bind(wx.EVT_TEXT_ENTER, self.on_text_matrix)
        self.text_a.Bind(wx.EVT_KILL_FOCUS, self.on_text_matrix)
        self.text_b.Bind(wx.EVT_KILL_FOCUS, self.on_text_matrix)
        self.text_c.Bind(wx.EVT_KILL_FOCUS, self.on_text_matrix)
        self.text_d.Bind(wx.EVT_KILL_FOCUS, self.on_text_matrix)
        self.text_e.Bind(wx.EVT_KILL_FOCUS, self.on_text_matrix)
        self.text_f.Bind(wx.EVT_KILL_FOCUS, self.on_text_matrix)

        self.button_translate_up.Bind(wx.EVT_RIGHT_DOWN, self.on_translate_up_10)
        self.button_translate_down.Bind(wx.EVT_RIGHT_DOWN, self.on_translate_down_10)
        self.button_translate_left.Bind(wx.EVT_RIGHT_DOWN, self.on_translate_left_10)
        self.button_translate_right.Bind(wx.EVT_RIGHT_DOWN, self.on_translate_right_10)

        self.button_rotate_ccw.Bind(wx.EVT_RIGHT_DOWN, self.on_rotate_ccw_90)
        self.button_rotate_cw.Bind(wx.EVT_RIGHT_DOWN, self.on_rotate_cw_90)
        self.button_scale_down.Bind(wx.EVT_RIGHT_DOWN, self.on_scale_down_50)
        self.button_scale_up.Bind(wx.EVT_RIGHT_DOWN, self.on_scale_up_50)
        # end wxGlade
        self.select_ready(False)

    def __set_properties(self):
        # begin wxGlade: Transform.__set_properties
        self.button_scale_down.SetSize(self.button_scale_down.GetBestSize())
        self.button_translate_up.SetSize(self.button_translate_up.GetBestSize())
        self.button_scale_up.SetSize(self.button_scale_up.GetBestSize())
        self.button_translate_left.SetSize(self.button_translate_left.GetBestSize())
        self.button_reset.SetSize(self.button_reset.GetBestSize())
        self.button_translate_right.SetSize(self.button_translate_right.GetBestSize())
        self.button_rotate_ccw.SetSize(self.button_rotate_ccw.GetBestSize())
        self.button_translate_down.SetSize(self.button_translate_down.GetBestSize())
        self.button_rotate_cw.SetSize(self.button_rotate_cw.GetBestSize())

        self.button_scale_down.SetToolTip(
            _("Scale Down by 5% / 50% on left / right click")
        )
        self.button_translate_up.SetToolTip(
            _("Translate Up by 1x / 10x Jog-Distance on left / right click")
        )
        self.button_scale_up.SetToolTip(_("Scale Up by 5% / 50% on left / right click"))
        self.button_translate_left.SetToolTip(
            _("Translate Left by 1x / 10x Jog-Distance on left / right click")
        )
        self.button_reset.SetToolTip(_("Reset Matrix"))
        self.button_translate_right.SetToolTip(
            _("Translate Right by 1x / 10x Jog-Distance on left / right click")
        )
        self.button_rotate_ccw.SetToolTip(
            _("Rotate Counterclockwise by 5° / by 90° on left / right click")
        )
        self.button_translate_down.SetToolTip(
            _("Translate Down by 1x / 10x Jog-Distance on left / right click")
        )
        self.button_rotate_cw.SetToolTip(
            _("Rotate Clockwise by 5° / by 90° on left / right click")
        )
        self.text_a.SetMinSize((55, -1))
        self.text_a.SetToolTip(
            _(
                "Scale X - scales the element by this factor in the X-Direction, i.e. 2.0 means 200% of the original scale. "
                "You may enter either this factor directly or state the scale as a %-value, so 0.5 or 50% will both cut the scale in half."
            )
        )
        self.text_d.SetMinSize((55, -1))
        self.text_d.SetToolTip(
            _(
                "Scale Y - scales the element by this factor in the Y-Direction, i.e. 2.0 means 200% of the original scale. "
                "You may enter either this factor directly or state the scale as a %-value, so 0.5 or 50% will both cut the scale in half."
            )
        )
        self.text_c.SetMinSize((55, -1))
        self.text_c.SetToolTip(
            _(
                "Skew X - to skew the element in X-direction by alpha° you need either \n"
                "- to provide tan(alpha), i.e. 15° = 0.2679, 30° = 0.5774, 45° = 1.0 and so on...\n"
                "- or provide the angle as 15deg, 0.25turn, (like all other angles)\n"
                "In any case this value will then be represented as tan(alpha)"
            )
        )
        self.text_b.SetMinSize((55, -1))
        self.text_b.SetToolTip(
            _(
                "Skew Y - to skew the element in Y-direction by alpha° you need either \n"
                "- to provide tan(alpha), i.e. 15° = 0.2679, 30° = 0.5774, 45° = 1.0 and so on...\n"
                "- or provide the angle as 15deg, 0.25turn, (like all other angles)\n"
                "In any case this value will then be represented as tan(alpha)"
            )
        )
        self.text_e.SetMinSize((40, -1))
        self.text_e.SetToolTip(
            _(
                "Translate X - moves the element by this amount of mils in the X-direction; "
                "you may use 'real' distances when modifying this factor, i.e. 2in, 3cm, 50mm"
            )
        )
        self.text_f.SetMinSize((40, -1))
        self.text_f.SetToolTip(
            _(
                "Translate Y - moves the element by this amount of mils in the Y-direction; "
                "you may use 'real' distances when modifying this factor, i.e. 2in, 3cm, 50mm"
            )
        )
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: Transform.__do_layout
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        icon_sizer = wx.FlexGridSizer(3, 3, 0, 0)
        icon_sizer.Add(self.button_scale_down, 0, 0, 0)
        icon_sizer.Add(self.button_translate_up, 0, 0, 0)
        icon_sizer.Add(self.button_scale_up, 0, 0, 0)
        icon_sizer.Add(self.button_translate_left, 0, 0, 0)
        icon_sizer.Add(self.button_reset, 0, 0, 0)
        icon_sizer.Add(self.button_translate_right, 0, 0, 0)
        icon_sizer.Add(self.button_rotate_ccw, 0, 0, 0)
        icon_sizer.Add(self.button_translate_down, 0, 0, 0)
        icon_sizer.Add(self.button_rotate_cw, 0, 0, 0)

        matrix_sizer = wx.BoxSizer(wx.HORIZONTAL)
        col_sizer_1 = wx.BoxSizer(wx.VERTICAL)
        col_sizer_1.Add(wx.StaticText(self, wx.ID_ANY, ""), wx.HORIZONTAL)
        col_sizer_1.Add(wx.StaticText(self, wx.ID_ANY, _("X:")), wx.HORIZONTAL)
        col_sizer_1.Add(wx.StaticText(self, wx.ID_ANY, _("Y:")), wx.HORIZONTAL)

        # Add some labels to make textboxes clearer to understand
        col_sizer_2 = wx.BoxSizer(wx.VERTICAL)
        col_sizer_2.Add(wx.StaticText(self, wx.ID_ANY, _("Scale")), wx.HORIZONTAL)
        col_sizer_2.Add(self.text_a, 0, wx.EXPAND, 0)  # Scale X
        col_sizer_2.Add(self.text_d, 0, wx.EXPAND, 0)  # Scale Y

        col_sizer_3 = wx.BoxSizer(wx.VERTICAL)
        col_sizer_3.Add(wx.StaticText(self, wx.ID_ANY, _("Skew")), wx.HORIZONTAL)
        col_sizer_3.Add(self.text_c, 0, wx.EXPAND, 0)  # Skew X
        col_sizer_3.Add(self.text_b, 0, wx.EXPAND, 0)  # Skew Y

        col_sizer_4 = wx.BoxSizer(wx.VERTICAL)
        col_sizer_4.Add(wx.StaticText(self, wx.ID_ANY, _("Translate")), wx.HORIZONTAL)
        col_sizer_4.Add(self.text_e, 0, wx.EXPAND, 0)  # Translate X
        col_sizer_4.Add(self.text_f, 0, wx.EXPAND, 0)  # Translate Y

        matrix_sizer.Add(col_sizer_1, 0, wx.EXPAND, 0)  # fixed width
        matrix_sizer.Add(col_sizer_2, 1, wx.EXPAND, 0)  # grow
        matrix_sizer.Add(col_sizer_3, 1, wx.EXPAND, 0)  # grow
        matrix_sizer.Add(col_sizer_4, 1, wx.EXPAND, 0)  # grow

        main_sizer.Add(icon_sizer, 0, wx.EXPAND, 0)
        main_sizer.Add(matrix_sizer, 0, wx.EXPAND, 0)
        self.SetSizer(main_sizer)
        main_sizer.Fit(self)
        self.Layout()
        # end wxGlade

    def initialize(self, *args):
        self.context.listen("emphasized", self.on_emphasized_elements_changed)
        self.context.listen("modified", self.on_modified_element)
        self.update_matrix_text()

    def finalize(self, *args):
        self.context.unlisten("emphasized", self.on_emphasized_elements_changed)
        self.context.unlisten("modified", self.on_modified_element)

    def on_modified_element(self, origin, *args):
        self.update_matrix_text()

    def on_emphasized_elements_changed(self, origin, elements):
        self.select_ready(self.context.elements.has_emphasis())
        self.update_matrix_text()

    def update_matrix_text(self):
        f = self.context.elements.first_element(emphasized=True)
        v = f is not None
        self.text_a.Enable(v)
        self.text_b.Enable(v)
        self.text_c.Enable(v)
        self.text_d.Enable(v)
        self.text_e.Enable(v)
        self.text_f.Enable(v)
        if v:
            matrix = f.transform
            # You will get sometimes slightly different numbers thean you would expect due to arithmetic operations
            # we will therefore 'adjust' those figures slightly to avoid confusion by rounding them to the sixth decimal (arbitrary)
            # that should be good enough...
            self.text_a.SetValue("%.5f" % matrix.a)  # Scale X
            self.text_b.SetValue("%.5f" % matrix.b)  # Skew Y
            self.text_c.SetValue("%.5f" % matrix.c)  # Skew X
            self.text_d.SetValue("%.5f" % matrix.d)  # Scale Y
            # Translate X & are in mils, so about 0.025 mm, so 1 digit should be more than enough...
            self.text_e.SetValue("%.1f" % matrix.e)  # Translate X
            self.text_f.SetValue("%.1f" % matrix.f)  # Translate Y

    def select_ready(self, v):
        """
        Enables the relevant buttons when there is a selection in the elements.
        :param v: whether selection is currently drag ready.
        :return:
        """
        self.button_scale_down.Enable(v)
        self.button_scale_up.Enable(v)
        self.button_rotate_ccw.Enable(v)
        self.button_rotate_cw.Enable(v)
        self.button_translate_down.Enable(v)
        self.button_translate_up.Enable(v)
        self.button_translate_left.Enable(v)
        self.button_translate_right.Enable(v)
        self.button_reset.Enable(v)

    def matrix_updated(self):
        self.context.signal("refresh_scene")
        self.update_matrix_text()

    def scaleit(self, scale):
        self.context("scale %f %f \n" % (scale, scale))
        self.matrix_updated()

    def rotateit(self, angle):
        self.context("rotate %fdeg \n" % (angle))
        self.matrix_updated()

    def translateit(self, dx, dy):
        self.context("translate %f %f\n" % (dx, dy))
        self.matrix_updated()

    def on_scale_down_50(self, event=None):  # wxGlade: Navigation.<event_handler>
        scale = 2.0 / 3.0  # 66.6% - inverse of 150%
        self.scaleit(scale)

    def on_scale_up_50(self, event=None):  # wxGlade: Navigation.<event_handler>
        scale = 3.0 / 2.0  # 150%
        self.scaleit(scale)

    def on_scale_down_5(self, event=None):  # wxGlade: Navigation.<event_handler>
        scale = 19.0 / 20.0
        self.scaleit(scale)

    def on_scale_up_5(self, event=None):  # wxGlade: Navigation.<event_handler>
        scale = 20.0 / 19.0
        self.scaleit(scale)

    def on_translate_up_1(self, event=None):  # wxGlade: Navigation.<event_handler>
        dx = 0
        dy = -self.context.navigate_jog
        self.translateit(dx, dy)

    def on_translate_up_10(self, event=None):  # wxGlade: Navigation.<event_handler>
        dx = 0
        dy = -self.context.navigate_jog * 10
        self.translateit(dx, dy)

    def on_translate_left_1(self, event=None):  # wxGlade: Navigation.<event_handler>
        dx = -self.context.navigate_jog
        dy = 0
        self.translateit(dx, dy)

    def on_translate_left_10(self, event=None):  # wxGlade: Navigation.<event_handler>
        dx = -self.context.navigate_jog * 10
        dy = 0
        self.translateit(dx, dy)

    def on_translate_right_1(self, event=None):  # wxGlade: Navigation.<event_handler>
        dx = self.context.navigate_jog
        dy = 0
        self.translateit(dx, dy)

    def on_translate_right_10(self, event=None):  # wxGlade: Navigation.<event_handler>
        dx = self.context.navigate_jog * 10
        dy = 0
        self.translateit(dx, dy)

    def on_translate_down_1(self, event=None):  # wxGlade: Navigation.<event_handler>
        dx = 0
        dy = self.context.navigate_jog
        self.translateit(dx, dy)

    def on_translate_down_10(self, event=None):  # wxGlade: Navigation.<event_handler>
        dx = 0
        dy = self.context.navigate_jog * 10
        self.translateit(dx, dy)

    def on_reset(self, event=None):  # wxGlade: Navigation.<event_handler>
        self.context("reset\n")
        self.matrix_updated()

    def on_rotate_ccw_5(self, event=None):  # wxGlade: Navigation.<event_handler>
        angle = -5.0
        self.rotateit(angle)

    def on_rotate_cw_5(self, event=None):  # wxGlade: Navigation.<event_handler>
        angle = 5.0
        self.rotateit(angle)

    def on_rotate_ccw_90(self, event=None):  # wxGlade: Navigation.<event_handler>
        angle = -90.0
        self.rotateit(angle)

    def on_rotate_cw_90(self, event=None):  # wxGlade: Navigation.<event_handler>
        angle = 90.0
        self.rotateit(angle)

    @staticmethod
    def skewed_value(stxt):
        return float(
            Angle.parse(stxt).as_radians
        )  # Temp fix until svgelements fix is merged
        # return Angle.parse(stxt).as_radians

    @staticmethod
    def scaled_value(stxt):
        if stxt.endswith("%"):
            valu = float(stxt[:-1]) / 100.0
        else:
            valu = float(stxt)
        return valu

    def on_text_matrix(self, event=None):  # wxGlade: Navigation.<event_handler>
        try:
            event.Skip()
            sc_x = self.scaled_value(self.text_a.GetValue())
            sk_x = self.skewed_value(self.text_c.GetValue())
            sc_y = self.scaled_value(self.text_d.GetValue())
            sk_y = self.skewed_value(self.text_b.GetValue())
            tl_x = float(self.text_e.GetValue())
            tl_y = float(self.text_f.GetValue())
            f = self.context.elements.first_element(emphasized=True)
            matrix = f.transform
            if (
                sc_x == matrix.a
                and sk_y == matrix.b
                and sk_x == matrix.c
                and sc_y == matrix.d
                and tl_x == matrix.e
                and tl_y == matrix.f
            ):
                return
            # SVG defines the transformation Matrix as  - Matrix parameters are
            #  Scale X  - Skew X  - Translate X            1 - 3 - 5
            #  Skew Y   - Scale Y - Translate Y            2 - 4 - 6
            self.context(
                "matrix %f %f %f %f %s %s\n"
                % (
                    sc_x,  # Scale X
                    sk_y,  # Skew Y
                    sk_x,  # Skew X
                    sc_y,  # Scale Y
                    tl_x,  # Translate X
                    tl_y,  # Translate Y
                )
            )
            self.context.signal("refresh_scene")
        except ValueError:
            pass

        self.update_matrix_text()


class JogDistancePanel(wx.Panel):
    def __init__(self, *args, context=None, pane=False, **kwds):
        # begin wxGlade: JogDistancePanel.__init__
        kwds["style"] = kwds.get("style", 0) | wx.TAB_TRAVERSAL
        wx.Panel.__init__(self, *args, **kwds)
        self.context = context
        self.spin_jog_mils = wx.SpinCtrlDouble(
            self,
            wx.ID_ANY,
            style=wx.TE_PROCESS_ENTER,
            value="100.0",
            min=0.0,
            max=10000.0,
        )
        self.spin_jog_inch = wx.SpinCtrlDouble(
            self, wx.ID_ANY, style=wx.TE_PROCESS_ENTER, value="0.394", min=0.0, max=10.0
        )
        self.spin_jog_mm = wx.SpinCtrlDouble(
            self, wx.ID_ANY, style=wx.TE_PROCESS_ENTER, value="10.0", min=0.0, max=254.0
        )
        self.spin_jog_cm = wx.SpinCtrlDouble(
            self, wx.ID_ANY, style=wx.TE_PROCESS_ENTER, value="1.0", min=0.0, max=25.4
        )

        # begin wxGlade: JogDistancePanel.__set_properties
        self.spin_jog_mils.SetMinSize((80, 23))
        self.spin_jog_mils.SetToolTip(
            _("Set Jog Distance in mils (1/1000th of an inch)")
        )
        self.spin_jog_mm.SetMinSize((80, 23))
        self.spin_jog_mm.SetToolTip(_("Set Jog Distance in mm"))
        self.spin_jog_cm.SetMinSize((80, 23))
        self.spin_jog_cm.SetToolTip(_("Set Jog Distance in cm"))
        self.spin_jog_inch.SetMinSize((80, 23))
        self.spin_jog_inch.SetToolTip(_("Set Jog Distance in inch"))
        # end wxGlade
        # begin wxGlade: JogDistancePanel.__do_layout
        main_sizer = wx.StaticBoxSizer(
            wx.StaticBox(self, wx.ID_ANY, _("Jog Distance:")), wx.VERTICAL
        )
        row_1 = wx.BoxSizer(wx.HORIZONTAL)
        main_sizer.Add(row_1, 0, wx.EXPAND, 0)
        if pane:
            row_2 = wx.BoxSizer(wx.HORIZONTAL)
            main_sizer.Add(row_2, 0, wx.EXPAND, 0)
        else:
            row_2 = row_1
        cm_sizer = wx.StaticBoxSizer(
            wx.StaticBox(self, wx.ID_ANY, _("cm")), wx.VERTICAL
        )
        mm_sizer = wx.StaticBoxSizer(
            wx.StaticBox(self, wx.ID_ANY, _("mm")), wx.VERTICAL
        )
        in_sizer = wx.StaticBoxSizer(
            wx.StaticBox(self, wx.ID_ANY, _("inches")), wx.VERTICAL
        )
        st_sizer = wx.StaticBoxSizer(
            wx.StaticBox(self, wx.ID_ANY, _("steps")), wx.VERTICAL
        )
        st_sizer.Add(self.spin_jog_mils, 0, 0, 0)
        row_1.Add(st_sizer, 0, wx.EXPAND, 0)
        in_sizer.Add(self.spin_jog_inch, 0, 0, 0)
        row_1.Add(in_sizer, 0, wx.EXPAND, 0)
        mm_sizer.Add(self.spin_jog_mm, 0, 0, 0)
        row_2.Add(mm_sizer, 0, wx.EXPAND, 0)
        cm_sizer.Add(self.spin_jog_cm, 0, 0, 0)
        row_2.Add(cm_sizer, 0, wx.EXPAND, 0)
        self.SetSizer(main_sizer)
        main_sizer.Fit(self)
        self.Layout()

        self.Bind(wx.EVT_SPINCTRLDOUBLE, self.on_spin_jog_distance, self.spin_jog_mils)
        self.Bind(wx.EVT_TEXT_ENTER, self.on_spin_jog_distance, self.spin_jog_mils)
        self.Bind(wx.EVT_SPINCTRLDOUBLE, self.on_spin_jog_distance, self.spin_jog_mm)
        self.Bind(wx.EVT_TEXT_ENTER, self.on_spin_jog_distance, self.spin_jog_mm)
        self.Bind(wx.EVT_SPINCTRLDOUBLE, self.on_spin_jog_distance, self.spin_jog_cm)
        self.Bind(wx.EVT_TEXT_ENTER, self.on_spin_jog_distance, self.spin_jog_cm)
        self.Bind(wx.EVT_SPINCTRLDOUBLE, self.on_spin_jog_distance, self.spin_jog_inch)
        self.Bind(wx.EVT_TEXT_ENTER, self.on_spin_jog_distance, self.spin_jog_inch)
        # end wxGlade

    def initialize(self, *args):
        self.set_jog_distances(self.context.navigate_jog)
        self.Children[0].SetFocus()

    def set_jog_distances(self, jog_mils):
        self.spin_jog_mils.SetValue(jog_mils)
        self.spin_jog_mm.SetValue(jog_mils / MILS_IN_MM)
        self.spin_jog_cm.SetValue(jog_mils / (MILS_IN_MM * 10.0))
        self.spin_jog_inch.SetValue(jog_mils / 1000.0)

    def on_spin_jog_distance(self, event):  # wxGlade: Navigation.<event_handler>
        if event.Id == self.spin_jog_mils.Id:
            self.context.navigate_jog = float(self.spin_jog_mils.GetValue())
        elif event.Id == self.spin_jog_mm.Id:
            self.context.navigate_jog = float(self.spin_jog_mm.GetValue() * MILS_IN_MM)
        elif event.Id == self.spin_jog_cm.Id:
            self.context.navigate_jog = float(
                self.spin_jog_cm.GetValue() * MILS_IN_MM * 10.0
            )
        else:
            self.context.navigate_jog = float(self.spin_jog_inch.GetValue() * 1000.0)
        self.set_jog_distances(int(self.context.navigate_jog))


class NavigationPanel(wx.Panel):
    def __init__(self, *args, context=None, **kwds):
        kwds["style"] = kwds.get("style", 0) | wx.TAB_TRAVERSAL
        wx.Panel.__init__(self, *args, **kwds)
        self.context = context

        main_sizer = wx.BoxSizer(wx.VERTICAL)
        pulse_and_move_sizer = wx.BoxSizer(wx.HORIZONTAL)
        main_panels_sizer = wx.BoxSizer(wx.HORIZONTAL)

        jogdistancepanel = JogDistancePanel(self, wx.ID_ANY, context=self.context)
        main_sizer.Add(jogdistancepanel, 0, wx.EXPAND, 0)

        navigationpanel = Jog(self, wx.ID_ANY, context=self.context)
        main_panels_sizer.Add(navigationpanel, 1, wx.EXPAND, 0)

        alignpanel = Drag(self, wx.ID_ANY, context=self.context)
        main_panels_sizer.Add(alignpanel, 1, wx.EXPAND, 0)

        transformpanel = Transform(self, wx.ID_ANY, context=self.context)

        main_panels_sizer.Add(transformpanel, 0, 0, 0)
        main_sizer.Add(main_panels_sizer, 0, wx.EXPAND, 0)

        short_pulse = PulsePanel(self, wx.ID_ANY, context=self.context)
        pulse_and_move_sizer.Add(short_pulse, 0, wx.EXPAND, 0)

        move_panel = MovePanel(self, wx.ID_ANY, context=self.context)
        pulse_and_move_sizer.Add(move_panel, 0, wx.EXPAND, 0)

        size_panel = SizePanel(self, wx.ID_ANY, context=self.context)
        pulse_and_move_sizer.Add(size_panel, 0, wx.EXPAND, 0)

        main_sizer.Add(pulse_and_move_sizer, 1, wx.EXPAND, 0)
        self.SetSizer(main_sizer)
        self.Layout()
        self.panels = [
            jogdistancepanel,
            navigationpanel,
            alignpanel,
            transformpanel,
            short_pulse,
            move_panel,
            size_panel,
        ]
        # end wxGlade

    def initialize(self):
        for p in self.panels:
            try:
                p.initialize()
            except AttributeError:
                pass

    def finalize(self):
        for p in self.panels:
            try:
                p.finalize()
            except AttributeError:
                pass


class Navigation(MWindow):
    def __init__(self, *args, **kwds):
        super().__init__(598, 429, *args, **kwds)

        self.panel = NavigationPanel(self, wx.ID_ANY, context=self.context)

        _icon = wx.NullIcon
        _icon.CopyFromBitmap(icons8_move_50.GetBitmap())
        self.SetIcon(_icon)
        # begin wxGlade: Navigation.__set_properties
        self.SetTitle(_("Navigation"))

    def window_open(self):
        self.panel.initialize()

    def window_close(self):
        self.panel.finalize()