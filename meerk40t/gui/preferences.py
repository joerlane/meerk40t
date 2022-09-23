# -*- coding: ISO-8859-1 -*-
#
# generated by wxGlade 0.9.3 on Thu Jun 27 21:45:40 2019
#
import platform

import wx

from .choicepropertypanel import ChoicePropertyPanel
from .icons import icons8_administrative_tools_50
from .mwindow import MWindow
from .wxutils import TextCtrl

_ = wx.GetTranslation


class PreferencesUnitsPanel(wx.Panel):
    def __init__(self, *args, context=None, **kwds):
        # begin wxGlade: PreferencesUnitsPanel.__init__
        kwds["style"] = kwds.get("style", 0)
        wx.Panel.__init__(self, *args, **kwds)
        self.context = context

        sizer_1 = wx.BoxSizer(wx.HORIZONTAL)

        self.radio_units = wx.RadioBox(
            self,
            wx.ID_ANY,
            _("Units"),
            choices=[_("mm"), _("cm"), _("inch"), _("mils")],
            majorDimension=1,
            style=wx.RA_SPECIFY_ROWS,
        )
        self.radio_units.SetToolTip(_("Set default units for guides"))
        sizer_1.Add(self.radio_units, 0, wx.EXPAND, 0)

        self.SetSizer(sizer_1)

        self.Layout()

        self.Bind(wx.EVT_RADIOBOX, self.on_radio_units, self.radio_units)

        self.radio_units.SetSelection(self._get_units_index())

    def on_radio_units(self, event):
        if event.Int == 0:
            self.set_mm()
        elif event.Int == 1:
            self.set_cm()
        elif event.Int == 2:
            self.set_inch()
        elif event.Int == 3:
            self.set_mil()

    def _get_units_index(self):
        p = self.context.root
        units = p.units_name
        if units == "mm":
            return 0
        if units == "cm":
            return 1
        if units in ("in", "inch", "inches"):
            return 2
        if units == "mil":
            return 3
        return 0

    def set_inch(self):
        p = self.context.root
        p.units_name = "inch"
        p.signal("units", p.units_name)

    def set_mil(self):
        p = self.context.root
        p.units_name = "mil"
        p.signal("units", p.units_name)

    def set_cm(self):
        p = self.context.root
        p.units_name = "cm"
        p.signal("units", p.units_name)

    def set_mm(self):
        p = self.context.root
        p.units_name = "mm"
        p.signal("units", p.units_name)


# end of class PreferencesUnitsPanel


class PreferencesLanguagePanel(wx.Panel):
    def __init__(self, *args, context=None, **kwds):
        # begin wxGlade: PreferencesLanguagePanel.__init__
        kwds["style"] = kwds.get("style", 0)
        wx.Panel.__init__(self, *args, **kwds)
        self.context = context

        sizer_2 = wx.StaticBoxSizer(
            wx.StaticBox(self, wx.ID_ANY, _("Language")), wx.HORIZONTAL
        )
        from .wxmeerk40t import supported_languages

        choices = [
            language_name
            for language_code, language_name, language_index in supported_languages
        ]
        self.combo_language = wx.ComboBox(
            self, wx.ID_ANY, choices=choices, style=wx.CB_READONLY
        )
        self.combo_language.SetToolTip(
            _("Select the desired language to use (requires a restart to take effect).")
        )
        sizer_2.Add(self.combo_language, 0, wx.ALIGN_CENTER_VERTICAL, 0)

        self.SetSizer(sizer_2)

        self.Layout()

        self.context.setting(int, "language", 0)

        self.Bind(wx.EVT_COMBOBOX, self.on_combo_language, self.combo_language)
        # end wxGlade
        self.combo_language.SetSelection(self.context.language)

    def on_combo_language(self, event=None):
        lang = self.combo_language.GetSelection()
        if lang != -1 and self.context.app is not None:
            self.context.app.update_language(lang)


# end of class PreferencesLanguagePanel


class PreferencesPixelsPerInchPanel(wx.Panel):
    def __init__(self, *args, context=None, **kwds):
        # begin wxGlade: PreferencesPixelsPerInchPanel.__init__
        kwds["style"] = kwds.get("style", 0)
        wx.Panel.__init__(self, *args, **kwds)
        self.context = context

        sizer_3 = wx.StaticBoxSizer(
            wx.StaticBox(self, wx.ID_ANY, _("SVG Pixel Per Inch")), wx.HORIZONTAL
        )

        self.combo_svg_ppi = wx.ComboBox(
            self,
            wx.ID_ANY,
            choices=[
                _("96 px/in Inkscape"),
                _("72 px/in Illustrator"),
                _("90 px/in Old Inkscape"),
                _("Custom"),
            ],
            style=wx.CB_READONLY,
        )
        self.combo_svg_ppi.SetToolTip(
            _("Select the Pixels Per Inch to use when loading an SVG file")
        )
        sizer_3.Add(self.combo_svg_ppi, 0, wx.ALIGN_CENTER_VERTICAL, 0)

        sizer_3.Add((20, 20), 0, 0, 0)

        self.text_svg_ppi = TextCtrl(
            self, wx.ID_ANY, "", check="float", style=wx.TE_PROCESS_ENTER, limited=True
        )
        # self.text_svg_ppi.SetMinSize((60, 23))
        self.text_svg_ppi.SetToolTip(
            _("Custom Pixels Per Inch to use when loading an SVG file")
        )
        sizer_3.Add(self.text_svg_ppi, 1, wx.EXPAND, 0)

        self.SetSizer(sizer_3)

        self.Layout()

        self.Bind(wx.EVT_COMBOBOX, self.on_combo_svg_ppi, self.combo_svg_ppi)
        self.text_svg_ppi.SetActionRoutine(self.on_text_svg_ppi)
        # end wxGlade

        context.elements.setting(float, "svg_ppi", 96.0)
        self.text_svg_ppi.SetValue(str(context.elements.svg_ppi))
        self.on_text_svg_ppi()

    def on_combo_svg_ppi(self, event=None):
        elements = self.context.elements
        ppi = self.combo_svg_ppi.GetSelection()
        if ppi == 0:
            elements.svg_ppi = 96.0
        elif ppi == 1:
            elements.svg_ppi = 72.0
        elif ppi == 2:
            elements.svg_ppi = 90.0
        else:
            elements.svg_ppi = 96.0
        self.text_svg_ppi.SetValue(str(elements.svg_ppi))

    def on_text_svg_ppi(self):
        elements = self.context.elements
        try:
            svg_ppi = float(self.text_svg_ppi.GetValue())
        except ValueError:
            return
        if svg_ppi == 96:
            if self.combo_svg_ppi.GetSelection() != 0:
                self.combo_svg_ppi.SetSelection(0)
        elif svg_ppi == 72:
            if self.combo_svg_ppi.GetSelection() != 1:
                self.combo_svg_ppi.SetSelection(1)
        elif svg_ppi == 90:
            if self.combo_svg_ppi.GetSelection() != 2:
                self.combo_svg_ppi.SetSelection(2)
        else:
            if self.combo_svg_ppi.GetSelection() != 3:
                self.combo_svg_ppi.SetSelection(3)
        elements.svg_ppi = svg_ppi


# end of class PreferencesPixelsPerInchPanel


class PreferencesMain(wx.Panel):
    def __init__(self, *args, context=None, **kwds):
        # begin wxGlade: PreferencesMain.__init__
        kwds["style"] = kwds.get("style", 0)
        wx.Panel.__init__(self, *args, **kwds)
        self.context = None

        sizer_main = wx.BoxSizer(wx.VERTICAL)

        self.panel_units = PreferencesUnitsPanel(self, wx.ID_ANY, context=context)
        sizer_main.Add(self.panel_units, 0, wx.EXPAND, 0)

        self.panel_language = PreferencesLanguagePanel(self, wx.ID_ANY, context=context)
        sizer_main.Add(self.panel_language, 0, wx.EXPAND, 0)

        self.panel_ppi = PreferencesPixelsPerInchPanel(self, wx.ID_ANY, context=context)
        sizer_main.Add(self.panel_ppi, 0, wx.EXPAND, 0)

        self.panel_pref1 = ChoicePropertyPanel(
            self,
            id=wx.ID_ANY,
            context=context,
            choices="preferences",
            constraint=("-Classification", "-Gui", "-Scene"),
        )
        sizer_main.Add(self.panel_pref1, 1, wx.EXPAND, 0)

        self.SetSizer(sizer_main)

        self.Layout()
        # end wxGlade

    def delegates(self):
        yield self.panel_ppi
        yield self.panel_language
        yield self.panel_units
        yield self.panel_pref1


# end of class PreferencesMain

#
# class PreferencesPanel(wx.Panel):
#     def __init__(self, *args, context=None, **kwds):
#         # begin wxGlade: PreferencesPanel.__init__
#         kwds["style"] = kwds.get("style", 0)
#         wx.Panel.__init__(self, *args, **kwds)
#         self.context = context
#
#         sizer_settings = wx.BoxSizer(wx.VERTICAL)
#
#         self.panel_main = PreferencesMain(self, wx.ID_ANY, context=context)
#         sizer_settings.Add(self.panel_main, 1, wx.EXPAND, 0)
#
#         self.SetSizer(sizer_settings)
#
#         self.Layout()
#         # end wxGlade
#
#     def delegates(self):
#         yield self.panel_main


class Preferences(MWindow):
    def __init__(self, *args, **kwds):
        super().__init__(
            525,
            605,
            *args,
            style=wx.CAPTION
            | wx.CLOSE_BOX
            | wx.FRAME_FLOAT_ON_PARENT
            | wx.TAB_TRAVERSAL
            | (wx.RESIZE_BORDER if platform.system() != "Darwin" else 0),
            **kwds,
        )
        self.notebook_main = wx.aui.AuiNotebook(
            self,
            -1,
            style=wx.aui.AUI_NB_TAB_EXTERNAL_MOVE
            | wx.aui.AUI_NB_SCROLL_BUTTONS
            | wx.aui.AUI_NB_TAB_SPLIT
            | wx.aui.AUI_NB_TAB_MOVE,
        )

        # self.panel_main = PreferencesPanel(self, wx.ID_ANY, context=self.context)
        self.panel_main = PreferencesMain(self, wx.ID_ANY, context=self.context)

        self.panel_classification = ChoicePropertyPanel(
            self,
            id=wx.ID_ANY,
            context=self.context,
            choices="preferences",
            constraint=("Classification"),
        )
        self.panel_classification.SetupScrolling()

        self.panel_gui = ChoicePropertyPanel(
            self,
            id=wx.ID_ANY,
            context=self.context,
            choices="preferences",
            constraint=("Gui"),
        )
        self.panel_gui.SetupScrolling()

        self.panel_scene = ChoicePropertyPanel(
            self,
            id=wx.ID_ANY,
            context=self.context,
            choices="preferences",
            constraint=("Scene"),
        )
        self.panel_scene.SetupScrolling()

        main_scene = getattr(self.context.root, "mainscene", None)
        colorchoices = []
        local_default_color = []
        for key in main_scene.colors.default_color:
            local_default_color.append(key)
        local_default_color.sort()
        section = ""
        for key in local_default_color:
            colorkey = f"color_{key}"
            defaultcolor = main_scene.colors.default_color[key]
            # Try to make a sensible name out of it
            keyname = key.replace("_", " ")
            idx = 1  # Intentionally
            while idx < len(keyname):
                if keyname[idx] in "0123456789" and keyname[idx - 1] != " ":
                    keyname = keyname[:idx] + " " + keyname[idx:]
                idx += 1
            keyname = keyname[0].upper() + keyname[1:]
            words = keyname.split()
            possible_section = words[0]
            if possible_section[0:2] != section[0:2]:
                section = possible_section
            singlechoice = {
                "attr": colorkey,
                "object": self.context,
                "default": defaultcolor,
                "type": str,
                "style": "color",  # hexa representation
                "label": keyname,
                "section": section,
                "signals": ("refresh_scene", "theme"),
            }
            colorchoices.append(singlechoice)

        self.panel_color = ChoicePropertyPanel(
            self,
            id=wx.ID_ANY,
            context=self.context,
            choices=colorchoices,
            entries_per_column=12,
        )
        self.panel_color.SetupScrolling()

        self.notebook_main.AddPage(self.panel_main, _("General"))
        self.notebook_main.AddPage(self.panel_classification, _("Classification"))
        self.notebook_main.AddPage(self.panel_gui, _("GUI"))
        self.notebook_main.AddPage(self.panel_scene, _("Scene"))
        self.notebook_main.AddPage(self.panel_color, _("Colors"))
        self.Layout()

        _icon = wx.NullIcon
        _icon.CopyFromBitmap(icons8_administrative_tools_50.GetBitmap())
        self.SetIcon(_icon)
        self.SetTitle(_("Preferences"))

    def delegates(self):
        yield self.panel_main
        yield self.panel_classification
        yield self.panel_gui
        yield self.panel_scene
        yield self.panel_color

    @staticmethod
    def sub_register(kernel):
        import platform

        if platform.system() != "Darwin":
            kernel.register(
                "button/config/Preferences",
                {
                    "label": _("Preferences"),
                    "icon": icons8_administrative_tools_50,
                    "tip": _("Opens Preferences Window"),
                    "action": lambda v: kernel.console("window toggle Preferences\n"),
                },
            )

    def window_open(self):
        pass

    def window_close(self):
        pass

    @staticmethod
    def menu_label():
        return _("Pr&eferences...\tCtrl-,")

    @staticmethod
    def menu_tip():
        return _("Show/Hide the Preferences window")

    @staticmethod
    def menu_id():
        return wx.ID_PREFERENCES
