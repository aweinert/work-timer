#!/usr/bin/env python

import gui
import logic_layer

if __name__ == "__main__":

    logic_controller = logic_layer.LogicController("work.db")
    gui_object = gui.Gui(logic_controller)
    gui_object.run()