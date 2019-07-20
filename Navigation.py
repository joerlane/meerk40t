# -*- coding: ISO-8859-1 -*-
#
# generated by wxGlade 0.9.3 on Thu Jun 27 21:45:40 2019
#

import wx
# begin wxGlade: dependencies
# end wxGlade

# begin wxGlade: extracode
# end wxGlade


class Navigation(wx.Frame):
    def __init__(self, *args, **kwds):
        # begin wxGlade: Navigation.__init__
        kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        self.bitmap_button_1 = wx.BitmapButton(self, wx.ID_ANY, wx.Bitmap("icons/icons8up.png", wx.BITMAP_TYPE_ANY))
        self.bitmap_button_7 = wx.BitmapButton(self, wx.ID_ANY, wx.Bitmap("icons/icons8-padlock-50.png", wx.BITMAP_TYPE_ANY))
        self.bitmap_button_9 = wx.BitmapButton(self, wx.ID_ANY, wx.Bitmap("icons/icons8-lock-50.png", wx.BITMAP_TYPE_ANY))
        self.bitmap_button_2 = wx.BitmapButton(self, wx.ID_ANY, wx.Bitmap("icons/icons8-left.png", wx.BITMAP_TYPE_ANY))
        self.bitmap_button_6 = wx.BitmapButton(self, wx.ID_ANY, wx.Bitmap("icons/icons8-home-filled-50.png", wx.BITMAP_TYPE_ANY))
        self.bitmap_button_3 = wx.BitmapButton(self, wx.ID_ANY, wx.Bitmap("icons/icons8-right.png", wx.BITMAP_TYPE_ANY))
        self.bitmap_button_4 = wx.BitmapButton(self, wx.ID_ANY, wx.Bitmap("icons/icons8-down.png", wx.BITMAP_TYPE_ANY))
        self.bitmap_button_8 = wx.BitmapButton(self, wx.ID_ANY, wx.Bitmap("icons/icons8-gas-industry-50.png", wx.BITMAP_TYPE_ANY))
        self.spin_jumpamount = wx.SpinCtrlDouble(self, wx.ID_ANY, "10.0", min=0.0, max=1000.0)

        self.__set_properties()
        self.__do_layout()
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: Navigation.__set_properties
        self.SetTitle("Navigation")
        _icon = wx.NullIcon
        _icon.CopyFromBitmap(wx.Bitmap("icons/icons8-move-32.png", wx.BITMAP_TYPE_ANY))
        self.SetIcon(_icon)
        self.bitmap_button_1.SetSize(self.bitmap_button_1.GetBestSize())
        self.bitmap_button_7.SetSize(self.bitmap_button_7.GetBestSize())
        self.bitmap_button_9.SetSize(self.bitmap_button_9.GetBestSize())
        self.bitmap_button_2.SetSize(self.bitmap_button_2.GetBestSize())
        self.bitmap_button_6.SetSize(self.bitmap_button_6.GetBestSize())
        self.bitmap_button_3.SetSize(self.bitmap_button_3.GetBestSize())
        self.bitmap_button_4.SetSize(self.bitmap_button_4.GetBestSize())
        self.bitmap_button_8.SetSize(self.bitmap_button_8.GetBestSize())
        self.spin_jumpamount.SetMinSize((70, 23))
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: Navigation.__do_layout
        sizer_9 = wx.BoxSizer(wx.VERTICAL)
        sizer_15 = wx.BoxSizer(wx.HORIZONTAL)
        grid_sizer_1 = wx.FlexGridSizer(4, 5, 0, 0)
        grid_sizer_1.Add((0, 0), 0, 0, 0)
        grid_sizer_1.Add(self.bitmap_button_1, 0, 0, 0)
        grid_sizer_1.Add((0, 0), 0, 0, 0)
        grid_sizer_1.Add(self.bitmap_button_7, 0, 0, 0)
        grid_sizer_1.Add(self.bitmap_button_9, 0, 0, 0)
        grid_sizer_1.Add(self.bitmap_button_2, 0, 0, 0)
        grid_sizer_1.Add(self.bitmap_button_6, 0, 0, 0)
        grid_sizer_1.Add(self.bitmap_button_3, 0, 0, 0)
        grid_sizer_1.Add((0, 0), 0, 0, 0)
        grid_sizer_1.Add((0, 0), 0, 0, 0)
        grid_sizer_1.Add((0, 0), 0, 0, 0)
        grid_sizer_1.Add(self.bitmap_button_4, 0, 0, 0)
        grid_sizer_1.Add((0, 0), 0, 0, 0)
        grid_sizer_1.Add((0, 0), 0, 0, 0)
        grid_sizer_1.Add((0, 0), 0, 0, 0)
        grid_sizer_1.Add((0, 0), 0, 0, 0)
        grid_sizer_1.Add((0, 0), 0, 0, 0)
        grid_sizer_1.Add((0, 0), 0, 0, 0)
        grid_sizer_1.Add((0, 0), 0, 0, 0)
        grid_sizer_1.Add(self.bitmap_button_8, 0, 0, 0)
        sizer_9.Add(grid_sizer_1, 0, 0, 0)
        sizer_15.Add(self.spin_jumpamount, 0, 0, 0)
        label_mm3 = wx.StaticText(self, wx.ID_ANY, "mm")
        sizer_15.Add(label_mm3, 0, 0, 0)
        sizer_9.Add(sizer_15, 1, wx.EXPAND, 0)
        self.SetSizer(sizer_9)
        sizer_9.Fit(self)
        self.Layout()
        # end wxGlade

# end of class Navigation
