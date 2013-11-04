from gi.repository import Gtk
from gi.repository import GObject

import datetime

import logic_layer

class ObjectChooserButton:
    def __init__(self, button):
        self._button = button
        self._model = Gtk.ListStore(GObject.TYPE_STRING, GObject.TYPE_OBJECT)
        self._button.set_model(self._model)
        self._button.set_entry_text_column(0)
        
    def populate_model(self, objects):
        for entry in objects:
            self._model.append([str(entry), entry])
            
    def get_chosen_object(self):
        tree_iter = self._button.get_active_iter()
        return self._model[tree_iter][1]


class GContract(GObject.GObject):
    def __init__(self, contract):
        super(GContract, self).__init__()
        self.contract = contract
        
    def __str__(self):
        return self.contract.name

class _Window:
    def __init__(self, gui, xmlpath, window_name, handlers):
        self._gui = gui
        
        builder = Gtk.Builder()
        builder.add_from_file(xmlpath)
        self._window = builder.get_object(window_name)
        builder.connect_signals(handlers)
        self._set_internal_objects(builder)

    def show(self):
        self._window.show()
        
    def hide(self):
        self._window.hide()
        
    def _set_internal_objects(self, builder):
        """Subclasses may implement this method to keep references
        to important elements of the window, such as, e.g., text inputs"""
        pass
        
    # Interface for the GUI-main-object
    # TODO: Throw fitting exceptions
    def set_object(self, obj):
        """Make the window display the given object. Window keeps a reference
        to the object in order to update it if the user demands it"""
        pass
        
    def clear(self):
        """Resets all fields in the window to their default value. If the
        window still holds a reference to an object, the reference is
        discarded"""
        pass

class _MainWindow(_Window):
    def __init__(self, gui):
        XMLPATH = "guixml/contract.glade"
        WINDOW_NAME = "main_window"
        HANDLERS = {
            "create_button_clicked": self._show_create_contract_window,
            "quit_button_clicked": self._quit,
        }
        
        _Window.__init__(self, gui, XMLPATH, WINDOW_NAME, HANDLERS)
        
    def set_object(self):
        # The main window does not display any objects
        pass
        
    def clear(self):
        # The main window does not display any objects
        pass
    
    def _show_create_contract_window(self, button):
        self._gui.create_and_show_contract_window()
        pass
    
    def _quit(self, button):
        self._gui.quit()
        
class _ContractWindow(_Window):
    def __init__(self, gui):
        XMLPATH = "guixml/contract.glade"
        WINDOW_NAME = "contract_window"
        HANDLERS = {
            "create_button_clicked": self._create_contract,
            "abort_button_clicked": self._abort
        }
        
        _Window.__init__(self, gui, XMLPATH, WINDOW_NAME, HANDLERS)
        
        self._initialize_calendars()
        
    def _initialize_calendars(self):
        today = datetime.date.today()
        self._start_calendar.select_month(today.month, today.year)
        self._start_calendar.select_day(today.day)
        self._end_calendar.select_month(today.month, today.year)
        self._end_calendar.select_day(today.day)
        
    def _set_internal_objects(self, builder):
        self._name_buffer = builder.get_object("name_entry").get_buffer()
        self._hours_adjustment = builder.get_object("hours_button").get_adjustment()
        self._start_calendar = builder.get_object("start_calendar")
        self._end_calendar = builder.get_object("end_calendar")
        
    def _create_contract(self, button):
        crud_controller = self._gui.get_logic_controller().crud_controller
        
        contract_name = self._name_buffer.get_text()
        hours = int(self._hours_adjustment.get_value())
        start_year, start_month, start_day = self._start_calendar.get_date()
        start_date = datetime.date(start_year, start_month, start_day)
        end_year, end_month, end_day = self._end_calendar.get_date()
        end_date = datetime.date(end_year, end_month, end_day)
        
        crud_controller.create_contract(contract_name, start_date, end_date, hours)
    
    def _abort(self, button):
        self._gui.destroy_window(self)
        
class _ProjectWindow(_Window):
    def __init__(self, gui):
        XMLPATH = "guixml/project.glade"
        WINDOW_NAME = "project_window"
        HANDLERS = {
            "create_button_clicked": self._create_project,
            "abort_button_clicked": self._abort
        }
        
        _Window.__init__(self, gui, XMLPATH, WINDOW_NAME, HANDLERS)

        self._populate_contract_model()
        
    def _set_internal_objects(self, builder):
        self._project_entry = builder.get_object("name_entry")
        self._contract_box = builder.get_object("contract_combobox")
        
    def _populate_contract_model(self):
        gcontracts = []
        for contract in self._gui.get_logic_controller().crud_controller.retrieve_all_contracts():
            gcontracts.append(GContract(contract))
        
        self._contract_chooser = ObjectChooserButton(self._contract_box)
        self._contract_chooser.populate_model(gcontracts)
            
        
    def _create_project(self, button):
        project_name = self._project_entry.get_text()
        contract = self._contract_chooser.get_chosen_object()
        print project_name
        print str(contract)

        #self._gui._logic_controller.crud_controller.create_project(project_name, contract)
    
    def _abort(self, button):
        self._gui.destroy_window(self)
        
class Gui:
    def __init__(self, db_path="work.db"):
        self._logic_controller = logic_layer.LogicController(db_path)
        self._main_window = _ProjectWindow(self)
        self._windows = [self._main_window]
        self._main_window._window.connect("destroy", Gtk.main_quit)
        
    def run(self):
        self._main_window.show()
        Gtk.main()
        
    def quit(self):
        Gtk.main_quit()
        
    def get_logic_controller(self):
        return self._logic_controller
    
    def create_and_show_contract_window(self):
        contract_window = _ContractWindow(self, Gui.XML_PATH)
        contract_window.show()
        self._windows.append(contract_window)
        
    def destroy_window(self, window):
        pass