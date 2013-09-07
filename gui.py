from gi.repository import Gtk

import logic_layer

class _Window:
    def __init__(self, gui, xmlpath, window_name, handlers):
        self._gui = gui
        
        builder = Gtk.Builder()
        builder.add_objects_from_file(xmlpath, [window_name])
        self._window = builder.get_object(window_name)
        builder.connect_signals(handlers)

    def show(self):
        self._window.show()
        
    def hide(self):
        self._window.hide()
        
    # Interface for the GUI-main-object
    # TODO: Throw fitting exceptions
    def set_object(self, obj):
        """Make the window display the given object. Window keeps a reference
        to the object in order to update it if the user demands it"""
        pass
        
    def clear_object(self):
        """Resets all fields in the window to their default value. If the
        window still holds a reference to an object, the reference is
        discarded"""
        pass

class _MainWindow(_Window):
    def __init__(self, gui, xmlpath):
        WINDOW_NAME = "main_window"
        HANDLERS = {
            "create_contract_button_clicked": self._show_create_contract_window,
            "quit_button_clicked": self._quit
        }
        
        _Window.__init__(self, gui, xmlpath, WINDOW_NAME, HANDLERS)
        
    def set_object(self):
        # The main window does not display any objects
        pass
        
    def clear(self):
        # The main window does not display any objects
        pass
    
    def _show_create_contract_window(self, button):
        # Not yet implemented
        #self._gui.show_create_contract_window()
        pass
    
    def _quit(self, button):
        self._gui.quit()
        
class Gui:
    XML_PATH = "guixml/gui.xml"

    def __init__(self, db_path="work.db"):
        self._logic_controller = logic_layer.LogicController(db_path)
        self._main_window = _MainWindow(self, Gui.XML_PATH)
        self._windows = [self._main_window]
        
    def run(self):
        self._main_window.show()
        Gtk.main()
        
    def quit(self):
        Gtk.main_quit()
        
    def get_logic_controller(self):
        return self._logic_controller
    
    def create_and_show_contract_window(self):
        pass