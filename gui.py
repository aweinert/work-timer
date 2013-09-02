from gi.repository import Gtk

class _MainWindow:
    _WINDOW_NAME = "main_window"
    
    def __init__(self, gui, xmlpath):
        self._gui = gui
        
        builder = Gtk.Builder()
        builder.add_objects_from_file(xmlpath, [_MainWindow._WINDOW_NAME])
        self._window = builder.get_object(_MainWindow._WINDOW_NAME)
        self._connect(builder)
        
    def _connect(self, builder):
        handlers = {
            "create_contract_button_clicked": self._show_create_contract_window,
            "quit_button_clicked": self._quit
        }
        
        builder.connect_signals(handlers)
        
    def reset(self):
        pass
    
    def show(self):
        self._window.show()
        
    def shutdown(self):
        self._window.hide()
        
    def _show_create_contract_window(self, button):
        # Not yet implemented
        #self._gui.show_create_contract_window()
        pass
    
    def _quit(self, button):
        self._gui.quit()

class Gui:
    XML_PATH = "guixml/gui.xml"

    def __init__(self):
        self._windows = {
            "main_window": _MainWindow(self, Gui.XML_PATH)
        }
        
    def run(self):
        self._windows["main_window"].show()

        Gtk.main()
        
    def quit(self):
        for window in self._windows.values():
            window.shutdown()
            
        Gtk.main_quit()
    
    def reset_and_show_create_contract_window(self):
        self._reset_window("create_contract_window")
        self._show_window("create_contract_window")
        
    def _reset_window(self, name):
        self._windows[name].reset()
    
    def _show_window(self, name):
        self._windows[name].show()