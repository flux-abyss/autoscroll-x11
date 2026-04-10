#!/usr/bin/env python3
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

class ScrollTest(Gtk.Window):
    def __init__(self):
        super().__init__(title="Autoscroll Test Box")
        self.set_default_size(600, 400)

        scrolled = Gtk.ScrolledWindow()
        self.add(scrolled)

        # Big grid so both directions scroll
        grid = Gtk.Grid()
        grid.set_row_spacing(10)
        grid.set_column_spacing(10)

        for i in range(50):
            for j in range(50):
                label = Gtk.Label(label=f"{i},{j}")
                frame = Gtk.Frame()
                frame.set_size_request(80, 40)
                frame.add(label)
                grid.attach(frame, j, i, 1, 1)

        scrolled.add(grid)

        self.connect("destroy", Gtk.main_quit)

win = ScrollTest()
win.show_all()
Gtk.main()